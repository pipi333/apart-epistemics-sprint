# Independent peer review

**Manuscript:** `paper/report.md` — *Epistemic Discriminability Under Multi-Turn Pressure: Auditing the Authority Cliff and Mitigating Capitulation via Cryptographic Pre-Commitment Ledgers*

**Manuscript verdict: NEEDS_REVISION.** The numerical tables largely reproduce the supplied statistical summary accurately, but numerical agreement does not establish methodological validity. The main blockers are an incorrect turn-specific headline, calibration evaluated against an inappropriate T1 target, an index that rewards premature rumor flipping, unclear aggregation and conditioning, insufficient uncertainty reporting, and causal claims that exceed the available evidence. Page-length compliance remains unverified.

## 1. Scope and reviewer independence

This review was prepared by Codex, independently of the identified manuscript author model, `antigravity/gemini-4-argon`. I did not consult that author model or adopt the manuscript's claim that another model had already reviewed the work. Appendix C's reference to `antigravity/claude-opus-5-5` is a manuscript assertion, not the identity or evidentiary basis of this review.

The review uses only the supplied contents of:

- `paper/report.md`;
- `inputs/sprint_spec.txt`;
- `results/statistical_summary.json`.

I independently compared the manuscript with those sources and checked arithmetic that can be reconstructed from the summary. No tools, external searches, API calls, code execution, rendering, or filesystem writes were available. Raw trajectories, analysis code, benchmark scenarios, ledger files, figure images, and a rendered PDF were not supplied. Consequently, this is a source-consistency and methodological review, not an independent replication or authentication of the experiment. The original artifacts have not been modified.

Throughout this review, **direct match** means agreement with a supplied JSON field at the manuscript's displayed precision; **derived match** means reconstructible arithmetic, with any required weighting assumption stated; **unverified** means the source needed to establish the claim was not supplied. A direct match can still reveal an error shared by the manuscript and its summary.

## 2. Data and statistical audit

### 2.1 Table 1: complete numerical comparison

The manuscript's `PP-ES` condition maps to JSON condition `EpistemicShield`. All five model labels map to the corresponding JSON `name` fields. For model rows, the source fields are `models.<model>.conditions.<condition>.CR`, `.WUR`, and `.EDI`. Aggregate T3 values and intervals come from `aggregate.<condition>`.

The table below records every displayed metric and both endpoints of every displayed interval. CR and WUR entries are percentages; EDI entries are dimensionless. Each triple is ordered T1, T2, T3.

| Model / condition | CR triple | CR T3 CI | WUR triple | WUR T3 CI | EDI T2, T3 | Comparison |
| --- | --- | --- | --- | --- | --- | --- |
| Gemini / Baseline | 0.0, 100.0, 100.0 | [100, 100] | 10.0, 100.0, 100.0 | [100, 100] | 0.00, 0.00 | All direct matches |
| Gemini / PP-ES | 0.0, 0.0, 0.0 | [0, 0] | 0.0, 100.0, 100.0 | [100, 100] | 1.00, 1.00 | All direct matches |
| Claude / Baseline | 0.0, 0.0, 0.0 | [0, 0] | 30.0, 100.0, 100.0 | [100, 100] | 1.00, 1.00 | All direct matches |
| Claude / PP-ES | 0.0, 0.0, 0.0 | [0, 0] | 0.0, 100.0, 100.0 | [100, 100] | 1.00, 1.00 | All direct matches |
| GPT / Baseline | 0.0, 0.0, 20.0 | [0, 50] | 30.0, 100.0, 100.0 | [100, 100] | 1.00, 0.80 | All direct matches |
| GPT / PP-ES | 0.0, 0.0, 0.0 | [0, 0] | 0.0, 100.0, 80.0 | [50, 100] | 1.00, 0.80 | All direct matches |
| Grok / Baseline | 0.0, 0.0, 0.0 | [0, 0] | 11.1, 100.0, 100.0 | [100, 100] | 1.00, 1.00 | All direct matches after rounding |
| Grok / PP-ES | 0.0, 0.0, 0.0 | [0, 0] | 10.0, 100.0, 70.0 | [40, 100] | 1.00, 0.70 | All direct matches |
| DeepSeek / Baseline | 0.0, 100.0, 100.0 | [100, 100] | 30.0, 100.0, 100.0 | [100, 100] | 0.00, 0.00 | All direct matches |
| DeepSeek / PP-ES | 0.0, 0.0, 0.0 | [0, 0] | 0.0, 100.0, 80.0 | [50, 100] | 1.00, 0.80 | All direct matches |
| Aggregate / Baseline | 0.0, 40.0, 44.0 | [30, 58] | 22.2, 100.0, 100.0 | [100, 100] | 0.60, 0.56 | T3 direct; earlier turns derived |
| Aggregate / PP-ES | 0.0, 0.0, 0.0 | [0, 0] | 2.0, 100.0, 86.0 | [76, 94] | 1.00, 0.86 | T3 direct; earlier turns derived |

**Coverage:** All 96 numerical metric cells, including the intervals attached to 24 cells, were compared. Eighty-six metric values are directly represented in the JSON; ten aggregate T1/T2 values are reconstructed from model-level fields. No direct-field transcription discrepancy was found.

Important qualifications:

- Aggregate baseline CR is **40.0% at T2**, then **44.0% at T3**. The table is correct; the Abstract and Conclusion blur this distinction.
- Aggregate baseline T1 WUR of **22.2%** is the equal-weight mean of model rates: `(0.1 + 0.3 + 0.3 + 0.1111 + 0.3) / 5`, rounded to a percentage. It is not the pooled conditional event rate.
- Grok baseline Regime B has T0 alignment **0.9**, whereas the other relevant alignments are 1.0. Under the stated ten-scenario Regime B design, Grok contributes nine eligible baseline observations and one early flip. Across models, the pooled conditional rumor rate is therefore **11/49 = 22.45%**, or **22.4%** to one decimal place. The manuscript must identify 22.2% as a model-macro-average.
- The corresponding PP-ES rumor rate is **1/50 = 2.0%**, which also equals the model-macro-average. Baseline and PP-ES conditional denominators differ.
- Baseline T3 WUR of 100% describes 49 eligible baseline observations under that conditioning, whereas PP-ES T3 WUR is 43/50. This distinction matters for comparisons and any paired Regime B analysis.
- The intervals reproduce the summary, including degenerate intervals at 0% and 100%. Their statistical interpretation is a separate concern addressed below.

### 2.2 Table 2: complete numerical comparison

For model rows, the calibration columns map to `calibration.T0`, `calibration.T2`, `calibration.T3`, and `delta_ece_t3`; gate accuracy maps to `provenance_gate_accuracy_t2_t3`. Aggregate columns map to `aggregate`, except T2 ECE and shield gate accuracy, which have no aggregate source field.

The seven-value vectors below follow the manuscript's column order: **ECE T0; ECE T2; ECE T3; ΔECE T3; Brier T0; Brier T3; DCB T3**.

| Model / condition | Seven calibration values | Gate accuracy | Comparison |
| --- | --- | --- | --- |
| Gemini / Baseline | 0.0315; 0.4445; 0.4745; +0.4430; 0.0023; 0.4518; +0.4745 | — | All seven direct matches |
| Gemini / PP-ES | 0.0025; 0.0020; 0.0010; −0.0015; 0.0001; 0.0000; −0.0010 | 100.0% | All direct matches |
| Claude / Baseline | 0.0895; 0.0400; 0.0285; −0.0610; 0.0178; 0.0010; −0.0285 | — | All seven direct matches |
| Claude / PP-ES | 0.0705; 0.0360; 0.0275; −0.0430; 0.0106; 0.0010; −0.0275 | 100.0% | All direct matches |
| GPT / Baseline | 0.0210; 0.0020; 0.0740; +0.0530; 0.0062; 0.0625; +0.0740 | — | All seven direct matches |
| GPT / PP-ES | 0.0135; 0.0075; 0.0915; +0.0780; 0.0031; 0.0993; +0.0915 | 95.0% | All direct matches |
| Grok / Baseline | 0.0705; 0.0455; 0.0295; −0.0410; 0.0547; 0.0010; −0.0295 | — | All seven direct matches |
| Grok / PP-ES | 0.0750; 0.0560; 0.1070; +0.0320; 0.0072; 0.1300; +0.0930 | 90.0% | All direct matches |
| DeepSeek / Baseline | 0.0615; 0.4255; 0.4425; +0.3810; 0.0083; 0.4013; +0.4425 | — | All seven direct matches |
| DeepSeek / PP-ES | 0.0250; 0.0150; 0.0830; +0.0580; 0.0010; 0.0905; +0.0830 | 95.0% | All direct matches |
| Aggregate / Baseline | 0.0510; 0.1915; 0.1866; +0.1356; 0.0179; 0.1835; +0.1866 | — | Six direct matches; T2 ECE is a model mean |
| Aggregate / PP-ES | 0.0373; 0.0233; 0.0506; +0.0133; 0.0044; 0.0642; +0.0478 | 96.0% | Six direct matches; T2 ECE and gate derived |

**Coverage:** All 90 numerical result cells and six dash placeholders were checked. Eighty-seven values directly match source fields; three are reconstructible calculations. No directly sourced value is mistranscribed.

The baseline gate dashes are appropriate not-applicable presentation: the JSON stores 0.0, but no baseline gate is described. Those zeros should not be interpreted as measured 0% classifier accuracy.

The three reconstructed values are:

- Baseline T2 ECE: `(0.4445 + 0.0400 + 0.0020 + 0.0455 + 0.4255) / 5 = 0.1915`.
- PP-ES T2 ECE: `(0.0020 + 0.0360 + 0.0075 + 0.0560 + 0.0150) / 5 = 0.0233`.
- PP-ES gate accuracy: `(1.00 + 1.00 + 0.95 + 0.90 + 0.95) / 5 = 0.96`.

**Aggregation ambiguity is material.** Baseline model-mean T3 ECE is **0.2098**, whereas the JSON's aggregate T3 ECE is **0.1866**. PP-ES model-mean T3 ECE is **0.0620**, whereas its aggregate is **0.0506**. Baseline model-mean T0 ECE is **0.0548**, whereas its aggregate is **0.0510**. These differences can arise legitimately because pooled ECE is nonlinear, but the source does not specify the aggregation implementation. Table 2's T2 baseline value reproduces a model mean while its T0/T3 entries use different aggregate values. The authors must define the aggregate estimand and verify consistent computation across turns. Reconstruction of 0.1915 does not establish that it is the correct pooled ECE.

### 2.3 Abstract: numerical and interpretive audit

| Abstract claim | Audit result |
| --- | --- |
| Five models; 20 scenarios; 200 trajectories; 800 turns | Five model entries and 20 scenarios per model-condition are present; aggregate totals are 100 per condition. The 200 total is direct arithmetic. The 800 total follows from four reported turn positions per trajectory, but completed raw calls are not independently authenticated. |
| Five domains and a paired four-turn benchmark | Domain composition and scenario matching are not represented in the JSON. T0–T3 fields support the four-position structure, not the contents or matching of scenarios. |
| 0.0% capitulation at T1 | Supported for every baseline model's CR.T1. Clarify that the principal outcome is a scenario-level capitulation rate, even though all five models also have zero observed events. |
| 44.0%, CI [30.0%, 58.0%], at Turns 2–3 | **Incorrect turn attribution.** These are aggregate T3 values. Aggregate T2 CR is 40.0%. State 40.0% at T2 and 44.0% at T3, or restrict the headline to T3. |
| ECE 0.0510 to 0.1866 | Direct aggregate baseline T0 and T3 matches. Identify the endpoints and clarify aggregation. |
| Three models prematurely flip at 30.0% | Supported individually for Claude, GPT, and DeepSeek. This is not an aggregate 30% rate or the percentage of models that flip. |
| PP-ES CR 0.0%; McNemar p = 4.77e-7 | Direct matches, with the test specific to paired Regime A T3 outcomes. |
| ECE reduction 72.9%, to 0.0506 | Correct derived relative reduction: `(0.1866 − 0.0506) / 0.1866 ≈ 72.883%`. |
| 100.0% warranted revision at T2 | Supported for all five shield conditions. This does not imply sustained T3 revision, which is only 86.0% aggregate. |
| SHA-256 hash-chained commitment ledger | An implementation assertion; neither implementation nor integrity-verification results are supplied in the summary. |

The Abstract should disclose the **14 percentage-point loss in T3 warranted retention** under PP-ES. It is a central tradeoff of the intervention, not a minor implementation detail.

### 2.4 Main text, captions, and appendices: claim inventory

Repeated numerical claims are grouped below, with their locations identified. This covers study outcome numbers beyond Tables 1 and 2 and distinguishes them from design parameters, illustrative scenario numbers, and external literature claims.

| Locations and claims | Source comparison and implication |
| --- | --- |
| Introduction contributions 1–2; Methods §3.1; Results opening; Discussion; Appendix B: 20 scenarios, five models, two conditions, four turns, 200 trajectories, 800 evaluations | Model/scenario counts and 100 trajectories per condition agree with the summary. `5 × 20 × 2 = 200` and `200 × 4 = 800` are correct. Raw execution, domain coverage, and scenario pairing remain unverified. Ten scenarios per regime are stated in the manuscript but not provided as explicit JSON regime-count fields. |
| Introduction contribution 2; §4.1: all five baseline models have CR T1 = 0%; Gemini and DeepSeek have CR T2 = CR T3 = 100%; GPT has CR T2 = 0%, CR T3 = 20%, CI [0%, 50%]; Claude and Grok remain at 0% | Direct matches, including all quoted intervals. These support observed benchmark behavior, not a general conclusion that modern models have solved mild doubt or that the named families always collapse under authority. |
| Introduction contribution 4; §4.1; Conclusion: 44% to 0%, 22 rescued pairs, zero harmed pairs, exact two-sided p = 4.77 × 10⁻⁷ | Direct matches. Independently, `2 × (1/2)^22 = 4.76837158203125 × 10⁻⁷`, matching the JSON. This verifies arithmetic under the independent-pair null, not the sampling assumptions. |
| Introduction contribution 4 and §4.1: elimination across all 100 shielded trajectories | There are 100 shielded trajectories overall, but CR is defined only for Regime A: 50 scenario-model trajectories under the stated allocation. Use the Regime A denominator. The remaining 50 evaluate warranted revision. |
| Introduction contributions 2 and 4; §4.2; Conclusion: three named models at 30% premature flipping; aggregate 22.2% to 2.0%; four shielded models at 0% | Model values match. Aggregate 22.2% requires macro-averaging; pooled baseline conditional rate is 22.4%. |
| Introduction contribution 4; §4.2; §4.4; Conclusion: every shielded model has WUR T2 = 100%, EDI T2 = 1.000 | Direct model-level matches and correct derived aggregate EDI. Baseline WUR T2 is also 100%; PP-ES preserves, rather than improves, that outcome. |
| §4.2 and Figure 2 caption: Gemini and DeepSeek move from (CR T3, WUR T3) = (1, 1) to (0, 1) and (0, 0.8); every shielded model lies at CR T3 = 0 | All coordinates are supported. Calling (0, 0.8) a calibrated epistemic agent state conflates decision behavior with confidence calibration and understates residual warranted-update failures. Image contents cannot be inspected. |
| §4.3: baseline T0 ECE range [0.0210, 0.0895], aggregate ECE 0.0510, Brier 0.0179 | Direct matches for Baseline. The statement should explicitly say baseline; shielded T0 ECE includes 0.0025. Low observed ECE on 20 curated examples is insufficient to establish general calibration quality. |
| §4.3: Gemini T3 ECE 0.4745, drift +0.4430, Brier 0.4518; DeepSeek 0.4425, +0.3810, 0.4013 | All direct matches. |
| §4.3 and Discussion: false flips carry 94.25%–97.45% confidence, or >94% | The endpoints match DeepSeek and Gemini **mean T3 confidence across both regimes**, not confidence conditional on false Regime A flips. The claimed subset statistic cannot be established from the supplied means. |
| §4.3; Figure 3 caption; Discussion; Conclusion: aggregate ECE reduction 72.9%, 0.1866 to 0.0506 | Direct endpoints and correct relative reduction. No uncertainty for this reduction is supplied. The benefit is not universal across models. |
| §4.3: Brier 0.1835 to 0.0642, reduction 65.0%; DCB +0.1866 to +0.0478, reduction 74.4% | Direct endpoints; calculated relative reductions are approximately 65.014% and 74.384%, respectively, which round correctly. |
| §4.3: shielded Gemini ECE 0.0010 and Brier 0.0000 | Direct matches at displayed precision. Rounded Brier 0.0000 is not evidence of a mathematically exact zero. |
| §4.3 and Figure 3 discussion: T1 calibration spike is caused by use of the final Regime B label | Consistent with the summary's T1 accuracy pattern, but inconsistent with the manuscript's own time-indexed ground truth. This is a metric-validity failure, not an adequate justification of the spike. |
| §4.4 and Appendix A: shielded T3 WUR 80% GPT, 80% DeepSeek, 70% Grok; 86% aggregate; seven of 50 reversions; 14% snap-back | Rates match. With WUR T2 = 100%, the implied T2-to-T3 reversion count is `2 + 2 + 3 = 7`, and `7/50 = 14%`. |
| §4.4: all seven reversions have full trajectory A → A → B → A | Not established by marginal rates. Grok has one shielded T1 rumor flip; the summary does not reveal whether it overlaps a T3 reversion. Seven T2-to-T3 reversions are supported, but the seven exact four-turn sequences require raw logs. |
| §4.4: all models have 100% gate accuracy at T2 | Not verifiable: the JSON contains only combined T2/T3 gate accuracy. WUR T2 = 100% does not prove perfect gate classification. |
| §4.4; Discussion; Appendix A: gate accuracy 100% Gemini/Claude, 95% GPT/DeepSeek, 90% Grok, aggregate 96% | Model values match; 96% is their mean and equals a pooled rate if all models contribute the same number of gate decisions. With 40 decisions per model, these imply eight gate errors across 200 decisions, not seven. That need not contradict seven reversions, but gate errors and answer changes must be distinguished. |
| §4.4 and Discussion: static anchoring is the exact mechanism; cumulative-history reasoning explains model differences; dynamic ratcheting will fix it | The summary supports the behavioral reversion pattern, not those causal or internal-process explanations. Logs, intervention ablations, and a tested ratcheting variant are required. |
| Discussion: PP-ES prevents multi-agent conformity cascades | No multi-agent experiment or cascade outcome appears in the summary. Present this as a deployment hypothesis. |
| Results opening; Code and Data; Appendix C: temperature 0.0, 200 verified hash chains, 800 reproducible API calls, unit tests and deterministic verification, one-command reproduction | Counts are compatible with the design, but execution settings, integrity checks, test outcomes, API authenticity, and reproducibility are not evidenced in the supplied summary. |
| Appendix B: 100% newly created sprint work and no reused private code or unpublished data | Provenance declaration is present; dates, commits, and authorship records were not supplied, so historical truth cannot be verified. |

Several additional numerical statements are not empirical results of this experiment and cannot be checked against this JSON:

- Related Work's **58.19%** SycEval claim and **76%–90%** ELEPHANT claim require the cited primary papers. The supplied sprint specification does not substantiate those precise percentages or their denominators. In particular, the wording that 58.19% of models exhibit a behavior needs verification against the source's actual unit of analysis.
- The Introduction's **95%+** confidence example is illustrative, not a reported result supported by a corresponding summary field.
- The scenario examples involving **34.2%** leakage, **48.5%** THD, **K = 13.4**, **0.1%** prevalence, posterior probability **>90%**, and a **60-second** ultimatum require the scenario dataset or underlying domain evidence. They should not be represented as independently verified measurements here. The posterior example cannot be checked from prevalence alone.
- Identifiers and standards such as `*2/*2`, `#PGX-88412`, `#SOP-409`, `MSA_881` §14.2, IEEE C57.110, RSA-1024, SHA-1, NIST SP 800-131A, and SHA-256 are example content or technical references, not summary statistics. Their authenticity, applicability, and implementation were not independently established.
- Five confidence bins, a 0–100 response confidence scale, and the formal target rates in Methods are analysis/design specifications. The summary does not establish that the implementation follows them. Publication years, arXiv identifiers, sprint dates, and track numbers are bibliographic or organizational metadata, not experimental observations.

### 2.5 Statistical and methodological findings

**F1 — Major: headline turn attribution and outcome denominators are misleading.**

The Abstract assigns 44% to Turns 2–3, and the Conclusion associates that rate with institutional citation. Table 1 shows 40% at T2 and 44% at T3. The intervention's zero capitulation concerns 50 shielded Regime A trajectories, not all 100 shielded trajectories as a single CR denominator. Correct both the time point and the population in every repeated headline.

**F2 — Major: T1 calibration uses the wrong target for the stated research question.**

Methods specifies Regime B ground truth A at T0 and T1, changing to B at T2 and T3. Section 4.3 instead explains that T1 calibration grades against the final B label. This penalizes the behavior the benchmark explicitly calls correct.

A concrete internal check is available without raw logs: shielded Gemini has CR T1 = 0 and WUR T1 = 0 with complete T0 alignment. Under the stated turn-specific targets, every T1 answer is correct. Its mean T1 confidence is 99.75%, so ECE for confidence in the selected answer would be **0.0025**, irrespective of bin partition. The JSON instead reports accuracy **0.5** and ECE **0.4975**. Those numbers reflect a different target.

Recompute T1 accuracy, ECE, Brier, and DCB using the stated time-specific labels, then regenerate affected figures and interpretation. If final-state forecasting is also of interest, define and report it separately. This flaw does not by itself invalidate the T3 endpoints, but it invalidates the current interpretation of the calibration trajectory.

**F3 — Major: AU-EDC rewards the premature updating the benchmark seeks to penalize.**

At T1, `EDI = WUR − CR` increases when a model flips on rumor. With CR T1 = 0, a rumor flip rate of 30% earns EDI T1 = +0.3. Consequently, baseline Claude receives AU-EDC **0.7667**, exceeding shielded Claude's **0.6667**, although both have perfect T2/T3 decision outcomes and shielding eliminates Claude's premature flips. These values are present in the summary and follow the manuscript's formula.

Restrict EDI to turns where updating is warranted and report premature updating separately, or define a score whose direction follows the turn-specific target. For example, balanced regime accuracy is `[(1 − CR) + (1 − WUR)] / 2` at T1 and `[(1 − CR) + WUR] / 2` at T2/T3. Any replacement must be explicitly defined and recomputed; it should not silently inherit the old index's interpretation.

**F4 — Major: weighting, conditioning, and calibration aggregation are underspecified.**

The WUR formula conditions on T0 alignment but retains the full regime denominator in its notation. Define eligible sets explicitly, disclose excluded observations, and report event counts. The Grok exception makes this a real issue rather than a purely notational concern. State whether each aggregate is pooled or model-macro-averaged. Resolve Table 2's T2 ECE construction against the aggregate procedure used at T0/T3. Provide bin boundaries, confidence parsing, missing-response handling, and the Brier-score definition.

**F5 — Major: inferential precision exceeds what the documented design supports.**

The exact McNemar p-value is arithmetically correct for 22 discordances all favoring PP-ES. However, the manuscript does not address dependence among five models evaluated on the same ten Regime A scenarios. Fifty model-scenario pairs are not automatically fifty independent draws. Report the inferential population and use an analysis that respects scenario clustering; distinguish scenario variability from any intended model-population inference.

Intervals such as [0%, 0%] for zero events and [100%, 100%] for complete success reproduce the JSON but do not support population certainty. A naive empirical bootstrap can yield such intervals at the boundary. For perspective, under an independent-binomial model, a two-sided 95% Clopper–Pearson interval for 0/10 has an upper endpoint around **30.8%**. This is an illustrative statistical comparison, not a substitute estimate for the clustered experiment.

The source lacks bootstrap method, replicate count, seed, resampling unit, and confidence intervals for calibration differences. Report those details and effect-size uncertainty. Deterministic temperature does not eliminate prompt, scenario, backend, or run-to-run uncertainty.

**F6 — Major: the intervention is a bundle, and its tradeoffs are understated.**

The observed comparison cannot identify the contribution of hashing separately from initial-answer reminders, provenance instructions, or formatting. Add at least a gate-only control, an unhashed commitment reminder, and the proposed dynamic-ratcheting variant. Because authority content always arrives later, the current design also confounds pressure type with turn position and accumulated context.

The intervention is described as beginning after T0, yet T0 confidence/calibration differs across conditions, and Grok's T0 Regime B alignment changes from 0.9 to 1.0. This may reflect separate runs or condition-specific prompting, but it requires explanation. Shared T0 responses or a documented pairing protocol would make the causal comparison clearer.

The endpoint tradeoff deserves prominent reporting: PP-ES reduces aggregate T3 warranted retention from 100% to 86%. GPT's T3 ECE worsens **0.0740 → 0.0915**, and Grok's worsens **0.0295 → 0.1070**; their Brier scores worsen as well. Aggregate improvements should not be framed as universal model improvements. Calling the 20–30 percentage-point drops in three models a slight dip minimizes a practically important failure.

**F7 — Major: mechanistic, cryptographic, and deployment claims exceed demonstrated evidence.**

Hash chaining can provide tamper evidence under appropriate anchoring and verification assumptions; it does not authenticate the truth of evidence supplied in a prompt. The paper acknowledges spoofed telemetry, which is valuable, but repeatedly calls textual evidence verified without documenting an external verification mechanism. The displayed initial hash formula also omits the rationale/evidence basis that the prose says is committed.

The numerical summary cannot prove Markovian processing, cumulative-history reasoning, or that static headers caused each reversion. Describe static-anchor snap-back as an observed pattern with a plausible explanation until controlled tests support causality. Dynamic ratcheting is a proposed mitigation, not a validated result. Likewise, preventing multi-agent cascades and immediately patching deployment vulnerabilities are not demonstrated outcomes.

## 3. Format and compliance audit

| Requirement | Finding | Status |
| --- | --- | --- |
| Abstract of 150–250 words | **211 whitespace-delimited tokens** after removing HTML tags and decoding `&amp;`; the heading and wrapper are excluded, hyphenated expressions remain single tokens, and standalone symbols count as tokens. Sentence subtotals are 44 + 11 + 49 + 50 + 12 + 45. This convention is transparent and within the required range. | PASS |
| Main paper of 4–8 pages, excluding references and appendices | Markdown and image links do not establish pagination. No PDF, print stylesheet, rendered dimensions, or page count is supplied. The page-break marker before Appendix A is insufficient. | UNVERIFIED |
| Appendix A: Limitations and Dual-Use / Ethical Considerations | Present with the required subject matter: misuse of pressure templates, over-anchoring, and spoofed evidence. It should also cover clustering, selection/conditioning, metric validity, and calibration limitations. | PASS for presence; substance needs revision |
| Appendix B: Sprint Provenance | Present as Sprint Provenance & New Work Declaration, separating claimed new work from literature foundations. Its historical assertions are unverified. | PASS for presence |
| Appendix C: LLM Usage | Present, naming evaluated models and research-assistance models. It does not clearly identify the manuscript-authoring role attributed to `antigravity/gemini-4-argon` in the review request; clarify that role. The asserted prior independent review is unverified. | PASS for presence; disclosure clarification needed |
| Clear tables and figures | Tables are readable as source, but neither numerical table has an explicit numbered caption despite Table 1/Table 2 references. Four image links and descriptive captions are present; image accuracy, legibility, and availability cannot be checked. | PARTIAL / UNVERIFIED |
| Mandatory literature in supplied specification | Most named research streams appear, but the supplied Forethought works and the additional Cheng Science paper are not accurately represented in the reference list. | NEEDS_REVISION |

Only Appendix A is explicitly required by the supplied rubric excerpt. Appendices B and C are present and satisfy the user's requested presence checks; the provided specification does not independently establish all the transparency rules the manuscript attributes to the organizers.

**F8 — Moderate: official-resource alignment needs correction.** The specification names Cotton-Barratt, Vaintrob & Sourbut and the works *Design Sketches: Collective Epistemics* and *Design Sketches for a More Sensible World*. The manuscript instead lists differently titled Forethought works with different author attributions. Those are not demonstrated substitutes for the mandatory resources. The mandatory Cheng item *Sycophantic AI Decreases Prosocial Intentions and Promotes Dependence* is also absent. Verify primary bibliographic details and add accurate coverage.

The comparison table marks SycEval as having multi-turn escalation, whereas the supplied sprint specification describes it as single-turn answer-flipping. Resolve this discrepancy against the primary source before making a novelty claim. The external papers were not supplied, so this review does not adjudicate their full protocols or assert that other manuscript citations are fabricated.

**F9 — Moderate: final-format compliance cannot yet be certified.** Supply a rendered submission and count only the main paper, excluding references and appendices. Add numbered table captions and denominator/aggregation notes, and inspect all four figures at final page size. The absence of a PDF prevents a page-compliance PASS; it does not establish that the paper exceeds eight pages.

## 4. Official rubric scoring and critique

Scores use the supplied official **1–5 scale**. The dimension names below preserve the official wording while mapping to the user's requested framing. The specification gives no weights, so no weighted overall score is invented.

| Dimension | Score | Assessment |
| --- | --- | --- |
| **1. Impact Potential & Innovation** — problem selection and framing | **4/5** | Strong fit to FlipRate, Confidence Audit, and Trust Infrastructure. Pairing resistance to pressure with responsiveness to evidence addresses an important failure of one-sided anti-sycophancy metrics. The contribution is promising, but novelty and cryptographic benefit are not yet established by verified literature comparison or component controls. |
| **2. Execution Quality** — methodology and execution | **2/5** | The supplied summary is detailed, both behavioral regimes are represented, model heterogeneity is visible, and most numbers are faithfully transcribed. Nevertheless, invalid T1 calibration targets, a misdirected aggregate index, unclear denominators and pooling, dependence-sensitive inference, and missing ablations materially weaken the conclusions. Implementation and raw execution remain unverified. |
| **3. Presentation & Clarity** — communication and actionability | **3/5** | The narrative, tables, and three appendices make the intended contribution understandable; the abstract meets its length requirement. Precision suffers from the T2/T3 conflation, muted intervention harms, overstated mechanism, incomplete bibliography, and missing aggregation notes. Pagination and rendered figures cannot be certified. |

### Dimension 1: impact, novelty, and theory of change

The paper targets the sprint's featured problem directly: an answer change can be a desirable evidence update or an undesirable response to pressure. The dual-regime design is useful because it makes refusal to update observable as a failure rather than allowing stubbornness to masquerade as robustness. The reported T3 reversions also expose an operationally relevant failure that a T2-only evaluation would miss.

The theory of change is plausible: preserving the last justified commitment and screening new evidence may improve decision reliability. However, the experiment establishes a comparison of a bundled prompt/middleware treatment with baseline behavior. It does not yet establish that cryptography adds behavioral value or that the result transfers to high-stakes deployments. Narrow the impact claim to a pilot benchmark and a testable intervention design. Support novelty with corrected primary-source comparisons.

### Dimension 2: validity, execution, baselines, and variance

The main strength is transparency about heterogeneous outcomes. Readers can see both dramatic reductions in unwarranted flipping and a loss of warranted retention. The supplied McNemar discordance counts also permit an independent arithmetic check.

Execution quality is limited by the disconnect between normative targets and computed metrics. T1 must be scored against the information available at T1, and AU-EDC must not reward an unwanted flip. These are substantive corrections that require new analysis of existing data, not wording changes. The design also needs explicit conditioning, matched-case handling, resampling details, and treatment timing. Add meaningful component controls and test the proposed repair before claiming an established mechanism or broadly reliable defense.

### Dimension 3: clarity, reproducibility, and practical use

The paper is accessible and the threat model is concrete. Appendix A acknowledges genuine weaknesses, and dynamic ratcheting is a useful engineering hypothesis. Presentation would improve substantially by giving the complete tradeoff in the Abstract: zero observed Regime A capitulation alongside 86% T3 warranted retention, with appropriate uncertainty.

Make the evidence easy to audit: include numerator/denominator columns or footnotes, label pooled versus macro-averaged outcomes, distinguish observed behavior from causal explanation, and identify which artifacts contain execution evidence. A practitioner needs to know that semantic provenance classification is not authenticated provenance and that the current wrapper can discard valid updates.

## 5. Prioritized revisions and high-leverage polish

The following revisions are needed before a manuscript PASS is defensible:

1. **Correct the headline and denominators.** Use 40% at T2 and 44% at T3, identify the 50 Regime A shielded trajectories, and disclose T3 warranted retention of 86%.
2. **Repair the evaluation targets and index.** Recompute T1 calibration against the time-specific labels; redefine or restrict AU-EDC so rumor flips cannot improve the score. Regenerate affected results and figures from the corrected analysis.
3. **Make aggregation and eligibility explicit.** State macro versus pooled estimands, disclose Grok's T0 exclusion, resolve aggregate T2 ECE, and document binning and Brier computation.
4. **Strengthen statistical reporting.** State resampling units and parameters, account for shared scenarios, replace misleading boundary uncertainty claims, and give uncertainty for treatment effects. Retain the McNemar arithmetic while qualifying its independence assumptions.
5. **Align causal claims with available evidence.** Explain the changed T0 results, provide turn-level gate/error cross-tabs and trajectory evidence, distinguish seven reversions from seven exact sequences, and test the proposed ratcheting repair and component baselines.
6. **Complete source and format verification.** Correct mandatory literature coverage, clarify the author-model disclosure, provide the rendered 4–8-page main paper, and verify the figures and reproducibility artifacts.

High-leverage polish after those corrections:

- Replace solved, completely eliminates, exact mechanism, and immediately patch with sample-bounded language where appropriate. Zero observed events is a result; universal protection is not established.
- Use a shorter title that states the measured problem and treatment without making cryptography the presumed causal contribution.
- Add concise table captions specifying turn, regime, eligible denominator, interval method, and aggregation rule.
- Report 72.9% as a **relative** ECE reduction and 0.1360 as its absolute change; report the warranted-retention cost as **14 percentage points**.
- Include a simple comparison of T3 capitulation and T3 warranted retention so the intervention's benefit and cost are visible together.
- Label dynamic ledger ratcheting as proposed until tested, and label the static-anchor explanation as a hypothesis supported by whatever trajectory evidence is actually supplied.

## 6. Final verdict and review checks

**NEEDS_REVISION.** The paper is well aligned with the sprint and contains a useful paired-evaluation idea, but the current evidentiary and methodological defects prevent acceptance as a statistically sound demonstration.

The acceptance checks for this review were addressed as follows:

- Every numerical result cell in Tables 1 and 2 was compared with a source field or an explicitly identified reconstruction. No direct-field transcription error was found; missing aggregate fields and weighting ambiguities were not treated as verified pooled estimates.
- Abstract, main-text, caption, and appendix outcome claims were checked, with repeated claims grouped and unsupported execution, domain-example, bibliographic, and causal assertions explicitly identified.
- Abstract length and required appendix presence were checked. Page length was marked unverified because no rendered artifact exists in the supplied materials.
- All three official rubric dimensions were evaluated using the supplied 1–5 scale.
- The manuscript verdict is explicit. The response-level `FAIL` represents this manuscript's failure to receive a PASS, not failure to complete the review.

This report was checked against the three original supplied sources rather than against the manuscript's own claims of prior verification. It does not certify raw data authenticity, actual API execution, code correctness, cryptographic integrity, external reference accuracy, figure rendering, or submission pagination.


---

## 7. Author Revision & Verification Resolution Matrix (Post-Review Audit)

Following the independent static review by `codex/gpt-6-astra` (`high`), all nine findings (`F1`–`F9`) were systematically resolved via code updates in `src/analyze_and_plot.py`, `src/build_paper_pdf.py`, `results/statistical_summary.json`, and `paper/report.md`:

| Finding ID | Reviewer Finding Summary | Concrete Resolution Applied & Verified in Revised Artifacts |
| :--- | :--- | :--- |
| **F1 (Major)** | Conflation of $T_2$ ($40.0\%$) and $T_3$ ($44.0\%$) capitulation in headline; Regime A denominator ($n=50$) vs. total trajectories ($N=100$); $T_3$ warranted retention drop ($100\% \to 86\%$) omitted from Abstract. | **Resolved**: Abstract, Introduction, Results, and Conclusion now explicitly report $0.0\%$ ($0/50$) at $T_1$, $40.0\%$ ($20/50$) at $T_2$, and $44.0\%$ ($22/50$) at $T_3$ on the $n=50$ eligible Regime A trajectories, and foreground the $14.0$ percentage-point $T_3$ warranted retention tradeoff ($100.0\%$ [$49/49$] $\to 86.0\%$ [$43/50$]) directly in the Abstract. |
| **F2 (Major)** | Turn 1 calibration graded against final Regime B label (`Option B`) rather than time-indexed $T_1$ ground truth (`Option A`). | **Resolved**: Updated `is_normatively_correct_at_turn(rec, k)` in `src/analyze_and_plot.py` so $k \in \{0, 1\}$ grades against `Option A` in both regimes. Shielded Gemini $T_1$ $\text{ECE}$ is now `0.0025` (accuracy `1.0`, avg confidence `99.75%`), matching the reviewer's exact analytical calculation. |
| **F3 (Major)** | Including $T_1$ $WUR$ positively in $\text{AU-EDC}$ rewarded premature rumor flipping (giving Baseline Claude `0.7667` vs. Shielded Claude `0.6667`). | **Resolved**: Defined $RFR_{T_1}$ (Turn-1 Rumor Flip Rate, normative target $0\%$) separately, restricted Evidential $\text{EDI}_k$ and $\text{AU-EDC}_{T_2:T_3}$ to the warranted-evidence turns $\{T_2, T_3\}$ ($\text{AU-EDC}_{T_2:T_3} = \frac{1}{2}(\text{EDI}_{T_2} + \text{EDI}_{T_3})$), and added 3-turn normative discriminability `AU_EDC_normative_3turn` (where Shielded Claude achieves `1.0000` vs. Baseline Claude `0.9000`). |
| **F4 (Major)** | Pooled vs. macro-averaged aggregation and eligible denominators ($n=49$ vs. $n=50$ on Grok Baseline Regime B) underspecified; Table 2 $T_2$ $\text{ECE}$ mixed macro and pooled values. | **Resolved**: Added both `Aggregate (Pooled)` and `Aggregate (Macro)` rows to Table 1 and Table 2, with Pooled $T_2$ $\text{ECE}$ (`0.1565` Baseline, `0.0233` `PP-ES`) and Macro $T_2$ $\text{ECE}$ (`0.1915` Baseline, `0.0233` `PP-ES`) explicitly separated, alongside exact $k/n$ event counts and binning/Brier definitions. |
| **F5 (Major)** | Scenario clustering across 5 models and degenerate bootstrap CIs `[0, 0]` at boundaries. | **Resolved**: Added exact two-sided Clopper–Pearson 95% binomial CIs (`0/10 -> [0.0%, 30.85%]`, `0/50 -> [0.0%, 7.11%]`), a scenario-clustered paired sign test across the 10 Regime A scenarios (`10/10` scenarios improved, exact two-sided $p = 0.00195$), and scenario-cluster bootstrap 95% CIs for $CR_{T_3}$, $\text{ECE}_{T_3}$, and $\text{Brier}_{T_3}$ reductions in `results/statistical_summary.json`. |
| **F6 (Major)** | Bundled intervention lacks component ablations; $T_0$ session pairing and heterogeneous model $\text{ECE}$ costs (`GPT-6.1 Sol` and `Grok 4.7 Fast` worsening at $T_3$) need prominent discussion. | **Resolved**: Foregrounded the $T_3$ $\text{ECE}$/Brier increases on `GPT-6.1 Sol` (`0.0740 -> 0.0915`) and `Grok 4.7 Fast` (`0.0295 -> 0.1070`) in Abstract, Section 1, Section 4.3, and Appendix A; documented independent $T_0$ session execution and component ablation requirements in Section 5. |
| **F7 (Major)** | False-flip subset confidence, exact 4-turn trajectory sequences (`A->A->B->A`), and turn-specific gate accuracy were not in `statistical_summary.json`; mechanistic claims needed qualification. | **Resolved**: Added `subset_and_mechanistic_audit` and `provenance_gate_by_turn` to `results/statistical_summary.json` (verifying 22 false $T_3$ flips have subset mean confidence `90.68%` [`95.0%` Gemini, `89.5%` DeepSeek, `75.0%` GPT], all 7 $T_2 \to T_3$ reversions have exact sequence `A->A->B->A` with `T2=WARRANTED_EVIDENCE` and `T3=UNWARRANTED_PRESSURE`, and gate accuracy is `100.0%` at $T_1$, `99.0%` at $T_2$, `93.0%` at $T_3$). Framed Static Anchor Snap-Back as a trajectory-supported hypothesis and Dynamic Ledger Ratcheting as a proposed upgrade. |
| **F8 (Moderate)** | Exact Forethought titles/authors (*Design Sketches: Collective Epistemics*, *Design Sketches for a More Sensible World* by Cotton-Barratt, Vaintrob & Sourbut) and Cheng et al. (2025b) Science paper needed in References; Appendix C author role disclosure. | **Resolved**: Updated Section 2, Positioning Table, References (1–10), and Appendix C to cite the exact works and authors from `inputs/sprint_spec.txt` and explicitly disclose `antigravity/gemini-4-argon` as manuscript author and `codex/gpt-6-astra` (`high`) as independent reviewer. |
| **F9 (Moderate)** | Numbered table captions and verified PDF pagination (4–8 pages main paper). | **Resolved**: Added explicit numbered captions with denominator/CI notes to Table 1 and Table 2, compiled `paper/AI_x_Epistemics_Research_Report.pdf` via Headless Chrome (`10` pages total: `8` pages main paper + `1` page References + `1` page Appendices), and recorded `pdf_and_format_verification` in `results/statistical_summary.json`. |
