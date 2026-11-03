import asyncio, pathlib
from playwright.async_api import async_playwright

OUT = pathlib.Path(__file__).resolve().parent.parent / "pins"
OUT.mkdir(exist_ok=True)

# Simple flat illustrations (original SVG, no product photos)
CART = """<svg viewBox="0 0 300 340" width="420"><g fill="none" stroke="{ink}" stroke-width="10" stroke-linecap="round">
<rect x="40" y="40" width="220" height="70" rx="10" fill="{a}"/><rect x="40" y="140" width="220" height="70" rx="10" fill="{b}"/>
<rect x="40" y="240" width="220" height="60" rx="10" fill="{a}"/><line x1="40" y1="40" x2="40" y2="300"/><line x1="260" y1="40" x2="260" y2="300"/></g>
<g fill="{ink}"><circle cx="60" cy="322" r="14"/><circle cx="240" cy="322" r="14"/></g>
<g fill="{c}"><rect x="70" y="10" width="60" height="40" rx="8"/><circle cx="200" cy="25" r="22"/></g></svg>"""

MIXER = """<svg viewBox="0 0 320 320" width="420"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M60 70 Q60 30 110 30 L230 30 Q270 30 270 70 L270 110 L60 110 Z" fill="{a}"/>
<rect x="200" y="110" width="60" height="150" rx="10" fill="{a}"/>
<path d="M70 170 L180 170 L165 245 L85 245 Z" fill="{c}"/>
<rect x="30" y="262" width="260" height="34" rx="10" fill="{b}"/></g>
<g fill="{ink}"><path d="M10 279 l18 -12 v24 z"/><path d="M310 279 l-18 -12 v24 z"/></g></svg>"""

MITT = """<svg viewBox="0 0 320 320" width="400"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round">
<path d="M90 280 L90 120 Q90 50 150 50 Q200 50 200 110 L200 150 Q230 120 255 140 Q275 160 245 195 L200 245 L200 280 Z" fill="{a}"/>
<rect x="80" y="270" width="130" height="36" rx="8" fill="{b}"/></g>
<g fill="{c}"><circle cx="125" cy="130" r="9"/><circle cx="160" cy="170" r="9"/><circle cx="125" cy="210" r="9"/><circle cx="165" cy="105" r="9"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><path d="M265 60 l10 22 24 3 -18 16 5 24 -21 -12 -21 12 5 -24 -18 -16 24 -3z"/></g></svg>"""

BLANKET = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M40 90 Q40 60 70 60 L250 60 Q280 60 280 90 L280 230 Q280 260 250 260 L70 260 Q40 260 40 230 Z" fill="{a}"/>
<path d="M40 200 Q160 150 280 200 L280 230 Q280 260 250 260 L70 260 Q40 260 40 230 Z" fill="{b}"/>
<line x1="90" y1="75" x2="90" y2="175" stroke="{c}"/><line x1="160" y1="75" x2="160" y2="165" stroke="{c}"/><line x1="230" y1="75" x2="230" y2="175" stroke="{c}"/>
<path d="M280 150 Q305 150 305 175 L305 290" fill="none"/><rect x="290" y="285" width="30" height="20" rx="4" fill="{ink}"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="5"><path d="M40 30 q10 -18 20 0 q10 18 20 0" fill="none"/><path d="M130 30 q10 -18 20 0 q10 18 20 0" fill="none"/></g></svg>"""

DESK = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="30" y="150" width="260" height="130" rx="12" fill="{a}"/>
<rect x="45" y="200" width="230" height="65" rx="8" fill="{b}"/><line x1="135" y1="232" x2="185" y2="232"/>
<rect x="45" y="60" width="70" height="90" rx="8" fill="{b}"/><rect x="200" y="95" width="75" height="55" rx="8" fill="{b}"/></g>
<g stroke="{ink}" stroke-width="8" stroke-linecap="round"><line x1="65" y1="60" x2="58" y2="20"/><line x1="82" y1="60" x2="88" y2="15"/><line x1="98" y1="60" x2="108" y2="28"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><rect x="128" y="85" width="58" height="65" rx="6"/></g>
<g fill="{ink}"><circle cx="58" cy="18" r="7"/><circle cx="108" cy="26" r="7"/></g></svg>"""

import json, sys
STYLES = {
  "terracotta": dict(bg="#F3E9DC", a="#C8553D", b="#F2D0A4", c="#2D6A4F", ink="#2B2118", accent="#C8553D"),
  "mint": dict(bg="#E8F1EE", a="#9AD1C0", b="#F4A261", c="#E9C46A", ink="#1D3540", accent="#E76F51"),
  "lavender": dict(bg="#EEEAF6", a="#B8A9E3", b="#FFFFFF", c="#F28482", ink="#2A2440", accent="#6C5CE7"),
  "rose": dict(bg="#FBE8EA", a="#E8A0A8", b="#FFFFFF", c="#B5485A", ink="#3A1F25", accent="#B5485A"),
}
ARTS = {"cart": CART, "mixer": MIXER, "mitt": MITT, "blanket": BLANKET, "desk": DESK}
# pins.json: [{"file","art":"cart|mixer|mitt|blanket|desk","style":"terracotta|mint|lavender|rose","kicker","title","sub"}]
PINS = []
for p in json.load(open(sys.argv[1])):
    d = dict(STYLES[p["style"]]); d.update(p); d["art"] = ARTS[p["art"]]; PINS.append(d)

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:I;src:url(file:///usr/share/fonts/opentype/inter/Inter-Medium.otf)}}
*{{margin:0;box-sizing:border-box}} body{{width:1000px;height:1500px;background:{bg};font-family:I;color:{ink};
display:flex;flex-direction:column;padding:90px 80px 60px;overflow:hidden}}
.k{{font-family:P;letter-spacing:6px;font-size:30px;color:{accent}}}
h1{{font-family:P;font-size:84px;line-height:1.05;margin:24px 0 28px}}
.s{{font-size:38px;line-height:1.35;opacity:.85}}
.art{{flex:1;display:flex;align-items:center;justify-content:center}}
.cta{{align-self:flex-start;background:{ink};color:{bg};font-family:P;font-size:36px;padding:22px 40px;border-radius:60px}}
.f{{display:flex;justify-content:space-between;margin-top:40px;font-size:24px;opacity:.75}}
</style></head><body><div class="k">{kicker}</div><h1>{title}</h1><div class="s">{sub}</div>
<div class="art">{svg}</div><div class="cta">See it on Amazon &rarr;</div>
<div class="f"><span>Nice Finds</span><span>Affiliate link &middot; I may earn from qualifying purchases</span></div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1000, "height": 1500})
        for d in PINS:
            svg = d["art"].format(**d)
            html = TPL.format(svg=svg, **d)
            import tempfile; f = pathlib.Path(tempfile.gettempdir()) / f"{d['file']}.html"; f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{d['file']}.png"))
        await b.close()

asyncio.run(main())
