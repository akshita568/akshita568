import os
import requests
from datetime import datetime

token = os.environ["CODOLIO_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

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

# -------------------------
# BASIC STATS
# -------------------------

lc_solved = leetcode["totalQuestionStats"]["totalQuestionCounts"]
lc_rating = leetcode["userStats"]["currentRating"]
lc_peak = leetcode["userStats"]["maxRating"]

gfg_solved = gfg["totalQuestionStats"]["totalQuestionCounts"]
cf_solved = cf["totalQuestionStats"]["totalQuestionCounts"]

total_solved = lc_solved + gfg_solved + cf_solved

ratings = leetcode["contestActivityStats"]["contestActivityList"]
ratings = [c["rating"] for c in ratings] if ratings else [0]

# -------------------------
# ACTIVE DAYS (UNION LOGIC)
# -------------------------

def extract_days(calendar):
    if not calendar:
        return set()
    return {
        datetime.utcfromtimestamp(int(ts)).date()
        for ts in calendar.keys()
    }

lc_days = extract_days(leetcode["dailyActivityStatsResponse"]["submissionCalendar"])
gfg_days = extract_days(gfg["dailyActivityStatsResponse"]["submissionCalendar"])
cf_days = extract_days(cf["dailyActivityStatsResponse"]["submissionCalendar"])

total_active_days = len(lc_days | gfg_days | cf_days)

# -------------------------
# GRAPH CONFIG (FIXED LAYOUT SYSTEM)
# -------------------------

WIDTH = 1000
HEIGHT = 520

HEADER_H = 120
GRAPH_TOP = HEADER_H
GRAPH_HEIGHT = 240
GRAPH_LEFT = 60
GRAPH_WIDTH = 880

PADDING = 20

min_rating = min(ratings)
max_rating = max(ratings)

if min_rating == max_rating:
    max_rating += 1

points = []

for i, rating in enumerate(ratings):

    x = GRAPH_LEFT + (i * GRAPH_WIDTH / max(1, len(ratings) - 1))

    usable_height = GRAPH_HEIGHT - 30

    y = (
        GRAPH_TOP
        + GRAPH_HEIGHT
        - 20
        - ((rating - min_rating) / (max_rating - min_rating)) * usable_height
    )

    points.append((x, y))

polyline_points = " ".join(f"{x},{y}" for x, y in points)

area_points = (
    f"{points[0][0]},{GRAPH_TOP + GRAPH_HEIGHT} "
    + polyline_points +
    f" {points[-1][0]},{GRAPH_TOP + GRAPH_HEIGHT}"
)

# -------------------------
# SVG
# -------------------------

svg = f"""
<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">

<!-- BACKGROUND -->
<rect width="100%" height="100%" rx="18" fill="#0d1117"/>

<!-- TITLE -->
<text x="25" y="40" fill="white" font-size="24" font-weight="bold">
Contest Analytics Dashboard
</text>

<!-- TOP STATS -->
<rect x="20" y="60" width="220" height="60" rx="10" fill="#161b22"/>
<text x="35" y="85" fill="#8b949e">Current Rating</text>
<text x="35" y="108" fill="white" font-size="18">{lc_rating}</text>

<rect x="260" y="60" width="220" height="60" rx="10" fill="#161b22"/>
<text x="275" y="85" fill="#8b949e">Peak Rating</text>
<text x="275" y="108" fill="white" font-size="18">{lc_peak}</text>

<rect x="500" y="60" width="220" height="60" rx="10" fill="#161b22"/>
<text x="515" y="85" fill="#8b949e">Total Solved</text>
<text x="515" y="108" fill="white" font-size="18">{total_solved}</text>

<rect x="740" y="60" width="220" height="60" rx="10" fill="#161b22"/>
<text x="755" y="85" fill="#8b949e">Max Streak</text>
<text x="755" y="108" fill="white" font-size="18">{leetcode["dailyActivityStatsResponse"]["maxStreak"]}</text>

<!-- GRAPH PANEL -->
<rect x="20" y="{GRAPH_TOP}" width="960" height="{GRAPH_HEIGHT}" rx="12" fill="#161b22"/>

<!-- GRAPH AREA -->
<polygon fill="rgba(168,85,247,0.2)" points="{area_points}"/>

<!-- LINE -->
<polyline fill="none" stroke="#a855f7" stroke-width="3" points="{polyline_points}"/>

<!-- POINTS -->
{"".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#a855f7"/>' for x, y in points)}

<!-- FOOTER -->
<rect x="20" y="450" width="960" height="60" rx="10" fill="#161b22"/>

<text x="40" y="485" fill="white" font-size="13">
🔥 Active Days: {total_active_days}
</text>

<text x="220" y="485" fill="#ffa116" font-size="13">
🟠 LC: {lc_solved}
</text>

<text x="360" y="485" fill="#22c55e" font-size="13">
🟢 GFG: {gfg_solved}
</text>

<text x="520" y="485" fill="#60a5fa" font-size="13">
🔵 CF: {cf_solved}
</text>

<text x="700" y="485" fill="#a855f7" font-size="13">
🏆 Contests: {len(ratings)}
</text>

</svg>
"""

# -------------------------
# SAVE FILE
# -------------------------

os.makedirs("assets", exist_ok=True)

with open("assets/codolio-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("SVG generated successfully.")