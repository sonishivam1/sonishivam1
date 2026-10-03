import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "about-me.svg")

W = 900
PAD = 40
SPLIT = 430
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'Cascadia Code', 'SF Mono', Consolas, 'Liberation Mono', monospace"

NARROW = set("iljtf.,:;'|!()[] ")
WIDE = set("mwMW@")


def text_w(s, size, weight=1.0):
    w = 0.0
    for ch in s:
        if ch in NARROW:
            w += 0.30
        elif ch in WIDE:
            w += 0.82
        elif ch.isupper():
            w += 0.64
        elif ch.isdigit():
            w += 0.56
        else:
            w += 0.53
    return w * size * weight


STACK = [
    ("Frontend", "#B4A2FF", ["Next.js 14", "React", "TypeScript", "TailwindCSS"]),
    ("Backend", "#7CB8FF", ["Node.js", "tRPC", "REST", "GraphQL"]),
    ("Commerce", "#F59ACB", ["commercetools", "Shopify Plus", "BigCommerce", "Adobe Commerce"]),
    ("AI", "#6EE7B7", ["Claude API", "LLM Agents", "Autonomous Workflows"]),
    ("Infra", "#FCD38A", ["Vercel Edge", "Docker", "PostgreSQL", "Redis"]),
]

BUILDING = [
    ("Royal Cyber CSA", "Customer Service Accelerator"),
    ("Commerce Orchestrator", "Multi-tenant data orchestration"),
    ("AI tooling", "Agents for enterprise workflows"),
]

parts = []
add = parts.append

# ---------- right column: stack chips ----------
rx0 = SPLIT + 30
rx1 = W - PAD - 6
y = 70
right = []
right.append(f'<text x="{rx0}" y="{y}" class="eyebrow">TECH STACK</text>')
y += 26
CH = 26
for label, color, chips in STACK:
    right.append(f'<text x="{rx0}" y="{y}" class="label" fill="{color}">{label.upper()}</text>')
    y += 10
    x = rx0
    for c in chips:
        cw = text_w(c, 12.5, 1.04) + 24
        if x + cw > rx1:
            x = rx0
            y += CH + 8
        right.append(
            f'<g class="chip"><rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{CH}" rx="13" '
            f'fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.38"/>'
            f'<text x="{x + cw / 2:.1f}" y="{y + 17.5}" class="chiptext" text-anchor="middle">{escape(c)}</text></g>'
        )
        x += cw + 8
    y += CH + 34
right_end = y - 34

# ---------- left column ----------
lx = PAD + 26
left = []
ly = 70
left.append(f'<text x="{lx}" y="{ly}" class="eyebrow">ABOUT ME</text>')
ly += 46
left.append(f'<text x="{lx}" y="{ly}" class="name">Shivam Soni</text>')
ly += 30
left.append(f'<text x="{lx}" y="{ly}" class="role">Full-Stack Engineer <tspan class="sep">/</tspan> Royal Cyber</text>')
ly += 28
# location pin + live dot
left.append(
    f'<g transform="translate({lx},{ly - 12})"><path d="M6 0C2.7 0 0 2.6 0 5.9 0 10.3 6 15 6 15s6-4.7 6-9.1C12 2.6 9.3 0 6 0zm0 8.2a2.3 2.3 0 1 1 0-4.6 2.3 2.3 0 0 1 0 4.6z" fill="#9B88FF"/></g>'
    f'<text x="{lx + 20}" y="{ly}" class="meta">Prayagraj, India</text>'
)
ly += 30
left.append(f'<line x1="{lx}" y1="{ly}" x2="{SPLIT - 10}" y2="{ly}" class="rule"/>')
ly += 34
left.append(f'<text x="{lx}" y="{ly}" class="eyebrow">CURRENTLY BUILDING</text>')
dot_x = lx + text_w("CURRENTLY BUILDING", 11.5, 1.08) + 2.6 * 18 + 14
left.append(
    f'<circle cx="{dot_x:.1f}" cy="{ly - 4}" r="3.5" fill="#34D399"/>'
    f'<circle cx="{dot_x:.1f}" cy="{ly - 4}" r="3.5" fill="none" stroke="#34D399" class="pulse"/>'
)
ly += 14
row_w = SPLIT - 10 - lx
for i, (title, sub) in enumerate(BUILDING):
    left.append(
        f'<g class="row"><rect x="{lx}" y="{ly}" width="{row_w}" height="46" rx="12" class="rowbg"/>'
        f'<rect x="{lx + 12}" y="{ly + 13}" width="20" height="20" rx="6" fill="url(#g{i})"/>'
        f'<text x="{lx + 44}" y="{ly + 20}" class="rowtitle">{escape(title)}</text>'
        f'<text x="{lx + 44}" y="{ly + 36}" class="rowsub">{escape(sub)}</text></g>'
    )
    ly += 54
ly += 26
left.append(f'<text x="{lx}" y="{ly}" class="eyebrow">CURRENT FOCUS</text>')
ly += 26
left.append(f'<text x="{lx}" y="{ly}" class="focus">Unifying commerce, CRM, OMS and ERP</text>')
ly += 22
left.append(f'<text x="{lx}" y="{ly}" class="focus">into one intelligent workspace<tspan class="cursor">_</tspan></text>')
left_end = ly

H = int(max(left_end, right_end) + 52)

css = f"""
.eyebrow{{font:700 11.5px {FONT};letter-spacing:2.6px;fill:#9B88FF}}
.label{{font:700 10.5px {FONT};letter-spacing:1.8px}}
.name{{font:800 36px {FONT};fill:url(#nameGrad);letter-spacing:-0.5px}}
.role{{font:600 15px {FONT};fill:#E4DEFF}}
.sep{{fill:#6D4CFF}}
.meta{{font:500 13.5px {FONT};fill:#A8A3C7}}
.rule{{stroke:#FFFFFF;stroke-opacity:.10}}
.rowbg{{fill:#FFFFFF;fill-opacity:.045;stroke:#FFFFFF;stroke-opacity:.09}}
.rowtitle{{font:700 14px {FONT};fill:#FFFFFF}}
.rowsub{{font:500 12px {FONT};fill:#A8A3C7}}
.focus{{font:500 15px {MONO};fill:#DDD6FE}}
.chiptext{{font:600 12.5px {FONT};fill:#F2EFFF}}
.blob{{transform-box:fill-box;transform-origin:center}}
.b1{{animation:d1 18s ease-in-out infinite alternate}}
.b2{{animation:d2 22s ease-in-out infinite alternate}}
.b3{{animation:d3 26s ease-in-out infinite alternate}}
@keyframes d1{{0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(120px,60px) scale(1.25)}}}}
@keyframes d2{{0%{{transform:translate(0,0) scale(1.1)}}100%{{transform:translate(-140px,-50px) scale(.9)}}}}
@keyframes d3{{0%{{transform:translate(0,0) scale(.9)}}100%{{transform:translate(-80px,70px) scale(1.2)}}}}
.shine{{animation:sweep 9s ease-in-out infinite}}
@keyframes sweep{{0%,60%{{transform:translateX(-500px)}}100%{{transform:translateX({W + 300}px)}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3);opacity:0}}}}
.cursor{{fill:#EC4899;animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

grads = "".join(
    f'<linearGradient id="g{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
    for i, (a, b) in enumerate([("#6D4CFF", "#EC4899"), ("#3B82F6", "#6D4CFF"), ("#10B981", "#3B82F6")])
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">About Shivam Soni</title>
<desc id="d">Full-Stack Engineer at Royal Cyber in Prayagraj, India. Building Royal Cyber CSA, a commerce orchestration platform and AI tooling. Stack: Next.js, React, TypeScript, Node.js, commercetools, Shopify, Claude API, PostgreSQL and Redis.</desc>
<defs>
<style>{css}</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0A18"/><stop offset="1" stop-color="#140F2E"/></linearGradient>
<linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#DDD6FE"/><stop offset="1" stop-color="#F9A8D4"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".45"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity=".08"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".22"/></linearGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".09"/><stop offset=".35" stop-color="#FFFFFF" stop-opacity=".02"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
{grads}
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="26"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g filter="url(#blur)" opacity=".75">
<circle class="blob b1" cx="150" cy="110" r="150" fill="#6D4CFF"/>
<circle class="blob b2" cx="{W - 140}" cy="{H - 90}" r="170" fill="#EC4899" fill-opacity=".75"/>
<circle class="blob b3" cx="{W - 260}" cy="70" r="120" fill="#3B82F6" fill-opacity=".7"/>
</g>
<rect x="18" y="18" width="{W - 36}" height="{H - 36}" rx="20" fill="#FFFFFF" fill-opacity=".05"/>
<rect x="18" y="18" width="{W - 36}" height="{(H - 36) * .5:.0f}" rx="20" fill="url(#gloss)"/>
<g class="shine"><rect x="0" y="0" width="260" height="{H}" fill="url(#shineGrad)" transform="skewX(-20)"/></g>
<rect x="18.5" y="18.5" width="{W - 37}" height="{H - 37}" rx="20" fill="none" stroke="url(#edge)"/>
<line x1="{SPLIT + 4}" y1="56" x2="{SPLIT + 4}" y2="{H - 56}" class="rule"/>
{''.join(left)}
{''.join(right)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="25.5" fill="none" stroke="#6D4CFF" stroke-opacity=".55"/>
</svg>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(OUT, W, H)
