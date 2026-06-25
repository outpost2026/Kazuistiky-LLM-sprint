---
title: "Deterministic CAM VCF Format Intelligence — Methodology & Validation Framework"
author: Ondřej Soušek
version: 1.0 (EN)
date: 2026-06
repository: outpost2026/Kazuistiky-LLM-sprint
---

# VCF File Reverse Engineering Intelligence — Methodology & Validation Framework

## 1. Problem & Context

Proprietary binary formats in industrial CNC machines create vendor lock-in, data opacity, and prevent systematic QC analysis. No public parser exists for the `.VCF` format used by Ruida controllers (VCutWorks, RDWorks).

| Tool | Format | VCF Parser | Defect Detection | ERP Integration |
|------|--------|-----------|-----------------|-----------------|
| VcutWorks (Ruida) | VCF native | Yes (closed) | No | No |
| LightBurn | DXF/LBRN | No | No | No |
| **Vcut-Parser** | **VCF** | **Yes (open)** | **20 types** | **Odoo CSV** |

**Market:** 50–150 CZ companies, 500–1000 EU-wide. Barrier to entry: ~200 hours RE + deep CNC domain knowledge.

---

## 2. Reverse Engineering Methodology — 6-Phase Process

### Phase 0: Tacit Knowledge Acquisition
Shadow the operator (9 days on the floor). Capture unwritten rules: color nomenclature, tool behavior, material-specific parameters. Without this, binary numbers lack semantics.

### Phase 1: Synthetic Ground Truth
Create test files with known geometry (rectangle 100×100 mm, circle r=50 mm, diamond) using trial software. If parser returns 100.00×100.01 mm on a known square, accuracy is confirmed.

### Phase 2: Differential Analysis
Pair-wise hex diff of nearly identical files:
1. Create file A with parameter X = value_1, file B with X = value_2
2. `hex_diff(A, B)` → differing bytes = parameter location
3. Iterate for every parameter (color, speed, tool, direction, height)

### Phase 3: Physical Validation
Compare predicted cut time against actual machine time. Tolerance ≤ 10% for B2B use. Calibrate kinematic model (max speed, corner penalty, lift time, material damping).

### Phase 4: Ground Truth Export
Store complete JSON output as "golden master" baselines. 7 baselines for different file types. Proves determinism: same input → identical output.

### Phase 5: Regression Testing
Automated pytest comparing current output against golden master JSONs. 8/8 test categories PASS (smoke, determinism, golden master, geometry, config, binary reader, KB overrides, time predictor).

### Pair Diff Method
```
1. Create file A with X = value_1  
2. Create file B with X = value_2 (everything else identical)  
3. hex_diff(A, B) → list of differing offsets  
4. Identify: offset = where parameter X is stored  
5. Repeat for each parameter
```
Works without knowledge of the format — no need to know endianness.

---

## 3. Epistemic Framework

Each rule carries epistemic metadata:

| Class | Description | Confidence | Example |
|-------|------------|-----------|---------|
| **CLASS_A** | Physical law | 0.99 | "Vibrate cutter must be last layer" |
| **CLASS_B** | Empirical validation | 0.90–0.95 | "H2 = 0.0 mm for 12mm PET felt" |
| **CLASS_C** | Heuristic | 0.80–0.90 | "Small area < 1.67 m² needs tape" |
| **CLASS_D** | Hypothesis | 0.70–0.85 | "Micro-segments < 1 mm = potential defect" |

**SNR Principle:** Value is not in the number of found errors, but in the certainty that a found error = a real physical defect. No warnings = clean drawing. INFO never displayed on screen (prevents alarm overload).

**Epistemic Confidence Index (ECI):** `ECI = empirical_constants / total_constants`. ECI < 0.5 = development phase. ECI > 0.8 = production-ready.

---

## 4. System Architecture

### Pipeline

```
VCF Binary Input → Layer Extraction → Geometry Parsing → Post-Processing → Knowledge Base Validation → Time Prediction → Output (parsed_data)
```

**Layer Extraction:** Magic signature detection, format version, backward search from first geometry, validation (speed 1–2000 mm/s, %5==0, color match).

**Geometry Parsing:** GEOMETRY_SIG scan, type dispatch (Circle/Polygon/Polyline/Line), 74B segment records with IEEE 754 doubles, arc/spline reconstruction, color-to-layer bit shift mapping.

**Post-Processing:** Cut order assignment, canvas bbox, coordinate normalization, material thickness detection, complexity computation, topology tree, ML feature extraction (50+ features).

**Knowledge Base Validation:** Two-layer system:
- Layer 1: Deterministic rules (physics, vacuum, V-groove, cut sequence)
- Layer 2: ML rules (decision tree max_depth=3, case-based reasoning, inverse conditional analysis)
- ML never overrides physics baseline.

**Time Prediction:** `cut_time = Σ(path_length / speed) + N_elements × t_lift + Σ(N_points × t_corner) + curve_penalty + traverse_time + setup_overhead + return_home_time`

**Output:** elements[], layers[], manufacturing_intelligence, operation_sequence, erp_time_prediction, topology_tree, ml_features, canvas_bbox, complexity_index.

---

## 5. Validation & Evidence

| Test | What it verifies | Criterion |
|------|-----------------|-----------|
| `test_smoke.py` | Parser doesn't crash on any input | elements > 0 |
| `test_determinism.py` | Same input = identical output | dictdiff == {} |
| `test_golden_master.py` | Regression protection | Exact JSON match |
| `test_geometry.py` | Geometric utilities | bbox, containment |
| `test_time_predictor.py` | Time prediction | format, predict |

**Results:** 8/8 test categories PASS. All 23 demo files parsed without failure.

### Accuracy

| Metric | Value | Method |
|--------|-------|--------|
| Geometry accuracy | **99.99%** | Validation against LightBurn |
| Element deviation | **< 0.02%** | Path length comparison |
| Total deviation | **< 0.008%** | Aggregate across all elements |
| Time prediction | **± 2–10%** | vs. real machine time |

### Golden Master Principle
```
VCF file → Parser → JSON output → golden_master/baseline.json → pytest diff (any deviation = FAIL)
```
Protected: geometry accuracy, layer correctness, cut ordering, time prediction, warnings. Volatile: file_hash, filename, time format string.

**What this proves:** Determinism (100% reproducibility), accuracy (99.99% geometry, ±2–5% time), regression protection, system integrity, production reliability.

---

## 6. Detection Taxonomy — 23 Defect Types

### Class A: Graphic / Design Errors (caught before cutting)

| # | Code | Description | Severity |
|---|------|------------|----------|
| 1 | EDGE_MERGE_MISSING | Missing edge connection | WARNING |
| 2 | UNCLOSED_LOOP | Unclosed loop gap | INFO–CRITICAL |
| 3 | MICRO_SEGMENT | Segments < 1 mm | WARNING |
| 4 | ZERO_LENGTH_SEGMENT | Zero-length segment | WARNING |
| 5 | SELF_INTERSECTION | Element crosses itself | CRITICAL |
| 6 | DUPLICATE_ELEMENT | Duplicate on same coords | WARNING |
| 7 | SPIKE_DETECT | Sudden direction change > 90° | WARNING |
| 8 | ELEMENT_OVERLAP | Two overlapping elements | WARNING |
| 9 | DEGENERATE_SHAPE | Points on a single line | WARNING |

### Class B: Technological / CNC Errors (prevent physical defects)

| # | Code | Description | Severity |
|---|------|------------|----------|
| 10 | SEQUENCE_LAYER_ERROR | Wrong layer order | CRITICAL |
| 11 | SEQUENCE_NESTING_ERROR | Wrong element order | CRITICAL |
| 12 | VACUUM_FIXATION_RISK | Small area, weak vacuum grip | WARNING |
| 13 | H2_SUBOPTIMAL | Suboptimal tool height | WARNING |
| 14 | NESTING_CLEARANCE | Insufficient clearance | WARNING |
| 15 | TAB_OVERLAP | Clamping tab overlap | WARNING |
| 16 | LAYER_INCONSISTENCY | Inconsistent layer params | WARNING |
| 17 | ORPHAN_ELEMENT | Unassigned element | INFO |
| 18 | ASYMMETRIC_PAIR | Asymmetric pair (symmetric designs) | INFO |
| 19 | NEAR_MISS_GAP | Gap < 0.1 mm | INFO |

### Class C: NC Code / Post-Process Errors

| # | Code | Description | Severity |
|---|------|------------|----------|
| 20 | COLOR_MAP_MISMATCH | Color doesn't match known layer | WARNING |
| 21 | AGGREGATED_JOB | Multiple panels in one file | INFO |
| 22 | UNKNOWN_VERSION | Unknown format version | WARNING |
| 23 | CORRUPT_GEOMETRY | Invalid coordinates | CRITICAL |

### Visual Overlay Methodology (HUD-inspired)
- Overlay shown ONLY when warnings exist. Clean drawing = no overlay.
- Max 3 warning types per object (Miller's Law).
- Only 2 levels displayed: CRITICAL (#F43F5E) and WARNING (#F59E0B). INFO never shown.

### ROI Quantification
| Parameter | Value |
|-----------|-------|
| Cost per defect | 500–5,000 CZK |
| Detectable defects | ~50% |
| Savings per job | 30–200 CZK |
| Annual savings (small shop) | 30,000–200,000 CZK |
| Parser cost (one-time) | 60–80K CZK |
| ROI | 1–3 saved jobs = parser paid |

---

## 7. Transferable Methodology

### Five Principles (inspired by Tomas Mikolov)

1. **Compression as structure extraction:** Descriptor vectors (5–20 numerical features) instead of raw data. Enables cosine similarity comparison, decision tree classification, cross-format transfer.

2. **Simple, interpretable models:** Decision tree (max_depth=3, ~94% accuracy) over deep neural networks (~95%). Interpretable, fast (ms), no large dataset needed.

3. **First principles before statistics:** Apply all physical/geometric constraints first. Add ML only where deterministic rules fall short. ML NEVER overrides physics.

4. **Novelty search / continuous learning:** Novelty buffer (10 deviations) → trigger → auto-retrain → validate on golden master → deploy if PASS / rollback if FAIL.

5. **Emergence from simple rules:** Complex behavior from atomic rule combinations. No "super-intelligent" rule — just simple ones combined.

### Transferable Artifacts
| Artifact | Description | Implementation time |
|----------|------------|-------------------|
| Descriptor generator | Numerical vectors from geometry | 2–5 days |
| Decision tree trainer | Train classifier on data | 1 day |
| Case-based reasoning | Find similar historical cases | 0.5 day |
| Novelty buffer | Track deviations, trigger retraining | 1 day |

### EROI Framework (Effort Return on Investment)
| Iteration | EROI | Effort | Description |
|-----------|------|--------|-------------|
| 0 (Hygiene) | High | 2–3 h | Logging, remove `except: pass` |
| 1 (Testing) | Critical | 4–6 h | Golden master, determinism |
| 2 (Dedup) | High | 8–12 h | Remove duplicate code |
| 3 (Modules) | Medium | 12–16 h | Separate parser, geometry, prediction |
| 4 (Production) | Medium | 4–6 h | Docker, GCP, monitoring |
| 5 (CI/CD) | Low | 6–8 h | Auto tests on commit |

### LLM Interaction Protocol
LLM is an autonomous microservice for code transformation, not a conversational partner. LLM writes: Python logic for config loading, Streamlit UI. LLM does NOT write: detection statistics, epistemic framework changes. LLM is a tool, not the architect. The architect decides which anomalies are acceptable.

---

## Conclusion

This methodology enables:

1. **Systematic decoding** of proprietary binary formats via a structured 6-phase process
2. **Accuracy validation** through golden master tests and physical calibration
3. **Epistemic documentation** of every parameter (CLASS_A–D)
4. **Proof of determinism** (8/8 tests PASS, 99.99% accuracy)
5. **Cross-format transferability** (DXF, PLT, LBRN)

**Key principle:** Transparency creates trust. Not "our parser is the best" — but "here is the methodology, here are the tests, here are the results."
