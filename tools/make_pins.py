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

THERMO = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<ellipse cx="160" cy="250" rx="120" ry="40" fill="{b}"/><path d="M70 245 Q90 180 160 175 Q230 180 250 245 Z" fill="{c}"/>
<line x1="150" y1="200" x2="120" y2="110" stroke-width="8"/>
<rect x="70" y="30" width="110" height="90" rx="22" fill="{a}" transform="rotate(-18 125 75)"/>
<rect x="88" y="48" width="66" height="34" rx="8" fill="{b}" transform="rotate(-18 125 75)"/></g>
<g fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"><path d="M210 60 q12 -14 0 -28"/><path d="M235 70 q12 -14 0 -28"/></g></svg>"""

SPINNER = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M40 130 L280 130 L255 270 Q250 290 230 290 L90 290 Q70 290 65 270 Z" fill="{b}"/>
<path d="M65 150 L255 150 L238 255 L82 255 Z" fill="{c}"/>
<line x1="110" y1="160" x2="115" y2="245"/><line x1="160" y1="160" x2="160" y2="245"/><line x1="210" y1="160" x2="205" y2="245"/>
<ellipse cx="160" cy="125" rx="130" ry="26" fill="{a}"/>
<rect x="135" y="60" width="50" height="60" rx="14" fill="{ink}"/><circle cx="235" cy="118" r="12" fill="{ink}"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><path d="M60 70 q30 -40 60 0 q-30 25 -60 0z"/></g></svg>"""

COVER = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M70 280 L70 120 Q70 50 150 50 L230 50 Q275 50 275 100 L275 280 Z" fill="{a}"/>
<g stroke="{b}" stroke-width="5" opacity=".8"><line x1="80" y1="100" x2="265" y2="100"/><line x1="75" y1="150" x2="270" y2="150"/><line x1="72" y1="200" x2="270" y2="200"/><line x1="72" y1="250" x2="270" y2="250"/></g>
<rect x="110" y="170" width="90" height="70" rx="10" fill="{c}"/>
<rect x="40" y="276" width="260" height="22" rx="8" fill="{b}"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><path d="M285 25 l7 15 16 2 -12 11 3 16 -14 -8 -14 8 3 -16 -12 -11 16 -2z"/></g></svg>"""

import json, sys
STYLES = {
  "terracotta": dict(bg="#F3E9DC", a="#C8553D", b="#F2D0A4", c="#2D6A4F", ink="#2B2118", accent="#C8553D"),
  "mint": dict(bg="#E8F1EE", a="#9AD1C0", b="#F4A261", c="#E9C46A", ink="#1D3540", accent="#E76F51"),
  "lavender": dict(bg="#EEEAF6", a="#B8A9E3", b="#FFFFFF", c="#F28482", ink="#2A2440", accent="#6C5CE7"),
  "rose": dict(bg="#FBE8EA", a="#E8A0A8", b="#FFFFFF", c="#B5485A", ink="#3A1F25", accent="#B5485A"),
}
ARTS = {"cart": CART, "mixer": MIXER, "mitt": MITT, "blanket": BLANKET, "desk": DESK, "thermo": THERMO, "spinner": SPINNER, "cover": COVER}
# pins.json: [{"file","art":"cart|mixer|mitt|blanket|desk|thermo|spinner|cover","style":"terracotta|mint|lavender|rose","kicker","title","sub"}]
PINS = []
for p in json.load(open(sys.argv[1])):
    d = dict(STYLES[p["style"]]); d.update(p)
    if "photo" not in d: d["art"] = ARTS[p["art"]]  # pines con foto no usan dibujo
    PINS.append(d)

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

# Pin con FOTO de producto: {"file","photo":"products/<x>.jpg","style","kicker","title"} (sin "art" ni "sub").
# La foto (cuadrada, aprobada) va arriba a sangre y abajo una franja con kicker, título y botón.
PHOTO_TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(file:///usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf)}}
@font-face{{font-family:I;src:url(file:///usr/share/fonts/opentype/inter/Inter-Medium.otf)}}
*{{margin:0;box-sizing:border-box}} body{{width:1000px;height:1500px;background:{bg};font-family:I;color:{ink};overflow:hidden;display:flex;flex-direction:column}}
.ph{{width:1000px;height:1000px;background:url('{photo_uri}') center/cover}}
.band{{flex:1;display:flex;flex-direction:column;padding:38px 70px 30px}}
.k{{font-family:P;letter-spacing:6px;font-size:26px;color:{accent}}}
h1{{font-family:P;font-size:{tsize}px;line-height:1.08;margin:12px 0 auto}}
.row{{display:flex;justify-content:space-between;align-items:center}}
.cta{{background:{ink};color:{bg};font-family:P;font-size:30px;padding:18px 34px;border-radius:60px}}
.f{{font-size:20px;opacity:.7;text-align:right;line-height:1.35}}
</style></head><body><div class="ph"></div><div class="band"><div class="k">{kicker}</div><h1>{title}</h1>
<div class="row"><div class="cta">See it on Amazon &rarr;</div><div class="f">Nice Finds &middot; Affiliate link<br>Illustrative image</div></div></div></body></html>"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1000, "height": 1500})
        for d in PINS:
            if "photo" in d:
                d["photo_uri"] = (OUT.parent / d["photo"]).resolve().as_uri()
                d["tsize"] = 64 if len(d["title"]) <= 34 else 54 if len(d["title"]) <= 52 else 46
                html = PHOTO_TPL.format(**d)
            else:
                svg = d["art"].format(**d)
                html = TPL.format(svg=svg, **d)
            import tempfile; f = pathlib.Path(tempfile.gettempdir()) / f"{d['file']}.html"; f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{d['file']}.png"))
        await b.close()

asyncio.run(main())
