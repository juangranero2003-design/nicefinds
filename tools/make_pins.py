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

SHIELD = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M50 140 L270 140 Q262 270 160 285 Q58 270 50 140 Z" fill="{b}"/>
<ellipse cx="160" cy="140" rx="125" ry="30" fill="{a}" fill-opacity=".55"/>
<ellipse cx="160" cy="140" rx="70" ry="14" fill="{bg}"/>
<path d="M215 125 L260 45 L305 70 L270 140 Z" fill="{a}" fill-opacity=".55"/>
<line x1="160" y1="20" x2="160" y2="135"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><circle cx="282" cy="30" r="9"/><circle cx="262" cy="18" r="6"/><circle cx="300" cy="44" r="6"/></g></svg>"""

FROTHER = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M60 160 L220 160 L205 290 L75 290 Z" fill="{b}"/>
<path d="M220 185 Q270 185 265 225 Q260 260 212 258" fill="none"/>
<path d="M66 175 Q140 150 214 175 L212 195 L68 195 Z" fill="{bg}"/>
<rect x="125" y="20" width="40" height="95" rx="18" fill="{a}"/>
<line x1="145" y1="115" x2="145" y2="200" stroke-width="7"/>
<circle cx="145" cy="203" r="16" fill="none" stroke-width="6"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="5"><circle cx="145" cy="50" r="8"/></g></svg>"""

SINKRACK = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M30 40 L290 40 L290 300 L30 300 Z" fill="{b}"/>
<path d="M140 40 L140 80 Q140 100 160 100 Q180 100 180 80 L180 40" fill="none"/>
<rect x="50" y="130" width="220" height="60" rx="8" fill="{a}"/><rect x="50" y="220" width="220" height="60" rx="8" fill="{a}"/>
<line x1="50" y1="130" x2="50" y2="285"/><line x1="270" y1="130" x2="270" y2="285"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><rect x="75" y="98" width="34" height="48" rx="8"/><rect x="125" y="110" width="28" height="36" rx="6"/><rect x="200" y="190" width="40" height="45" rx="8"/><rect x="80" y="195" width="30" height="40" rx="6"/></g></svg>"""

MUGWARM = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="45" y="235" width="230" height="50" rx="16" fill="{a}"/>
<ellipse cx="160" cy="238" rx="80" ry="10" fill="{b}"/>
<path d="M100 110 L220 110 L212 232 L108 232 Z" fill="{b}"/>
<path d="M218 135 Q262 135 258 170 Q255 205 212 200" fill="none"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><circle cx="245" cy="260" r="9"/></g>
<g fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"><path d="M135 90 q14 -20 0 -40 q-14 -20 0 -40"/><path d="M185 90 q14 -20 0 -40 q-14 -20 0 -40"/></g></svg>"""

LIDS = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M30 200 L170 200 Q165 285 100 290 Q35 285 30 200 Z" fill="{b}"/>
<path d="M28 200 Q100 170 172 200 Q100 215 28 200 Z" fill="{a}" fill-opacity=".8"/>
<path d="M190 225 L300 225 Q296 290 245 292 Q194 290 190 225 Z" fill="{b}"/>
<path d="M188 225 Q245 202 302 225 Q245 238 188 225 Z" fill="{c}" fill-opacity=".8"/></g>
<g stroke="{ink}" stroke-width="7"><circle cx="120" cy="80" r="55" fill="{a}" fill-opacity=".7"/><circle cx="225" cy="105" r="42" fill="{c}" fill-opacity=".7"/><circle cx="180" cy="40" r="26" fill="{a}" fill-opacity=".45"/></g>
<g fill="none" stroke="{ink}" stroke-width="5"><circle cx="120" cy="80" r="30"/><circle cx="225" cy="105" r="22"/></g></svg>"""

WINE = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M95 300 L95 170 Q95 135 115 120 L115 70 L145 70 L145 120 Q165 135 165 170 L165 300 Z" fill="{a}"/>
<rect x="108" y="10" width="44" height="70" rx="14" fill="{ink}"/>
<path d="M215 170 L275 170 Q278 225 245 235 Q212 225 215 170 Z" fill="{b}"/>
<line x1="245" y1="235" x2="245" y2="290"/><line x1="220" y1="292" x2="270" y2="292"/>
<path d="M219 195 Q245 188 271 195 Q270 222 245 230 Q220 222 219 195 Z" fill="{c}" stroke-width="6"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><rect x="40" y="250" width="26" height="45" rx="8"/><circle cx="53" cy="243" r="11"/></g></svg>"""

NECKLIGHT = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="40" y="215" width="240" height="75" rx="10" fill="{b}"/><line x1="160" y1="215" x2="160" y2="290"/>
<path d="M90 60 Q160 10 230 60" fill="none" stroke-width="22"/>
<path d="M90 60 Q70 110 105 150" fill="none" stroke-width="12"/><path d="M230 60 Q250 110 215 150" fill="none" stroke-width="12"/>
<circle cx="108" cy="158" r="16" fill="{a}"/><circle cx="212" cy="158" r="16" fill="{a}"/></g>
<g fill="{c}" opacity=".45"><path d="M95 172 L60 215 L150 215 L122 172 Z"/><path d="M198 172 L170 215 L260 215 L225 172 Z"/></g></svg>"""

TURNTABLE = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<ellipse cx="160" cy="250" rx="135" ry="38" fill="{b}"/><path d="M25 235 L25 250 Q25 288 160 288 Q295 288 295 250 L295 235" fill="none"/>
<ellipse cx="160" cy="235" rx="135" ry="38" fill="{a}"/>
<rect x="75" y="130" width="40" height="95" rx="10" fill="{c}"/><rect x="140" y="150" width="40" height="80" rx="10" fill="{b}"/><rect x="205" y="120" width="40" height="105" rx="10" fill="{c}"/>
<rect x="80" y="112" width="30" height="22" rx="5" fill="{ink}"/><rect x="210" y="102" width="30" height="22" rx="5" fill="{ink}"/></g>
<g fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"><path d="M40 170 Q30 130 60 100"/><path d="M52 92 l10 6 -2 -12"/></g></svg>"""

SHREDDER = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="20" y="70" width="70" height="120" rx="14" fill="{a}"/>
<rect x="90" y="105" width="150" height="55" rx="12" fill="{b}"/>
<rect x="130" y="25" width="50" height="85" rx="8" fill="{b}"/><rect x="138" y="5" width="34" height="30" rx="6" fill="{c}"/>
<circle cx="250" cy="132" r="36" fill="{b}"/><circle cx="250" cy="132" r="16" fill="{c}"/>
<path d="M175 300 L195 225 L305 225 L320 300 Z" fill="{a}" fill-opacity=".5"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="5"><circle cx="240" cy="190" r="9"/><circle cx="262" cy="205" r="9"/><circle cx="248" cy="215" r="8"/></g></svg>"""

PASTRY = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M30 230 Q30 300 160 300 Q290 300 290 230 Z" fill="{b}"/><line x1="20" y1="230" x2="300" y2="230"/>
<rect x="145" y="10" width="30" height="55" rx="8" fill="{c}"/>
<path d="M160 65 L95 95 Q70 170 160 250 Q250 170 225 95 Z" fill="none"/>
<path d="M120 90 Q105 165 160 235" fill="none" stroke-width="7"/><path d="M160 75 L160 240" fill="none" stroke-width="7"/><path d="M200 90 Q215 165 160 235" fill="none" stroke-width="7"/></g>
<g fill="{a}" stroke="{ink}" stroke-width="5"><rect x="70" y="200" width="26" height="22" rx="4"/><rect x="230" y="205" width="24" height="20" rx="4"/></g></svg>"""

CANDLELAMP = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="40" y="275" width="160" height="28" rx="8" fill="{b}"/><line x1="70" y1="275" x2="70" y2="70"/>
<path d="M70 70 L120 70" fill="none"/><path d="M95 70 L190 70 Q200 130 160 135 L125 135 Q85 130 95 70 Z" fill="{a}"/>
<rect x="105" y="195" width="80" height="80" rx="12" fill="{c}"/><rect x="105" y="195" width="80" height="18" rx="6" fill="{b}"/></g>
<g fill="{a}" opacity=".35"><path d="M120 140 L95 195 L195 195 L170 140 Z"/></g>
<g fill="none" stroke="{ink}" stroke-width="5" stroke-linecap="round"><path d="M240 120 q15 -20 0 -40"/><path d="M265 140 q15 -20 0 -40"/></g></svg>"""

HERBSCISSORS = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="20" y="240" width="280" height="50" rx="10" fill="{b}"/>
<ellipse cx="80" cy="190" rx="38" ry="26" fill="{c}"/><ellipse cx="90" cy="110" rx="38" ry="26" fill="{c}"/>
<path d="M115 175 L250 120" fill="none"/><path d="M120 125 L250 120" fill="none"/></g>
<g stroke="{ink}" stroke-width="6" stroke-linecap="round"><line x1="150" y1="110" x2="285" y2="75"/><line x1="150" y1="122" x2="290" y2="92"/><line x1="150" y1="134" x2="292" y2="109"/><line x1="150" y1="146" x2="290" y2="126"/><line x1="150" y1="158" x2="285" y2="143"/></g>
<g fill="{a}" stroke="{ink}" stroke-width="5"><path d="M180 255 q12 -20 26 0 q-12 12 -26 0z"/><path d="M215 262 q12 -20 26 0 q-12 12 -26 0z"/><path d="M150 265 q12 -18 24 0 q-12 10 -24 0z"/></g></svg>"""

DESKPAD = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M15 270 L60 150 L300 150 L305 270 Z" fill="{b}"/>
<path d="M45 255 L80 165 L280 165 L285 255 Z" fill="{c}"/>
<rect x="110" y="60" width="110" height="80" rx="8" fill="{a}"/><path d="M95 140 L235 140" fill="none"/>
<rect x="110" y="195" width="120" height="35" rx="8" fill="{b}"/><ellipse cx="258" cy="215" rx="13" ry="18" fill="{b}"/></g>
<g fill="{a}" stroke="{ink}" stroke-width="6"><path d="M30 120 h40 v30 h-40 z"/><path d="M70 125 q15 0 15 12 q0 12 -15 12" fill="none"/></g></svg>"""

HOLDERS = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="20" y="20" width="280" height="290" rx="14" fill="{b}"/>
<rect x="40" y="50" width="50" height="26" rx="8" fill="{a}"/><rect x="135" y="50" width="50" height="26" rx="8" fill="{a}"/><rect x="230" y="50" width="50" height="26" rx="8" fill="{a}"/>
<line x1="65" y1="76" x2="65" y2="115"/><path d="M65 115 L35 150 Q35 240 65 260 Q95 240 95 150 Z" fill="{c}"/><path d="M65 130 L50 160 Q52 215 65 235 Q78 215 80 160 Z" fill="{b}"/>
<line x1="160" y1="76" x2="160" y2="120"/><path d="M160 120 Q120 150 150 190 Q175 225 145 265" fill="none"/>
<line x1="255" y1="76" x2="255" y2="115"/><path d="M255 115 Q215 180 255 270 Q295 180 255 115 Z" fill="none"/><path d="M255 115 Q235 190 255 270" fill="none" stroke-width="6"/><path d="M255 115 Q275 190 255 270" fill="none" stroke-width="6"/></g></svg>"""

HANDWARM = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<rect x="45" y="70" width="110" height="170" rx="48" fill="{a}"/><rect x="165" y="70" width="110" height="170" rx="48" fill="{a}"/>
<line x1="160" y1="85" x2="160" y2="225" stroke="{c}" stroke-dasharray="6 14"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="5"><circle cx="85" cy="200" r="8"/><circle cx="100" cy="200" r="8"/><circle cx="115" cy="200" r="8"/></g>
<g fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"><path d="M110 50 q14 -18 0 -36"/><path d="M160 50 q14 -18 0 -36"/><path d="M210 50 q14 -18 0 -36"/></g>
<g fill="{b}" stroke="{ink}" stroke-width="6"><path d="M290 250 l8 17 19 3 -14 13 4 19 -17 -9 -17 9 4 -19 -14 -13 19 -3z"/></g></svg>"""

SCALE = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M30 230 L60 150 L260 150 L290 230 Z" fill="{b}"/><path d="M30 230 L290 230 L290 262 Q290 275 277 275 L43 275 Q30 275 30 262 Z" fill="{a}"/>
<rect x="115" y="238" width="90" height="28" rx="5" fill="{bg}"/><circle cx="70" cy="252" r="8" fill="{ink}"/><circle cx="250" cy="252" r="8" fill="{ink}"/>
<path d="M95 175 Q160 120 225 175 Z" fill="{c}"/></g>
<g fill="{c}" stroke="{ink}" stroke-width="6"><circle cx="130" cy="95" r="22"/><circle cx="185" cy="100" r="18"/></g>
<g fill="{ink}"><rect x="128" y="247" width="64" height="10" rx="3"/></g></svg>"""

CANRACK = """<svg viewBox="0 0 320 320" width="430"><g stroke="{ink}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round">
<path d="M40 40 L40 300 M280 40 L280 300" fill="none"/>
<path d="M40 70 L280 100 M40 130 L280 100 M40 160 L280 190 M40 220 L280 190 M40 250 L280 280" fill="none"/>
<g fill="{a}"><rect x="70" y="40" width="44" height="40" rx="6" transform="rotate(7 92 60)"/><rect x="190" y="55" width="44" height="40" rx="6" transform="rotate(7 212 75)"/>
<rect x="190" y="138" width="44" height="40" rx="6" transform="rotate(-7 212 158)"/><rect x="70" y="190" width="44" height="40" rx="6" transform="rotate(7 92 210)"/><rect x="150" y="205" width="44" height="40" rx="6" transform="rotate(7 172 225)"/></g></g>
<g fill="{c}"><rect x="76" y="54" width="32" height="10" transform="rotate(7 92 60)"/><rect x="196" y="69" width="32" height="10" transform="rotate(7 212 75)"/><rect x="196" y="152" width="32" height="10" transform="rotate(-7 212 158)"/><rect x="76" y="204" width="32" height="10" transform="rotate(7 92 210)"/><rect x="156" y="219" width="32" height="10" transform="rotate(7 172 225)"/></g></svg>"""

import json, sys
STYLES = {
  "terracotta": dict(bg="#F3E9DC", a="#C8553D", b="#F2D0A4", c="#2D6A4F", ink="#2B2118", accent="#C8553D"),
  "mint": dict(bg="#E8F1EE", a="#9AD1C0", b="#F4A261", c="#E9C46A", ink="#1D3540", accent="#E76F51"),
  "lavender": dict(bg="#EEEAF6", a="#B8A9E3", b="#FFFFFF", c="#F28482", ink="#2A2440", accent="#6C5CE7"),
  "rose": dict(bg="#FBE8EA", a="#E8A0A8", b="#FFFFFF", c="#B5485A", ink="#3A1F25", accent="#B5485A"),
}
ARTS = {"cart": CART, "mixer": MIXER, "mitt": MITT, "blanket": BLANKET, "desk": DESK, "thermo": THERMO, "spinner": SPINNER, "cover": COVER,
        "shield": SHIELD, "frother": FROTHER, "sinkrack": SINKRACK, "mugwarm": MUGWARM, "lids": LIDS,
        "wine": WINE, "necklight": NECKLIGHT, "turntable": TURNTABLE, "shredder": SHREDDER,
        "pastry": PASTRY, "candlelamp": CANDLELAMP, "herbscissors": HERBSCISSORS, "deskpad": DESKPAD,
        "holders": HOLDERS, "handwarm": HANDWARM, "scale": SCALE, "canrack": CANRACK}
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
