"""
Automated Registration & Project Submission Helper for Apart Research:
AI x Epistemics Research Sprint (Nov 13-15, 2026)
URL: https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15

Configured for:
- Author / Participant: Zeshuai Pi (pizeshuai@gmail.com)
- Location: Online
- Discord: creampp
- GitHub: https://github.com/pipi333
"""
import argparse
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"
SPRINT_URL = "https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15"

PROJECT_TITLE = (
    "Epistemic Discriminability Under Multi-Turn Pressure: Auditing the Authority Cliff "
    "and Evaluating Pre-Commitment & Provenance Gating"
)

PROJECT_SUMMARY_236W = (
    "Language models in clinical, financial, legal, and engineering workflows must resist "
    "unwarranted social or institutional pressure while revising prior beliefs when presented "
    "with verifiable primary evidence. Single-turn sycophancy benchmarks conflate robustness "
    "with stubbornness. We introduce EpistemicFlipBench (Track 1), a 20-scenario, four-turn "
    "benchmark contrasting Regime A (Unwarranted Rebuttal Pressure escalating from mild doubt "
    "to institutional citation and executive coercion; n=10) against Regime B (Warranted "
    "Evidential Revision progressing from unverified rumor to primary telemetry and audit "
    "confirmation; n=10). Across five frontier models (200 trajectories, 800 turns), we "
    "uncover an Authority Cliff in Regime A (n=50 eligible trajectories): baseline capitulation "
    "is 0.0% (0/50) at Turn 1, rises to 40.0% (20/50) at Turn 2 under institutional citation, "
    "and reaches 44.0% (22/50; 95% bootstrap CI: [30.0%, 58.0%]) at Turn 3, while pooled ECE "
    "degrades from 0.0510 (Turn 0) to 0.1866 (Turn 3). In Regime B, premature Turn 1 rumor "
    "flipping occurs in 22.4% (11/49 pooled; 22.2% macro-mean; three models at 30.0%). We "
    "evaluate the Provenance & Pre-Commitment Epistemic Shield (PP-ES, Track 2), bundling a "
    "SHA-256 commitment ledger with an inference-time provenance gate. On this benchmark, PP-ES "
    "reduces observed Regime A capitulation to 0.0% (0/50; exact McNemar p=4.77e-7; clustered "
    "sign test p=0.00195), lowers Turn 1 rumor flipping to 2.0% (1/50), cuts pooled Turn 3 ECE "
    "by 72.9% relatively (-0.1360 absolute, to 0.0506), and preserves 100.0% (50/50) Turn 2 "
    "revision, but reduces Turn 3 warranted retention from 100.0% (49/49) to 86.0% (43/50)."
)

DEFAULT_REASON_FOR_JOINING = (
    "To investigate multi-turn epistemic robustness and calibration under institutional pressure, "
    "and to build verifiable cryptographic pre-commitment and provenance-gating infrastructure "
    "that separates warranted Bayesian belief updating from sycophantic capitulation."
)

DEFAULT_PROJECT_INTENT = (
    "We are building EpistemicFlipBench (Track 1: 20 4-turn high-stakes decision scenarios "
    "contrasting unwarranted authority coercion vs. primary empirical evidence) and the "
    "Provenance & Pre-Commitment Epistemic Shield (PP-ES, Track 2: a SHA-256 hash-chained "
    "T0 commitment ledger coupled with an inference-time provenance gate evaluated across 5 "
    "frontier model families)."
)


def build_payload_preview(args: argparse.Namespace) -> dict:
    pdf_path = ROOT / "paper" / "AI_x_Epistemics_Research_Report.pdf"
    slides_path = ROOT / "paper" / "AI_x_Epistemics_Slides.pdf"
    img_path = ROOT / "figures" / "fig2_epistemic_phase_space.png"
    words = len(PROJECT_SUMMARY_236W.split())
    return {
        "sprint_url": SPRINT_URL,
        "mode": args.mode,
        "signup_form_fields": {
            "FirstName_Framer": args.first_name,
            "LastName_Framer": args.last_name,
            "Email_Framer": args.email,
            "Location_Framer": args.location,
            "GitHub_Framer": args.github,
            "Scholar_Framer": args.scholar,
            "LinkedIn_Framer": args.linkedin,
            "Career_Framer": f"AI Epistemics & Trust Infrastructure Research (Discord: {args.discord})",
            "AISafetyExperience_Framer": args.experience,
            "ReasonForJoining_Framer": DEFAULT_REASON_FOR_JOINING,
            "ProjectIntent_Framer": DEFAULT_PROJECT_INTENT,
            "HeardAbout_Framer": "Social media",
        },
        "submission_form_fields": {
            "ProjectTitle_Framer": PROJECT_TITLE,
            "ProjectSummary_Framer ": PROJECT_SUMMARY_236W,
            "abstract_word_count": words,
            "PDF File": str(pdf_path),
            "pdf_exists": pdf_path.exists(),
            "pdf_size_mb": round(pdf_path.stat().st_size / (1024 * 1024), 3) if pdf_path.exists() else 0,
            "InterestedInPublishing_Framer": "Yes",
            "Tracks": ["Track 1", "Track 2"],
            "Code_Framer": args.code_url,
            "Image_File_Framer": str(img_path),
            "image_exists": img_path.exists(),
            "TeamName_Framer": args.team_name,
            "Location_Framer": args.location,
            "Member1_Name_Framer": f"{args.first_name} {args.last_name}".strip(),
            "Member1_Email_Framer": args.email,
            "Member1_Discord_Framer": args.discord,
            "Member1_Scholar_Framer": args.scholar,
        },
        "submission_window_utc": {
            "opens": "2026-11-13T12:00:00Z (2026-11-13 20:00 UTC+8)",
            "closes": "2026-11-16T13:00:00Z (2026-11-16 21:00 UTC+8)",
        },
    }


def run_signup(args: argparse.Namespace) -> dict:
    out_dir = ROOT / "outputs" / "portal_receipts"
    out_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print(f"Navigating to {SPRINT_URL} ...")
        page.goto(SPRINT_URL, wait_until="networkidle", timeout=45000)

        dialog_id = "sign-up-ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15"
        trigger = page.locator(f'button[commandfor="{dialog_id}"]').first
        trigger.click()
        dialog = page.locator(f"dialog#{dialog_id}")
        dialog.wait_for(state="visible", timeout=10000)

        dialog.locator('input[name="FirstName_Framer"]').fill(args.first_name)
        dialog.locator('input[name="LastName_Framer"]').fill(args.last_name)
        dialog.locator('input[name="Email_Framer"]').fill(args.email)
        dialog.locator('input[name="Location_Framer"]').fill(args.location)
        if args.github:
            dialog.locator('input[name="GitHub_Framer"]').fill(args.github)
        if args.scholar:
            dialog.locator('input[name="Scholar_Framer"]').fill(args.scholar)
        if args.linkedin:
            dialog.locator('input[name="LinkedIn_Framer"]').fill(args.linkedin)
        dialog.locator('textarea[name="Career_Framer"]').fill(
            f"AI Epistemics & Trust Infrastructure Research (Discord: {args.discord})"
        )
        dialog.locator(f'input[name="AISafetyExperience_Framer"][value="{args.experience}"]').check()
        dialog.locator('textarea[name="ReasonForJoining_Framer"]').fill(DEFAULT_REASON_FOR_JOINING)
        dialog.locator('textarea[name="ProjectIntent_Framer"]').fill(DEFAULT_PROJECT_INTENT)
        dialog.locator('select[name="HeardAbout_Framer"]').select_option("Social media")

        desktop_filled_shot = out_dir / "signup_filled_desktop_1280x900.png"
        page.screenshot(path=str(desktop_filled_shot))

        # Capture mobile 375x812 view as well per global rule
        page.set_viewport_size({"width": 375, "height": 812})
        time.sleep(0.3)
        mobile_filled_shot = out_dir / "signup_filled_mobile_375x812.png"
        page.screenshot(path=str(mobile_filled_shot))

        # Restore desktop viewport and submit
        page.set_viewport_size({"width": 1280, "height": 900})
        time.sleep(0.3)
        submit_btn = dialog.locator('button[type="submit"]')
        submit_btn.click()

        # Wait for navigation to /success-signup or status update
        try:
            page.wait_for_url("**/success**", timeout=20000)
        except Exception:
            time.sleep(5)

        final_url = page.url
        final_title = page.title()
        body_text = page.locator("main").inner_text() if page.locator("main").count() > 0 else page.inner_text("body")

        desktop_receipt_shot = out_dir / "signup_receipt_desktop_1280x900.png"
        page.screenshot(path=str(desktop_receipt_shot), full_page=True)

        page.set_viewport_size({"width": 375, "height": 812})
        time.sleep(0.3)
        mobile_receipt_shot = out_dir / "signup_receipt_mobile_375x812.png"
        page.screenshot(path=str(mobile_receipt_shot), full_page=True)

        browser.close()

    receipt = {
        "action": "sprint_signup",
        "participant": f"{args.first_name} {args.last_name}",
        "email": args.email,
        "location": args.location,
        "github": args.github,
        "discord": args.discord,
        "final_url": final_url,
        "final_title": final_title,
        "confirmation_text_excerpt": body_text[:1000],
        "screenshots": {
            "desktop_filled": str(desktop_filled_shot),
            "mobile_filled": str(mobile_filled_shot),
            "desktop_receipt": str(desktop_receipt_shot),
            "mobile_receipt": str(mobile_receipt_shot),
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    receipt_path = out_dir / "signup_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    return receipt


def run_submit_project(args: argparse.Namespace) -> dict:
    """Fills and submits the official project submission modal when the window is live."""
    out_dir = ROOT / "outputs" / "portal_receipts"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = ROOT / "paper" / "AI_x_Epistemics_Research_Report.pdf"
    slides_path = ROOT / "paper" / "AI_x_Epistemics_Slides.pdf"
    img_path = ROOT / "figures" / "fig2_epistemic_phase_space.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        page.goto(SPRINT_URL, wait_until="networkidle", timeout=45000)

        dialog_id = "submission-ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15"
        dialog = page.locator(f"dialog#{dialog_id}")

        # Open modal via official HTML5 dialog API if trigger button is not yet rendered
        trigger = page.locator(f'button[commandfor="{dialog_id}"]')
        if trigger.count() > 0 and trigger.first.is_visible():
            trigger.first.click()
        else:
            page.evaluate(f'document.getElementById("{dialog_id}").showModal()')

        dialog.wait_for(state="visible", timeout=10000)

        dialog.locator('input[name="ProjectTitle_Framer"]').fill(PROJECT_TITLE)
        dialog.locator('textarea[name="ProjectSummary_Framer "]').fill(PROJECT_SUMMARY_236W)
        dialog.locator('input[name="InterestedInPublishing_Framer"][value="Yes"]').check()
        dialog.locator('input[name="Tracks"][value="Track 1"]').check()
        dialog.locator('input[name="Tracks"][value="Track 2"]').check()
        if args.code_url:
            dialog.locator('input[name="Code_Framer"]').fill(args.code_url)
        dialog.locator('input[name="TeamName_Framer"]').fill(args.team_name)
        dialog.locator('input[name="Location_Framer"]').fill(args.location)
        dialog.locator('input[name="Member1_Name_Framer"]').fill(f"{args.first_name} {args.last_name}")
        dialog.locator('input[name="Member1_Email_Framer"]').fill(args.email)
        if args.discord:
            dialog.locator('input[name="Member1_Discord_Framer"]').fill(args.discord)
        if args.scholar:
            dialog.locator('input[name="Member1_Scholar_Framer"]').fill(args.scholar)

        submit_btn = dialog.locator('button[type="submit"]')
        is_disabled = submit_btn.is_disabled()
        status_text = dialog.locator(f"#{dialog_id}-status").inner_text().strip()

        desktop_preview = out_dir / "project_submission_preview_desktop_1280x900.png"
        page.screenshot(path=str(desktop_preview))

        page.set_viewport_size({"width": 375, "height": 812})
        time.sleep(0.3)
        mobile_preview = out_dir / "project_submission_preview_mobile_375x812.png"
        page.screenshot(path=str(mobile_preview))

        final_url = page.url
        if not is_disabled:
            page.set_viewport_size({"width": 1280, "height": 900})
            dialog.locator('input[name="PDF File"]').set_input_files(str(pdf_path))
            if slides_path.exists():
                dialog.locator('input[name="Slideshow_File_Framer"]').set_input_files(str(slides_path))
            if img_path.exists():
                dialog.locator('input[name="Image_File_Framer"]').set_input_files(str(img_path))
            submit_btn.click()
            try:
                page.wait_for_url("**/success**", timeout=30000)
            except Exception:
                time.sleep(5)
            final_url = page.url
            status_text = "SUBMITTED_LIVE"

        browser.close()

    return {
        "action": "project_submission",
        "submit_button_currently_disabled": is_disabled,
        "portal_status_message": status_text,
        "final_url": final_url,
        "screenshots": {
            "desktop_preview": str(desktop_preview),
            "mobile_preview": str(mobile_preview),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Apart Research Sprint Sign-up & Submission Helper")
    parser.add_argument("--mode", choices=["preview", "signup", "submit"], default="preview")
    parser.add_argument("--first-name", default="Zeshuai")
    parser.add_argument("--last-name", default="Pi")
    parser.add_argument("--email", default="pizeshuai@gmail.com")
    parser.add_argument("--location", default="Online")
    parser.add_argument("--team-name", default="EpistemicShield Lab")
    parser.add_argument("--discord", default="creampp")
    parser.add_argument("--github", default="https://github.com/pipi333")
    parser.add_argument("--scholar", default="")
    parser.add_argument("--linkedin", default="")
    parser.add_argument("--code-url", default="https://github.com/pipi333/apart-epistemics-sprint")
    parser.add_argument("--experience", default="Intermediate (projects/research)")
    args = parser.parse_args()

    if args.mode == "preview":
        print(json.dumps(build_payload_preview(args), indent=2, ensure_ascii=False))
    elif args.mode == "signup":
        res = run_signup(args)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args.mode == "submit":
        res = run_submit_project(args)
        print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
