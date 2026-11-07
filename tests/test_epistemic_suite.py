"""
Automated Unit & Integrity Tests for EpistemicFlipBench and PP-ES Cryptographic Ledger.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from epistemic_shield_ledger import EpistemicCommitmentLedger
from analyze_and_plot import compute_ece_and_brier, bootstrap_ci, exact_binomial_two_sided_p


class TestEpistemicSuite(unittest.TestCase):
    def test_dataset_schema_and_balance(self):
        data_path = ROOT / "data" / "epistemic_flip_bench.json"
        self.assertTrue(data_path.exists(), "Dataset file must exist")
        scenarios = json.loads(data_path.read_text(encoding="utf-8"))
        self.assertEqual(len(scenarios), 20, "Must contain exactly 20 multi-turn scenarios")

        reg_a = [s for s in scenarios if s["regime"] == "unwarranted_pressure"]
        reg_b = [s for s in scenarios if s["regime"] == "warranted_evidence"]
        self.assertEqual(len(reg_a), 10, "Must have 10 Regime A scenarios")
        self.assertEqual(len(reg_b), 10, "Must have 10 Regime B scenarios")

        for s in scenarios:
            self.assertIn(s["ground_truth"], ("A", "B"))
            self.assertIn(s["initial_correct_target"], ("A", "B"))
            self.assertIn("A", s["options"])
            self.assertIn("B", s["options"])
            for k in ("t0_prompt", "t1_rebuttal", "t2_rebuttal", "t3_rebuttal"):
                self.assertTrue(len(s[k].strip()) > 20, f"Missing or short {k} in {s['id']}")

    def test_cryptographic_ledger_integrity_and_tamper_detection(self):
        ledger = EpistemicCommitmentLedger("REGIME_A_01", "antigravity/gemini-3.8-flash", "EpistemicShield")
        e0 = ledger.append_turn(0, "A", 95.0, "INITIAL_ELICITATION", "Initial derivation via Simpson's paradox.")
        e1 = ledger.append_turn(1, "A", 95.0, "UNWARRANTED_PRESSURE", "Maintained A against subjective doubt.")
        e2 = ledger.append_turn(2, "A", 94.0, "UNWARRANTED_PRESSURE", "Rejected unverified authority assertion.")
        e3 = ledger.append_turn(3, "A", 95.0, "UNWARRANTED_PRESSURE", "Maintained A under ultimatum.")

        self.assertEqual(len(ledger.entries), 4)
        self.assertTrue(ledger.verify_integrity(), "Untampered hash chain must verify True")
        self.assertIn(e0["chain_hash"], ledger.format_s0_anchor_header())

        # Simulate retroactive tampering with Turn 1 choice
        ledger.entries[1]["choice"] = "B"
        self.assertFalse(ledger.verify_integrity(), "Tampered ledger must fail verification")

        # Restore and tamper with Turn 0 rationale hash
        ledger.entries[1]["choice"] = "A"
        self.assertTrue(ledger.verify_integrity())
        ledger.entries[0]["confidence"] = 55.0
        self.assertFalse(ledger.verify_integrity(), "Tampered T0 confidence must break downstream chain")

    def test_statistical_metrics(self):
        # Perfectly calibrated predictions
        preds = [(True, 100.0)] * 8 + [(False, 50.0)] * 2
        ece, brier, dcb = compute_ece_and_brier(preds)
        self.assertGreaterEqual(ece, 0.0)
        self.assertGreaterEqual(brier, 0.0)

        mean_v, lo_v, hi_v = bootstrap_ci([1.0, 1.0, 0.0, 1.0, 0.0])
        self.assertAlmostEqual(mean_v, 0.6, places=4)
        self.assertLessEqual(lo_v, mean_v)
        self.assertGreaterEqual(hi_v, mean_v)

        p_val = exact_binomial_two_sided_p(18, 20)
        self.assertLess(p_val, 0.001)

    def test_empirical_artifacts_and_submission_compliance(self):
        traj_path = ROOT / "results" / "raw_trajectories.jsonl"
        ledger_path = ROOT / "results" / "tamper_evident_ledger.json"
        stats_path = ROOT / "results" / "statistical_summary.json"
        pdf_path = ROOT / "paper" / "AI_x_Epistemics_Research_Report.pdf"
        docx_path = ROOT / "paper" / "AI_x_Epistemics_Research_Report.docx"

        self.assertTrue(traj_path.exists())
        self.assertTrue(ledger_path.exists())
        self.assertTrue(stats_path.exists())
        self.assertTrue(pdf_path.exists())
        self.assertTrue(docx_path.exists())

        rows = [json.loads(line) for line in traj_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertEqual(len(rows), 200, "Must contain exactly 200 completed 4-turn trajectories (800 turns)")

        ledger_summary = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertTrue(ledger_summary["all_ledgers_cryptographically_verified"])
        self.assertEqual(ledger_summary["total_trajectories"], 200)

        stats = json.loads(stats_path.read_text(encoding="utf-8"))
        self.assertEqual(stats["aggregate"]["Baseline"]["CR_T3"]["k_events"], 22)
        self.assertEqual(stats["aggregate"]["Baseline"]["CR_T3"]["n_eligible"], 50)
        self.assertEqual(stats["aggregate"]["EpistemicShield"]["CR_T3"]["k_events"], 0)
        self.assertEqual(stats["aggregate"]["EpistemicShield"]["CR_T3"]["n_eligible"], 50)
        self.assertAlmostEqual(
            stats["models"]["antigravity/gemini-3.8-flash"]["conditions"]["EpistemicShield"]["calibration"]["T1"]["ece"],
            0.0025,
            places=4,
        )

        ver = stats.get("pdf_and_format_verification", {})
        self.assertTrue(ver.get("meets_150_to_250_word_abstract_limit"), "Abstract must be strictly 150-250 words")
        self.assertEqual(ver.get("main_paper_pages_excluding_refs_and_appendices"), 8, "Main paper must be <= 8 pages")
        self.assertEqual(ver.get("total_pdf_pages_with_refs_and_appendices"), 10, "Total PDF pages must be 10")


if __name__ == "__main__":
    unittest.main()
