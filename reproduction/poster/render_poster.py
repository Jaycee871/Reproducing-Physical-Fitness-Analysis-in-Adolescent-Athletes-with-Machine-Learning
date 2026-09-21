from pathlib import Path
import base64
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
HTML = HERE / "poster.html"
PNG = HERE / "poster_preview.png"
EMBED = HERE / "poster_embed.html"

html = HTML.read_text(encoding="utf-8")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 2400, "height": 1440})
    page.set_content(html, wait_until="load")
    page.screenshot(path=str(PNG), full_page=True)
    browser.close()

encoded = base64.b64encode(PNG.read_bytes()).decode("ascii")
EMBED.write_text(
    '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>中文重現海報</title><style>html,body{margin:0;background:#f3f7f8}'
    'img{display:block;width:100%;height:auto}</style></head><body>'
    '<img alt="青少年男性運動員體適能機器學習分析重現研究海報" '
    'src="data:image/png;base64,' + encoded + '"></body></html>',
    encoding="utf-8",
)

print(f"Wrote {PNG}")
print(f"Wrote {EMBED}")
