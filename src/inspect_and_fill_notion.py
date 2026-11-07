"""
Fills and submits the Apart Research Notion Pre-Sprint Survey:
https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8
"""
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"
NOTION_URL = "https://apartresearch.notion.site/2b0fcfd1de9d8080ac3ac4c41a78c8f8"


def fill_and_submit_notion():
    out_dir = ROOT / "outputs" / "portal_receipts"
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = b.new_page(viewport={"width": 1280, "height": 1200})
        page.goto(NOTION_URL, wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        inputs = page.locator("input[placeholder='你的答案'], input[placeholder='Your answer']")
        print("Text inputs count:", inputs.count())
        # [0]: Name, [1]: Email, [2]: LinkedIn, [3]: GitHub, [4]: Current Role, [5]: Geographic Location
        inputs.nth(0).fill("Zeshuai Pi")
        inputs.nth(1).fill("pizeshuai@gmail.com")
        inputs.nth(2).fill("N/A")
        inputs.nth(3).fill("https://github.com/pipi333")
        inputs.nth(4).fill("Independent AI Safety & Epistemics Researcher")
        inputs.nth(5).fill("Online")

        # Click "Which Sprint/Hackathon?" dropdown
        dropdown_btn = page.locator("div[role='button']").filter(has_text="你的答案").first
        if dropdown_btn.count() == 0:
            dropdown_btn = page.locator("div[role='button']").filter(has_text="Your answer").first
        dropdown_btn.click()
        time.sleep(1.5)

        # Print all visible options in dropdown popover
        options_text = page.inner_text("body")
        print("=== DROPDOWN OPENED ===")
        # Look for Epistemics option
        epistemics_opt = page.get_by_text("Epistemics", exact=False)
        print("Epistemics matches:", epistemics_opt.count())
        if epistemics_opt.count() > 0:
            epistemics_opt.first.click()
        else:
            # Print all role=option or menuitem
            for el in page.locator("[role='option'], [role='menuitem'], div[role='button']").all():
                try:
                    t = el.inner_text().strip()
                    if t:
                        print("OPT:", t)
                except Exception:
                    pass
        time.sleep(1)

        # Fill Textarea: Current/Biggest Challenge
        ta = page.locator("textarea").first
        ta.fill(
            "Bridging empirical multi-turn AI epistemics evaluations with verifiable cryptographic trust infrastructure, "
            "and seeking research feedback, compute support, and publication mentorship via the Apart Fellowship."
        )

        # Click radio/checkbox buttons by exact text
        choices = [
            "Intermediate (projects/research)",
            "Actively planning transition",
            "Prefer to work solo",
            "Mid career (3-10 years)",
            "Contribute to AI safety research",
            "Build portfolio project",
            "Get feedback on ideas",
            "Attending full event",
            "Social media",
            "Yes, I agree",
        ]
        for c_txt in choices:
            loc = page.locator("div[role='button']").filter(has_text=c_txt).first
            loc.scroll_into_view_if_needed()
            loc.click()
            time.sleep(0.25)

        time.sleep(1)
        filled_desktop = out_dir / "notion_survey_filled_desktop_1280x900.png"
        page.screenshot(path=str(filled_desktop), full_page=True)

        page.set_viewport_size({"width": 375, "height": 812})
        time.sleep(0.5)
        filled_mobile = out_dir / "notion_survey_filled_mobile_375x812.png"
        page.screenshot(path=str(filled_mobile), full_page=True)

        page.set_viewport_size({"width": 1280, "height": 1200})
        time.sleep(0.5)

        # Click Submit ("提交" or "Submit")
        submit_btn = page.locator("div[role='button']").filter(has_text="提交")
        if submit_btn.count() == 0:
            submit_btn = page.locator("div[role='button']").filter(has_text="Submit")
        submit_btn.last.scroll_into_view_if_needed()
        submit_btn.last.click()

        time.sleep(5)
        after_text = page.inner_text("body")
        print("=== AFTER SUBMIT TEXT ===")
        print(after_text[:1500])

        receipt_desktop = out_dir / "notion_survey_receipt_desktop_1280x900.png"
        page.screenshot(path=str(receipt_desktop), full_page=True)

        page.set_viewport_size({"width": 375, "height": 812})
        time.sleep(0.5)
        receipt_mobile = out_dir / "notion_survey_receipt_mobile_375x812.png"
        page.screenshot(path=str(receipt_mobile), full_page=True)

        b.close()


if __name__ == "__main__":
    fill_and_submit_notion()
