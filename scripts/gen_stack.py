"""Builds assets/tech-stack.svg. Logo paths in icons.json come from Simple Icons (CC0, simpleicons.org)."""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "assets", "tech-stack.svg")
ICONS = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))

# (icon slug, label, logo colour) - dark brand colours are lightened so they read on the dark glass
TOOLS = [
    ("typescript", "TypeScript", "#3178C6"),
    ("javascript", "JavaScript", "#F7DF1E"),
    ("python", "Python", "#5A9FD4"),
    ("react", "React", "#61DAFB"),
    ("nextdotjs", "Next.js", "#FFFFFF"),
    ("tailwindcss", "Tailwind CSS", "#38BDF8"),
    ("nodedotjs", "Node.js", "#6CC24A"),
    ("graphql", "GraphQL", "#E10098"),
    ("postgresql", "PostgreSQL", "#6E9BEF"),
    ("redis", "Redis", "#FF4438"),
    ("shopify", "Shopify", "#95BF47"),
    ("claude", "Claude", "#D97757"),
    ("docker", "Docker", "#2496ED"),
    ("git", "Git", "#F05032"),
    ("github", "GitHub", "#FFFFFF"),
    ("vercel", "Vercel", "#FFFFFF"),
]

W = 900
X0, X1 = 58, 842
IW = X1 - X0
PER_ROW = 8
GAP = 14
TW = (IW - GAP * (PER_ROW - 1)) / PER_ROW
TH = 98
LOGO = 32
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"

parts = []
add = parts.append
add(f'<text x="{X0}" y="70" class="eyebrow">TECH STACK</text>')
add(f'<text x="{X1}" y="70" class="meta" text-anchor="end">Languages, frameworks and tools</text>')

TY = 92
for i, (slug, label, color) in enumerate(TOOLS):
    row, col = divmod(i, PER_ROW)
    x = X0 + col * (TW + GAP)
    y = TY + row * (TH + GAP)
    cx = x + TW / 2
    s = LOGO / 24
    add(
        f'<rect x="{x:.1f}" y="{y}" width="{TW:.1f}" height="{TH}" rx="18" class="tile"/>'
        f'<circle cx="{cx:.1f}" cy="{y + 38}" r="24" fill="{color}" opacity=".22" filter="url(#glow)"/>'
        f'<g class="float" style="animation-delay:-{(i * 0.37) % 4:.2f}s">'
        f'<path transform="translate({cx - LOGO / 2:.1f},{y + 38 - LOGO / 2}) scale({s:.4f})" d="{ICONS[slug]}" fill="{color}"/></g>'
        f'<text x="{cx:.1f}" y="{y + TH - 16}" class="name" text-anchor="middle">{escape(label)}</text>'
    )

rows = -(-len(TOOLS) // PER_ROW)
H = int(TY + rows * TH + (rows - 1) * GAP + 42)

css = f"""
.eyebrow{{font:700 11.5px {FONT};letter-spacing:2.6px;fill:#9B88FF}}
.meta{{font:500 12.5px {FONT};fill:#A8A3C7}}
.name{{font:600 12px {FONT};fill:#E4DEFF}}
.tile{{fill:#FFFFFF;fill-opacity:.05;stroke:#FFFFFF;stroke-opacity:.10}}
.float{{animation:float 4s ease-in-out infinite alternate}}
@keyframes float{{from{{transform:translateY(2px)}}to{{transform:translateY(-3px)}}}}
.blob{{transform-box:fill-box;transform-origin:center}}
.b1{{animation:d1 18s ease-in-out infinite alternate}}
.b2{{animation:d2 22s ease-in-out infinite alternate}}
.b3{{animation:d3 26s ease-in-out infinite alternate}}
@keyframes d1{{0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(160px,30px) scale(1.2)}}}}
@keyframes d2{{0%{{transform:translate(0,0) scale(1.1)}}100%{{transform:translate(-180px,20px) scale(.9)}}}}
@keyframes d3{{0%{{transform:translate(0,0) scale(.9)}}100%{{transform:translate(-100px,-30px) scale(1.15)}}}}
.shine{{animation:sweep 9s ease-in-out infinite}}
@keyframes sweep{{0%,60%{{transform:translateX(-500px)}}100%{{transform:translateX({W + 300}px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Tech stack</title>
<desc id="d">{escape(", ".join(t[1] for t in TOOLS))}</desc>
<defs>
<style>{css}</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0A18"/><stop offset="1" stop-color="#140F2E"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".45"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity=".08"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".22"/></linearGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".09"/><stop offset=".35" stop-color="#FFFFFF" stop-opacity=".02"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="26"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g filter="url(#blur)" opacity=".7">
<circle class="blob b1" cx="120" cy="{H // 2}" r="140" fill="#6D4CFF"/>
<circle class="blob b2" cx="{W - 120}" cy="{H // 2}" r="150" fill="#EC4899" fill-opacity=".7"/>
<circle class="blob b3" cx="{W // 2}" cy="40" r="110" fill="#3B82F6" fill-opacity=".6"/>
</g>
<rect x="18" y="18" width="{W - 36}" height="{H - 36}" rx="20" fill="#FFFFFF" fill-opacity=".05"/>
<rect x="18" y="18" width="{W - 36}" height="{(H - 36) * .5:.0f}" rx="20" fill="url(#gloss)"/>
<g class="shine"><rect x="0" y="0" width="260" height="{H}" fill="url(#shineGrad)" transform="skewX(-20)"/></g>
<rect x="18.5" y="18.5" width="{W - 37}" height="{H - 37}" rx="20" fill="none" stroke="url(#edge)"/>
{''.join(parts)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="25.5" fill="none" stroke="#6D4CFF" stroke-opacity=".55"/>
</svg>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({W}x{H})")
