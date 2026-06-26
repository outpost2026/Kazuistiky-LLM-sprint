# Reverse Engineering Case Study: Ruida VCF & LightBurn DXF — revised

**Version:** 2.1 **|** **Date:** June 12, 2026

29 days of reverse engineering two proprietary CAM formats — .VCF (Ruida/VCutWorks) and DXF exported from LightBurn. Output: parser with >99.98% accuracy, deployed on GCP Cloud Run.

---

## 1. Key findings (deviations from expected behavior)

### 1.1 VCF is a deterministic binary serialization
Not encrypted, not compressed. IEEE 754 double floats (little-endian), Windows-1250 metadata. 74B segment blocks. Identified via pair-wise hex diff.

### 1.2 Preview simulation ≠ reality
VCutWorks Preview **systematically differs** from actual CNC runtime. Author manually read values from the machine display — the discrepancy led to developing a custom kinematic model (corner slowdown, plunge overhead, lift time).

### 1.3 LightBurn DXF ≠ AutoCAD DXF
**Most critical finding.** Standard libraries (ezdxf) assume AutoCAD ACI color mapping. LightBurn uses its **own 32-color CAM palette** — e.g., ACI 4 (standard cyan) maps differently. Solution: Euclidean RGB interpolation minimizing (ΔR)²+(ΔG)²+(ΔB)² against a reference palette.

### 1.4 INSERT blocks = up to 50% of geometry
LightBurn DXF stores geometry as block references (INSERT entities). Without block explosion (definition extraction + transform matrix), half the data is lost.

### 1.5 Color-to-layer bit shift mapping
Layers are not explicit in the binary structure — they are derived from color coding. Without this matrix, technological parameters (speed, tool, depth) cannot be correctly assigned.

### 1.6 False length from fixed offset (V10)
Padding float 1.0 interpreted as path length → circle r=500 mm reported as 8 mm. Solution: reconstruct length from point coordinates, not from a fixed offset.

### 1.7 Circle regression +41% (V14)
Color mapping refactored without unit tests → radius 500→707 mm. Circles stored as 4 quadrant arcs, parser read Y-coordinates from unrelated data. Caught by golden master tests.

### 1.8 SNR: 25% of code drives >85% of variance
27+ computation modules classified into Tier 1–5 by predictive value for cutting time. Enabled prioritization.

---

## 2. Methodology (what worked)

| Method | Description | Why it works |
|--------|-------------|--------------|
| **Pair diff** | 2 nearly identical files differing in 1 element → hex diff → format structure | Requires no format knowledge or endianness |
| **Synthetic ground truth** | Trial software + known geometry (rect 2790×1200 mm, circle r=500 mm) | Absolute certainty about input |
| **Physical validation** | Real CNC runtime vs. Preview simulation | Only reliable reference |
| **Golden master** | Baseline JSON → pytest diff | Caught circle regression |
| **Epistemic framework** | Each value: empirical / calibrated / hypothesis | Transparent uncertainty |

---

## 3. Problems and solutions (unique only)

| Problem | Root cause | Solution |
|---------|------------|----------|
| LightBurn ACI divergence | Proprietary 32-color palette instead of standard | Euclidean RGB interpolation |
| INSERT blocks unparsed | DXF references, not direct geometry | Block explosion + transform matrix |
| Preview unreliable | VCutWorks simulation ≠ reality | Physical model + manual calibration |
| Tool assignment conflict | Two logics (ACI vs. geometry) conflict | ACI takes priority, conflict logged |
| Desync (V13) | Do-while loop read padding as elements | Segment-based reading with pt_count |
| PNG viz bugs | Arc center vs. start point; color-by-type vs. layer | Center fix + layer-aware rendering |

---

## 4. Results

| Metric | Value |
|--------|-------|
| Geometry accuracy | >99.98% (deviation <0.02%) |
| Speed match with GUI | 100% |
| Golden master tests | 10/10 PASS |
| Determinism tests | 2/2 PASS |
| Time prediction | ±2–5% vs. real machine |
| Detectable defects | 23 types in 3 classes |
| Savings per defect | 30–200 CZK/job |

---

## 5. LLM role in the RE process

- **5 models:** DeepSeek V4, Gemini, Claude, Groq, ChatGPT
- **Primary tool:** OpenCode CLI with API (DeepSeek + Gemini) — not web UI
- **Cross-validation:** Disagreements between models revealed interpretation errors
- **15+ handoff JSONs:** Machine-readable context between iterations
- **10 Golden Rules:** Determinism, config>code, test-first, epistemic transparency, logging, type hints, version stamping, no magic numbers, blacklist, handoff before break

---

## 6. Implications for the community

### For LightBurn users
- Your DXF export is **NOT compatible** with libraries assuming AutoCAD ACI. For custom processing, implement RGB interpolation against the 32-color LightBurn palette.
- INSERT blocks are standard LightBurn behavior — always implement block explosion when parsing.

### For VCutWorks users
- Preview simulation is unreliable for time prediction. Rely on physical measurement or a custom kinematic model.
- VCF format is readable — pair-wise hex diff is sufficient for structure extraction.

### For RE developers
- **Pair diff** + **clean room** = most efficient path for undocumented binary formats
- **Golden master testing** is not academic — it catches regressions that would surface only in production
- **Epistemic framework** (empirical/calibrated/hypothesis) prevents false certainty for heuristics
- **LLM cross-validation** (multiple models) = cheap way to detect misinterpretation
- **SNR trimming** (25% of code → 85% of variance) = prioritize before perfecting

### For anyone automating CNC workflows
- Transfer learning across domains (waterjet → oscillating knife) works — the kinematic physics model is portable.
- Physical validation is the only meaningful reference. No simulation replaces real measurement.

---

*Published as an open RE case study. Contains methodology and lessons learned — not proprietary format details.*
