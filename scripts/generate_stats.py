
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
        LEFT_MARGIN = 30
        RIGHT_MARGIN = 30
        
        x = (
            GRAPH_LEFT
            + LEFT_MARGIN
            + i * (GRAPH_WIDTH - LEFT_MARGIN - RIGHT_MARGIN)
              / (len(ratings) - 1)
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
<svg width="1000"
     height="420"
     xmlns="http://www.w3.org/2000/svg">

<defs>

<linearGradient id="areaGradient"
                x1="0"
                y1="0"
                x2="0"
                y2="1">
    <stop offset="0%" stop-color="#a855f7" stop-opacity="0.4"/>
    <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
</linearGradient>

</defs>

<style>

.title {{
    fill:white;
    font-size:24px;
    font-weight:bold;
    font-family:Arial;
}}

.label {{
    fill:#8b949e;
    font-size:14px;
    font-family:Arial;
}}

.value {{
    fill:white;
    font-size:18px;
    font-weight:bold;
    font-family:Arial;
}}

</style>

<rect width="100%"
      height="100%"
      rx="18"
      fill="#0d1117"/>

<!-- TITLE -->

<text x="25"
      y="35"
      class="title">
🚀 Coding Analytics Dashboard
</text>

<!-- TOP STATS -->

<rect x="20" y="55" width="220" height="60" rx="10" fill="#161b22"/>

<text x="35" y="80" class="label">
Current Rating
</text>

<text x="35" y="103" class="value">
{lc_rating}
</text>

<rect x="260" y="55" width="220" height="60" rx="10" fill="#161b22"/>

<text x="275" y="80" class="label">
Peak Rating
</text>

<text x="275" y="103" class="value">
{lc_peak}
</text>

<rect x="500" y="55" width="220" height="60" rx="10" fill="#161b22"/>

<text x="515" y="80" class="label">
Problems Solved
</text>

<text x="515" y="103" class="value">
{lc_solved}
</text>

<rect x="740" y="55" width="220" height="60" rx="10" fill="#161b22"/>

<text x="755" y="80" class="label">
Max Streak
</text>

<text x="755" y="103" class="value">
{lc_streak} days
</text>

<!-- GRAPH PANEL -->

<rect x="20"
      y="140"
      width="940"
      height="220"
      rx="12"
      fill="#161b22"/>

<text x="35"
      y="170"
      fill="white"
      font-size="18"
      font-family="Arial">
Contest Rating Trend
</text>

<!-- GRID -->

<line x1="50" y1="210" x2="930" y2="210" stroke="#21262d"/>
<line x1="50" y1="260" x2="930" y2="260" stroke="#21262d"/>
<line x1="50" y1="310" x2="930" y2="310" stroke="#21262d"/>

<line x1="50" y1="190" x2="50" y2="340" stroke="#30363d"/>
<line x1="50" y1="340" x2="930" y2="340" stroke="#30363d"/>

<polygon
fill="url(#areaGradient)"
points="{area_points}"/>

<polyline
fill="none"
stroke="#a855f7"
stroke-width="4"
points="{polyline_points}"/>

{"".join(
    f'<circle cx="{x}" cy="{y}" r="4" fill="#a855f7"/>'
    for x, y, _ in points
)}

<!-- FOOTER -->

<rect x="20"
      y="375"
      width="940"
      height="30"
      rx="8"
      fill="#161b22"/>

<text x="40"
      y="395"
      fill="white"
      font-size="13">
🔥 Active Days: {lc_active}
</text>

<text x="260"
      y="395"
      fill="#22c55e"
      font-size="13">
🟢 GFG Solved: {gfg_solved}
</text>

<text x="500"
      y="395"
      fill="#60a5fa"
      font-size="13">
🔵 Codeforces Solved: {cf_solved}
</text>

<text x="760"
      y="395"
      fill="#a855f7"
      font-size="13">
🏆 Contests: {len(ratings)}
</text>

</svg>
"""

print("SVG generated successfully.")
