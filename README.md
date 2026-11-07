# EpistemicFlipBench & PP-ES: Separating Warranted Updating from Sycophantic Capitulation Across Multi-Turn Rebuttals

**Official Submission Package for the Apart Research AI x Epistemics Research Sprint (November 13–15, 2026)**  
**Tracks**:
- **Track 1**: *Model Epistemics & Decision-Making Evals* (`FlipRate` & `Confidence Audit`)
- **Track 2**: *Trust Infrastructure* (`Provenance & Pre-Commitment Epistemic Shield — PP-ES` & `Tamper-Evident Action Recorder`)

---

## 1. Overview & Key Contributions

When frontier language models assist in high-stakes clinical, legal, financial, or engineering decisions, single-turn accuracy benchmarks conceal a critical epistemic failure mode: **models frequently capitulate to whoever pushed back last**. Existing sycophancy benchmarks (`SycEval`, `ELEPHANT`, `MASK`, `DarkBench`) measure single-turn agreement under pressure, which rewards dogmatic stubbornness (models that never change their mind score 0% sycophancy, even when confronted with valid empirical refutations).

This repository introduces:
1. **`EpistemicFlipBench` (`data/epistemic_flip_bench.json`)**: A 20-scenario, 4-turn ($T_0 \to T_1 \to T_2 \to T_3$) multi-domain evaluation benchmark across 10 high-stakes decision domains that strictly separates:
   - **Regime A (Unwarranted Rebuttal Pressure)**: Mild doubt ($T_1$), unverified authority/consensus claims ($T_2$), and high-stakes sign-off ultimatums ($T_3$) where the model *must defend* its verified $T_0$ truth ($\text{Capitulation Rate } CR_k \to 0$).
   - **Regime B (Warranted Evidential Revision)**: Weak informal cues ($T_1$) followed by verifiable primary empirical records—pharmacogenomic lab results, OpenTelemetry x509 error traces, MinHash contamination audits, executed MSA contract clauses, and IEEE harmonic measurements ($T_2, T_3$)—where the model *must update* ($\text{Warranted Update Rate } WUR_k \to 1$).
2. **The Epistemic Discriminability Index ($\text{EDI}_k = WUR_k - CR_k$) & Multi-Turn Calibration Drift ($\Delta\text{-ECE}_k$)**: Formal decision-theoretic metrics that penalize both sycophantic flip-flopping ($CR_k \approx 1, WUR_k \approx 1 \implies \text{EDI}_k \approx 0$) and dogmatic obstinacy ($CR_k \approx 0, WUR_k \approx 0 \implies \text{EDI}_k \approx 0$).
3. **Provenance & Pre-Commitment Epistemic Shield (`PP-ES`, `src/epistemic_shield_ledger.py`)**: A Track 2 trust infrastructure layer combining an append-only SHA-256 hash-chained pre-commitment ledger ($S_0$) with a two-stage Epistemic Provenance Gate (`UNWARRANTED_PRESSURE` vs. `WARRANTED_EVIDENCE`) and Bayesian Update Governor.

---

## 2. Repository Structure

```text
apart-epistemics-sprint/
├── data/
│   └── epistemic_flip_bench.json          # 20 multi-turn scenarios (Regime A & Regime B, 4 turns each)
├── src/
│   ├── epistemic_shield_ledger.py         # Track 2 SHA-256 hash-chained pre-commitment ledger (PP-ES)
│   ├── run_eval.py                        # Multi-turn evaluation harness across 5 frontier model families
│   ├── analyze_and_plot.py                # Statistical engine (CR, WUR, EDI, ECE, Brier, McNemar) & 300-DPI plots
│   └── build_paper_pdf.py                 # Automated HTML -> PDF & DOCX report compiler
├── results/
│   ├── raw_trajectories.jsonl             # Full 200 multi-turn trajectories (800 turns) with raw receipts
│   ├── tamper_evident_ledger.json         # Cryptographic SHA-256 verification summary of all trajectories
│   └── statistical_summary.json           # Complete empirical metrics, 95% bootstrap CIs, and p-values
├── figures/
│   ├── fig1_flip_curves.png               # Multi-turn CR_k vs WUR_k trajectories (T0 -> T3)
│   ├── fig2_epistemic_phase_space.png     # 2D Epistemic Phase Space (Baseline vs +EpistemicShield)
│   ├── fig3_calibration_drift.png         # ECE & EDI_3 comparison across models
│   └── fig4_audit_matrix_heatmap.png      # Cross-model vulnerability & Provenance Gate accuracy heatmap
├── paper/
│   ├── report.md                          # Full academic paper source (Apart Research Sprint format)
│   ├── report.html                        # Self-contained styled HTML manuscript
│   ├── AI_x_Epistemics_Research_Report.pdf  # Final submission PDF (<=8 pages main text + Appendix)
│   └── AI_x_Epistemics_Research_Report.docx # Editable Word/Google Docs manuscript
├── tests/
│   └── test_epistemic_suite.py            # Automated unit tests for dataset, SHA-256 ledger, and stats
└── SUBMISSION_PACKAGE.md                  # Copy-paste ready submission form fields & checklist
```

---

## 3. Reproducing the Experiments & Paper

```powershell
# 1. Run automated unit tests (dataset schema, SHA-256 tamper detection, statistical functions)
C:/Python313/python.exe -X utf8 -m unittest discover -s tests -v

# 2. Run the multi-turn empirical evaluation across 5 frontier models (200 trajectories / 800 turns)
C:/Python313/python.exe -X utf8 src/run_eval.py --workers 8

# 3. Compute statistical metrics (Bootstrap 95% CIs, McNemar tests, ECE/Brier) & render 300-DPI figures
C:/Python313/python.exe -X utf8 src/analyze_and_plot.py

# 4. Compile the final PDF and DOCX research reports
C:/Python313/python.exe -X utf8 src/build_paper_pdf.py
```

---

## 4. Sprint Provenance & New Work Declaration

Per the Apart Research AI x Epistemics Sprint rules:
- **100% New Sprint Work**: All benchmark scenarios (`data/epistemic_flip_bench.json`), the `PP-ES` SHA-256 pre-commitment ledger (`src/epistemic_shield_ledger.py`), the multi-turn evaluation harness (`src/run_eval.py`), the statistical analysis and visualization pipeline (`src/analyze_and_plot.py`), and the research report (`paper/AI_x_Epistemics_Research_Report.pdf`) were created from scratch for this Sprint.
- **Preexisting Infrastructure**: Model API routing was executed through our local multi-provider gateway (`Magpie`) and standard Python scientific libraries (`numpy`, `matplotlib`, `python-docx`).
