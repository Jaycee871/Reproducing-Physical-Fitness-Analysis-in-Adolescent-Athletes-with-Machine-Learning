from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
HTML = HERE / "poster.html"
PDF = HERE / "poster.pdf"
PNG = HERE / "poster.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 5760, "height": 3456}, device_scale_factor=1)
    page.goto(HTML.as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")

    page.pdf(
        path=str(PDF),
        width="60in",
        height="36in",
        print_background=True,
        margin={"top":"0","right":"0","bottom":"0","left":"0"},
        prefer_css_page_size=True,
    )

    page.screenshot(path=str(PNG), full_page=True)
    browser.close()

print(f"Wrote {PDF}")
print(f"Wrote {PNG}")
