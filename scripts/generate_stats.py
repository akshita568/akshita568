
import os
import requests

token = os.environ["CODOLIO_TOKEN"]

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(
    "https://api.codolio.com/user",
    headers=headers,
    timeout=30
)

response.raise_for_status()

data = response.json()["data"]["platformProfiles"]["platformProfiles"]

leetcode = next(p for p in data if p["platform"] == "leetcode")
gfg = next(p for p in data if p["platform"] == "geeksforgeeks")
cf = next(p for p in data if p["platform"] == "codeforces")

# --------------------
# Stats
# --------------------

lc_solved = leetcode["totalQuestionStats"]["totalQuestionCounts"]
lc_rating = leetcode["userStats"]["currentRating"]
lc_peak = leetcode["userStats"]["maxRating"]
lc_active = leetcode["dailyActivityStatsResponse"]["totalActiveDays"]
lc_streak = leetcode["dailyActivityStatsResponse"]["maxStreak"]

gfg_solved = gfg["totalQuestionStats"]["totalQuestionCounts"]
cf_solved = cf["totalQuestionStats"]["totalQuestionCounts"]

contest_history = leetcode["contestActivityStats"]["contestActivityList"]
ratings = [c["rating"] for c in contest_history]

# --------------------
# GRAPH CONFIG
# --------------------

GRAPH_LEFT = 420
GRAPH_TOP = 120

GRAPH_WIDTH = 730
GRAPH_HEIGHT = 360

PADDING = 30

min_rating = min(ratings)
max_rating = max(ratings)

if min_rating == max_rating:
    max_rating += 1

points = []

for i, rating in enumerate(ratings):

    if len(ratings) == 1:
        x = GRAPH_LEFT + GRAPH_WIDTH / 2
    else:
        x = GRAPH_LEFT + (
            i * GRAPH_WIDTH / (len(ratings) - 1)
        )

    usable_height = GRAPH_HEIGHT - PADDING * 2

    y = (
        GRAPH_TOP
        + GRAPH_HEIGHT
        - PADDING
        - (
            (rating - min_rating)
            / (max_rating - min_rating)
        )
        * usable_height
    )

    points.append((x, y, rating))

polyline_points = " ".join(
    f"{x},{y}" for x, y, _ in points
)

area_points = (
    f"{points[0][0]},{GRAPH_TOP + GRAPH_HEIGHT} "
    + polyline_points +
    f" {points[-1][0]},{GRAPH_TOP + GRAPH_HEIGHT}"
)

dots = ""

for x, y, rating in points:
    dots += f"""
    <circle cx="{x}" cy="{y}" r="5" fill="#a855f7"/>

    <text
        x="{x-15}"
        y="{y-12}"
        fill="white"
        font-size="12"
        font-family="Arial">
        {rating}
    </text>
    """

# --------------------
# SVG
# --------------------

svg = f"""
<svg width="1200"
     height="650"
     xmlns="http://www.w3.org/2000/svg">

<defs>

<linearGradient id="areaGradient"
                x1="0"
                y1="0"
                x2="0"
                y2="1">

<stop offset="0%"
      stop-color="#a855f7"
      stop-opacity="0.45"/>

<stop offset="100%"
      stop-color="#a855f7"
      stop-opacity="0"/>

</linearGradient>

<clipPath id="graphClip">

<rect
x="{GRAPH_LEFT}"
y="{GRAPH_TOP}"
width="{GRAPH_WIDTH}"
height="{GRAPH_HEIGHT}"
rx="12"/>

</clipPath>

</defs>

<style>

.title {{
fill:white;
font-size:28px;
font-weight:bold;
font-family:Arial;
}}

.card {{
fill:#161b22;
stroke:#30363d;
stroke-width:1;
}}

.label {{
fill:#8b949e;
font-size:14px;
font-family:Arial;
}}

.value {{
fill:white;
font-size:26px;
font-weight:bold;
font-family:Arial;
}}

</style>

<rect width="100%"
      height="100%"
      fill="#0d1117"
      rx="20"/>

<text x="30"
      y="45"
      class="title">
LeetCode Analytics
</text>

<!-- LEFT PANEL -->

<rect x="25" y="80" width="340" height="90" rx="14" class="card"/>
<text x="45" y="110" class="label">Current Rating</text>
<text x="45" y="145" class="value">{lc_rating}</text>

<rect x="25" y="190" width="340" height="90" rx="14" class="card"/>
<text x="45" y="220" class="label">Peak Rating</text>
<text x="45" y="255" class="value">{lc_peak}</text>

<rect x="25" y="300" width="340" height="90" rx="14" class="card"/>
<text x="45" y="330" class="label">Problems Solved</text>
<text x="45" y="365" class="value">{lc_solved}</text>

<rect x="25" y="410" width="340" height="90" rx="14" class="card"/>
<text x="45" y="440" class="label">Max Streak</text>
<text x="45" y="475" class="value">{lc_streak} days</text>

<!-- GRAPH PANEL -->

<rect
x="390"
y="80"
width="780"
height="450"
rx="16"
class="card"/>

<text
x="420"
y="110"
fill="white"
font-size="20"
font-family="Arial">
Contest Rating History
</text>

<line
x1="{GRAPH_LEFT}"
y1="{GRAPH_TOP + GRAPH_HEIGHT}"
x2="{GRAPH_LEFT + GRAPH_WIDTH}"
y2="{GRAPH_TOP + GRAPH_HEIGHT}"
stroke="#30363d"/>

<line
x1="{GRAPH_LEFT}"
y1="{GRAPH_TOP}"
x2="{GRAPH_LEFT}"
y2="{GRAPH_TOP + GRAPH_HEIGHT}"
stroke="#30363d"/>

<g clip-path="url(#graphClip)">

<polygon
fill="url(#areaGradient)"
points="{area_points}"/>

<polyline
fill="none"
stroke="#a855f7"
stroke-width="4"
points="{polyline_points}"/>

{dots}

</g>

<!-- FOOTER -->

<text x="40"
      y="600"
      fill="white"
      font-size="15">
Active Days: {lc_active}
</text>

<text x="300"
      y="600"
      fill="#22c55e"
      font-size="15">
GFG Solved: {gfg_solved}
</text>

<text x="550"
      y="600"
      fill="#60a5fa"
      font-size="15">
Codeforces Solved: {cf_solved}
</text>

<text x="850"
      y="600"
      fill="#a855f7"
      font-size="15">
Contests: {len(ratings)}
</text>

</svg>
"""

with open(
    "assets/codolio-stats.svg",
    "w",
    encoding="utf-8"
) as f:
    f.write(svg)

print("SVG generated successfully.")
