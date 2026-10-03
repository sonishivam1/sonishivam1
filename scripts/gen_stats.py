"""Builds assets/stats.svg from the GitHub GraphQL API. Needs GITHUB_TOKEN; STATS_JSON=<file> renders from a saved response instead."""
import datetime as dt
import json
import os
import urllib.request
from xml.sax.saxutils import escape

LOGIN = os.environ.get("GITHUB_LOGIN", "sonishivam1")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "stats.svg")

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch():
    if os.environ.get("STATS_JSON"):
        with open(os.environ["STATS_JSON"], encoding="utf-8") as f:
            return json.load(f)["data"]["user"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]


u = fetch()
cc = u["contributionsCollection"]
weeks = cc["contributionCalendar"]["weeks"]
days = [(dt.date.fromisoformat(d["date"]), d["contributionCount"]) for w in weeks for d in w["contributionDays"]]
total = cc["contributionCalendar"]["totalContributions"]

# streaks: a zero today doesn't break the current streak until the day is over
cur = 0
cur_start = None
idx = len(days) - 1
if days[idx][1] == 0:
    idx -= 1
while idx >= 0 and days[idx][1] > 0:
    cur += 1
    cur_start = days[idx][0]
    idx -= 1

best = run = 0
best_range = None
run_start = None
for d, c in days:
    if c > 0:
        run += 1
        run_start = run_start or d
        if run > best:
            best, best_range = run, (run_start, d)
    else:
        run, run_start = 0, None

busiest_day, busiest = max(days, key=lambda x: x[1])

stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
lang_bytes = {}
lang_color = {}
for r in u["repositories"]["nodes"]:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]
        lang_bytes[n] = lang_bytes.get(n, 0) + e["size"]
        lang_color[n] = e["node"]["color"] or "#8B8B9E"
lang_total = sum(lang_bytes.values()) or 1
langs = sorted(lang_bytes.items(), key=lambda x: -x[1])[:6]


def fmt(n):
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def md(d):
    return f"{d.strftime('%b')} {d.day}"


# ---------- layout ----------
W = 900
X0, X1 = 58, 842
IW = X1 - X0
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
NARROW = set("iljtf.,:;'|!()[] ")


def text_w(s, size):
    return sum(0.30 if ch in NARROW else 0.64 if ch.isupper() else 0.56 if ch.isdigit() else 0.53 for ch in s) * size


parts = []
add = parts.append
today = days[-1][0]

add(f'<text x="{X0}" y="70" class="eyebrow">GITHUB IN NUMBERS</text>')
add(f'<text x="{X1}" y="70" class="meta" text-anchor="end">Last 12 months  ·  updated {today.day} {today.strftime("%b %Y")}</text>')

tiles = [
    ("CONTRIBUTIONS", fmt(total), "in the last year"),
    ("CURRENT STREAK", f"{cur} day{'s' if cur != 1 else ''}", f"since {md(cur_start)}" if cur else "starts with the next commit"),
    ("BEST STREAK", f"{best} day{'s' if best != 1 else ''}", f"{md(best_range[0])} – {md(best_range[1])}" if best else "no streak yet"),
    ("BUSIEST DAY", fmt(busiest), f"contributions on {md(busiest_day)}"),
]
TY, TH, GAP = 90, 104, 14
tw = (IW - GAP * 3) / 4
for i, (label, value, sub) in enumerate(tiles):
    x = X0 + i * (tw + GAP)
    add(
        f'<rect x="{x:.1f}" y="{TY}" width="{tw:.1f}" height="{TH}" rx="16" class="tile"/>'
        f'<rect x="{x + 18:.1f}" y="{TY + 18}" width="22" height="3" rx="1.5" fill="url(#g{i})"/>'
        f'<text x="{x + 18:.1f}" y="{TY + 40}" class="label">{label}</text>'
        f'<text x="{x + 18:.1f}" y="{TY + 74}" class="big">{escape(value)}</text>'
        f'<text x="{x + 18:.1f}" y="{TY + 93}" class="sub">{escape(sub)}</text>'
    )

pills = [
    ("Commits", cc["totalCommitContributions"]),
    ("Pull requests", cc["totalPullRequestContributions"]),
    ("Code reviews", cc["totalPullRequestReviewContributions"]),
    ("Private contributions", cc["restrictedContributionsCount"]),
    ("Repositories", u["repositories"]["totalCount"]),
    ("Stars", stars),
]
PY, PH = TY + TH + 14, 32
widths = [text_w(lbl, 12.5) + text_w(fmt(v), 13.5) * 1.08 + 38 for lbl, v in pills]
spare = (IW - sum(widths)) / (len(pills) - 1)
if spare < 6:
    pills = pills[:5]
    widths = widths[:5]
    spare = (IW - sum(widths)) / (len(pills) - 1)
x = X0
for (lbl, v), pw in zip(pills, widths):
    add(
        f'<rect x="{x:.1f}" y="{PY}" width="{pw:.1f}" height="{PH}" rx="16" class="pill"/>'
        f'<text x="{x + 14:.1f}" y="{PY + 21}" class="pilltext">{lbl} <tspan class="pillnum" dx="4">{fmt(v)}</tspan></text>'
    )
    x += pw + spare

# ---------- contribution calendar ----------
CY = PY + PH + 46
add(f'<text x="{X0}" y="{CY}" class="eyebrow">CONTRIBUTION CALENDAR</text>')
LEGEND = ["#FFFFFF", "#6D4CFF", "#7C5CFF", "#9B7BFF", "#EC4899"]
OPAC = [0.06, 0.38, 0.62, 0.9, 0.95]
nonzero = sorted(c for _, c in days if c > 0)


def level(c):
    if c == 0 or not nonzero:
        return 0
    q = [nonzero[int(len(nonzero) * p)] for p in (0.25, 0.5, 0.75)]
    return 1 + sum(c > t for t in q)


lx = X1 - 5 * 15 - text_w("Less", 11) - text_w("More", 11) - 14
add(f'<text x="{lx:.1f}" y="{CY}" class="meta small">Less</text>')
lx += text_w("Less", 11) + 6
for i in range(5):
    add(f'<rect x="{lx:.1f}" y="{CY - 10}" width="11" height="11" rx="3" fill="{LEGEND[i]}" fill-opacity="{OPAC[i]}"/>')
    lx += 15
add(f'<text x="{lx + 2:.1f}" y="{CY}" class="meta small">More</text>')

GX = X0 + 30
GY = CY + 34
step = (X1 - GX) / len(weeks)
cell = step * 0.8
last_label_x = -99
for wi, w in enumerate(weeks):
    first = dt.date.fromisoformat(w["contributionDays"][0]["date"])
    cx = GX + wi * step
    if (wi == 0 or first.day <= 7) and cx - last_label_x > 34:
        add(f'<text x="{cx:.1f}" y="{GY - 9}" class="meta small">{first.strftime("%b")}</text>')
        last_label_x = cx
    for d in w["contributionDays"]:
        date = dt.date.fromisoformat(d["date"])
        row = (date.weekday() + 1) % 7
        lv = level(d["contributionCount"])
        cls = ' class="today"' if date == today else ""
        add(
            f'<rect{cls} x="{cx:.1f}" y="{GY + row * step:.1f}" width="{cell:.1f}" height="{cell:.1f}" rx="3" '
            f'fill="{LEGEND[lv]}" fill-opacity="{OPAC[lv]}"><title>{d["contributionCount"]} on {md(date)}</title></rect>'
        )
for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    add(f'<text x="{X0}" y="{GY + row * step + cell - 1:.1f}" class="meta small">{name}</text>')

# ---------- languages ----------
LY = GY + 7 * step + 44
add(f'<text x="{X0}" y="{LY}" class="eyebrow">TOP LANGUAGES</text>')
add(f'<text x="{X1}" y="{LY}" class="meta small" text-anchor="end">by code size across public repositories</text>')
BY = LY + 16
add(f'<clipPath id="bar"><rect x="{X0}" y="{BY}" width="{IW}" height="10" rx="5"/></clipPath><g clip-path="url(#bar)">')
bx = X0
shown_total = sum(b for _, b in langs) or 1
for name, b in langs:
    sw = IW * b / shown_total
    add(f'<rect x="{bx:.1f}" y="{BY}" width="{sw + 0.5:.1f}" height="10" fill="{lang_color[name]}"/>')
    bx += sw
add("</g>")
lx = X0
ly = BY + 36
for name, b in langs:
    label = f"{name}  {100 * b / lang_total:.1f}%"
    w = text_w(label, 12.5) + 30
    if lx + w > X1:
        lx = X0
        ly += 24
    add(
        f'<circle cx="{lx + 5}" cy="{ly - 4.5}" r="5" fill="{lang_color[name]}"/>'
        f'<text x="{lx + 16}" y="{ly}" class="langtext">{escape(name)} <tspan class="meta">{100 * b / lang_total:.1f}%</tspan></text>'
    )
    lx += w

H = int(ly + 48)

css = f"""
.eyebrow{{font:700 11.5px {FONT};letter-spacing:2.6px;fill:#9B88FF}}
.label{{font:700 10.5px {FONT};letter-spacing:1.6px;fill:#A8A3C7}}
.big{{font:800 30px {FONT};fill:url(#numGrad);letter-spacing:-0.5px}}
.sub{{font:500 12px {FONT};fill:#A8A3C7}}
.meta{{font:500 12.5px {FONT};fill:#A8A3C7}}
.small{{font-size:11px}}
.tile{{fill:#FFFFFF;fill-opacity:.05;stroke:#FFFFFF;stroke-opacity:.10}}
.pill{{fill:#FFFFFF;fill-opacity:.045;stroke:#9B88FF;stroke-opacity:.28}}
.pilltext{{font:500 12.5px {FONT};fill:#C9C3EA}}
.pillnum{{font:800 13.5px {FONT};fill:#FFFFFF}}
.langtext{{font:600 12.5px {FONT};fill:#F2EFFF}}
.blob{{transform-box:fill-box;transform-origin:center}}
.b1{{animation:d1 18s ease-in-out infinite alternate}}
.b2{{animation:d2 22s ease-in-out infinite alternate}}
.b3{{animation:d3 26s ease-in-out infinite alternate}}
@keyframes d1{{0%{{transform:translate(0,0) scale(1)}}100%{{transform:translate(140px,80px) scale(1.25)}}}}
@keyframes d2{{0%{{transform:translate(0,0) scale(1.1)}}100%{{transform:translate(-160px,-70px) scale(.9)}}}}
@keyframes d3{{0%{{transform:translate(0,0) scale(.9)}}100%{{transform:translate(-90px,90px) scale(1.2)}}}}
.shine{{animation:sweep 9s ease-in-out infinite}}
@keyframes sweep{{0%,60%{{transform:translateX(-500px)}}100%{{transform:translateX({W + 300}px)}}}}
.today{{stroke:#F9A8D4;stroke-width:1.5;animation:glow 1.6s ease-in-out infinite alternate}}
@keyframes glow{{from{{stroke-opacity:1}}to{{stroke-opacity:.15}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

grads = "".join(
    f'<linearGradient id="g{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
    for i, (a, b) in enumerate([("#6D4CFF", "#EC4899"), ("#10B981", "#3B82F6"), ("#F59E0B", "#EC4899"), ("#3B82F6", "#6D4CFF")])
)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">GitHub stats for {LOGIN}</title>
<desc id="d">{total} contributions in the last year. Current streak {cur} days, best streak {best} days. {cc["totalCommitContributions"]} commits, {cc["totalPullRequestContributions"]} pull requests, {stars} stars.</desc>
<defs>
<style>{css}</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0A18"/><stop offset="1" stop-color="#140F2E"/></linearGradient>
<linearGradient id="numGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DDD6FE"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".45"/><stop offset=".4" stop-color="#FFFFFF" stop-opacity=".08"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".22"/></linearGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".09"/><stop offset=".35" stop-color="#FFFFFF" stop-opacity=".02"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
{grads}
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<clipPath id="card"><rect width="{W}" height="{H}" rx="26"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g filter="url(#blur)" opacity=".7">
<circle class="blob b1" cx="140" cy="{H - 120}" r="160" fill="#6D4CFF"/>
<circle class="blob b2" cx="{W - 130}" cy="110" r="170" fill="#EC4899" fill-opacity=".7"/>
<circle class="blob b3" cx="{W // 2}" cy="{H - 60}" r="130" fill="#3B82F6" fill-opacity=".6"/>
</g>
<rect x="18" y="18" width="{W - 36}" height="{H - 36}" rx="20" fill="#FFFFFF" fill-opacity=".05"/>
<rect x="18" y="18" width="{W - 36}" height="{(H - 36) * .4:.0f}" rx="20" fill="url(#gloss)"/>
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
print(f"wrote {OUT} ({W}x{H}); {total} contributions, streak {cur}, best {best}")
