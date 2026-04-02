#!/usr/bin/env python3
"""
soc_predict.py – Predikce SOC baterie z meteo dat přes Anthropic API
Použití:
  python soc_predict.py --bms bms.csv --meteo meteo.csv --days 7
  python soc_predict.py --bms bms.csv --meteo meteo.csv --days 3 --format table
  python soc_predict.py --bms bms.csv --meteo meteo.csv --days 5 --format csv > forecast.csv

Vyžaduje: pip install anthropic pandas
API klíč: export ANTHROPIC_API_KEY=sk-ant-...
"""

import argparse
import json
import os
import sys
import pandas as pd
from datetime import timedelta

# ── Model konstanty (kalibrováno na 6 denních měření, R²=0.907) ─────────────
SLOPE     = 0.00776   # %SOC / Wh·m⁻²
INTERCEPT = -9.55
CAPACITY  = 630.0     # Ah nominál

# ── Argumenty ─────────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description="SOC forecast from meteo + BMS CSV")
    p.add_argument("--bms",    required=True,  help="Cesta k BMS CSV logu")
    p.add_argument("--meteo",  required=True,  help="Cesta k meteo forecast CSV")
    p.add_argument("--days",   type=int, default=7, help="Počet předpovědních dní (default: 7)")
    p.add_argument("--format", choices=["json", "table", "csv"], default="table",
                   help="Výstupní formát: json | table | csv (default: table)")
    p.add_argument("--bms-rows", type=int, default=20,
                   help="Počet posledních řádků BMS k odeslání do API (default: 20)")
    p.add_argument("--no-api",  action="store_true",
                   help="Přeskočí API, použije jen lineární model (offline)")
    return p.parse_args()

# ── Načtení a preprocessing BMS ──────────────────────────────────────────────
def load_bms(path, tail_rows=20):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["SOC_pct"] = df["SOC Cap. Remain"] / df["SOC Full Charge Cap."] * 100
    last_soc = float(df["SOC_pct"].iloc[-1])
    last_ts  = df["timestamp"].iloc[-1]
    tail_csv = df.tail(tail_rows)[
        ["timestamp", "Battery Current", "Battery Voltage", "SOC_pct", "Max Temp"]
    ].to_csv(index=False)
    return last_soc, last_ts, tail_csv

# ── Načtení a preprocessing meteo ────────────────────────────────────────────
def load_meteo(path, after_ts, n_days):
    df = pd.read_csv(path)
    df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
    try:
        df["time_local"] = df["time_utc"].dt.tz_convert("Europe/Prague")
    except Exception:
        df["time_local"] = df["time_utc"]
    df["date_local"] = df["time_local"].dt.date
    after_date = after_ts.date()
    cutoff_date = after_date + timedelta(days=n_days)
    filt = (df["date_local"] > after_date) & (df["date_local"] <= cutoff_date)
    df = df[filt].copy()
    # Pouze solární hodiny
    solar = df[df["solar_elevation"] > 0]
    # Denní agregáty pro context v promptu
    daily = solar.groupby("date_local").agg(
        rad_sum=("shortwave_radiation_masked", "sum"),
        rad_direct=("direct_radiation_masked", "sum"),
        cloud_avg=("cloud_cover", "mean"),
        max_rad=("shortwave_radiation_masked", "max"),
    ).reset_index()
    meteo_csv = solar[
        ["time_local", "shortwave_radiation_masked", "direct_radiation_masked",
         "cloud_cover", "solar_elevation", "is_shaded"]
    ].to_csv(index=False)
    return meteo_csv, daily

# ── Lineární model (offline fallback) ─────────────────────────────────────────
def linear_forecast(daily_df, soc_start):
    results = []
    soc = soc_start
    for _, row in daily_df.iterrows():
        delta = SLOPE * row["rad_sum"] + INTERCEPT
        soc_eod = min(100.0, max(soc, soc + delta))
        results.append({
            "date":      str(row["date_local"]),
            "rad_sum":   round(float(row["rad_sum"]), 0),
            "cloud_pct": round(float(row["cloud_avg"]), 0),
            "delta_soc": round(delta, 1),
            "soc_eod":   round(soc_eod, 1),
        })
        soc = soc_eod
    return results

# ── Sestavení promptu ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a solar battery SOC forecasting assistant.

SYSTEM CONSTANTS (calibrated, do not re-derive):
- Linear model: delta_SOC% = 0.00776 × rad_sum_Wh_m2 − 9.55  (R²=0.907)
- Charging threshold: ~1230 Wh/m²/day (below = no net charge gain)
- Battery nominal: 630 Ah, usable ~78%
- Charging window: 08:00–17:00 local time
- Best predictors: shortwave_radiation_masked (r=0.953), direct_radiation_masked (r=0.982)

TASK: Using the provided BMS and meteo data, output ONLY valid JSON — no explanation, no markdown, no preamble.

OUTPUT FORMAT:
{
  "soc_start": <float, SOC% from last BMS row>,
  "model": "linear_v1",
  "forecast": [
    {
      "date": "YYYY-MM-DD",
      "rad_sum": <float, Wh/m²>,
      "cloud_pct": <float, %>,
      "delta_soc": <float, %>,
      "soc_eod": <float, %, capped 0-100>
    }
  ]
}

RULES:
- soc_eod[n] = min(100, soc_eod[n-1] + delta_soc[n])
- Use only solar hours (solar_elevation > 0) from meteo CSV
- delta_soc = 0.00776 × daily_rad_sum − 9.55, floor at 0 if rad_sum < 1230
- soc_start = last SOC_pct value from BMS CSV
- Output ONLY the JSON object, nothing else"""

def build_user_message(bms_csv, meteo_csv, last_soc, n_days):
    return f"""Forecast {n_days} days. Last known SOC: {last_soc:.1f}%

<bms_tail>
{bms_csv}
</bms_tail>

<meteo_forecast>
{meteo_csv}
</meteo_forecast>"""

# ── Volání Anthropic API ───────────────────────────────────────────────────────
def call_api(system, user_msg):
    try:
        import anthropic
    except ImportError:
        sys.exit("Chybí balíček anthropic. Spusť: pip install anthropic")
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Chybí ANTHROPIC_API_KEY. Nastav: export ANTHROPIC_API_KEY=sk-ant-...")
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system,
        messages=[{"role": "user", "content": user_msg}]
    )
    raw = msg.content[0].text.strip()
    # Odstraň případné ```json``` wrappy
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)

# ── Formátování výstupu ────────────────────────────────────────────────────────
def fmt_table(result):
    lines = []
    lines.append(f"\nSOC prognóza – start: {result['soc_start']:.1f}%  |  model: {result['model']}\n")
    lines.append(f"{'Datum':<12} {'Záření Wh/m²':>14} {'Oblačnost':>10} {'ΔSOC%':>8} {'SOC konec':>10}")
    lines.append("─" * 58)
    for r in result["forecast"]:
        trend = "↑" if r["delta_soc"] > 0 else "→"
        lines.append(
            f"{r['date']:<12} {r['rad_sum']:>14.0f} {r['cloud_pct']:>9.0f}% "
            f"{r['delta_soc']:>+7.1f}% {r['soc_eod']:>8.1f}% {trend}"
        )
    return "\n".join(lines)

def fmt_csv(result):
    rows = ["date,rad_sum,cloud_pct,delta_soc,soc_eod"]
    for r in result["forecast"]:
        rows.append(f"{r['date']},{r['rad_sum']},{r['cloud_pct']},{r['delta_soc']},{r['soc_eod']}")
    return "\n".join(rows)

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()

    # Načtení dat
    last_soc, last_ts, bms_tail = load_bms(args.bms, args.bms_rows)
    meteo_csv, daily_df = load_meteo(args.meteo, last_ts, args.days)

    if args.no_api or not os.environ.get("ANTHROPIC_API_KEY"):
        # Offline – čistý lineární model
        forecast_list = linear_forecast(daily_df, last_soc)
        result = {
            "soc_start": round(last_soc, 1),
            "model":     "linear_offline",
            "forecast":  forecast_list,
        }
    else:
        # Online – API
        user_msg = build_user_message(bms_tail, meteo_csv, last_soc, args.days)
        result = call_api(SYSTEM_PROMPT, user_msg)

    # Výstup
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "csv":
        print(fmt_csv(result))
    else:
        print(fmt_table(result))

if __name__ == "__main__":
    main()
