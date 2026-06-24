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

ratings = [
    c["rating"]
    for c in leetcode["contestActivityStats"]["contestActivityList"]
]

# -------------------------
# ACTIVE DAYS (FIXED LOGIC)
# -------------------------

def extract_days(submission_calendar):
    """Convert timestamps -> day buckets"""
    days = set()
    if not submission_calendar:
        return days

    for ts in submission_calendar.keys():
        day = datetime.utcfromtimestamp(int(ts)).date()
        days.add(day)

    return days


lc_days = extract_days(
    leetcode["dailyActivityStatsResponse"]["submissionCalendar"]
)

gfg_days = extract_days(
    gfg["dailyActivityStatsResponse"]["submissionCalendar"]
)

cf_days = extract_days(
    cf["dailyActivityStatsResponse"]["submissionCalendar"]
)

total_active_days = len(lc_days | gfg_days | cf_days)

# -------------------------
# GRAPH CONFIG
# -------------------------

GRAPH_LEFT = 60
GRAPH_TOP = 160
GRAPH_WIDTH = 860
GRAPH_HEIGHT = 200
PADDING = 20

if not ratings:
    ratings = [0]

min_rating = min(ratings)
max_rating = max(ratings)

if min_rating == max_rating:
    max_rating += 1

points = []

for i, rating in enumerate(ratings):

    if len(ratings) == 1:
        x = GRAPH_LEFT + GRAPH_WIDTH / 2
    else:
        x = GRAPH_LEFT + i * (GRAPH_WIDTH / (len(ratings) - 1))

    usable_height = GRAPH_HEIGHT - PADDING * 2

    y = (
        GRAPH_TOP
        + GRAPH_HEIGHT
        - PADDING
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
<svg width="1000" height="460"
     xmlns="http://www.w3.org/2000/svg">

<rect width="100%" height="100%" rx="18" fill="#0d1117"/>

<!-- TITLE -->
<text x="25" y="35" fill="white" font-size="24" font-weight="bold">
Contest Analytics
</text>

<!-- TOP STATS -->
<rect x="20" y="55" width="220" height="60" rx="10" fill="#161b22"/>
<text x="35" y="80" fill="#8b949e">Current Rating</text>
<text x="35" y="103" fill="white" font-size="18">{lc_rating}</text>

<rect x="260" y="55" width="220" height="60" rx="10" fill="#161b22"/>
<text x="275" y="80" fill="#8b949e">Peak Rating</text>
<text x="275" y="103" fill="white" font-size="18">{lc_peak}</text>

<rect x="500" y="55" width="220" height="60" rx="10" fill="#161b22"/>
<text x="515" y="80" fill="#8b949e">Problems Solved</text>
<text x="515" y="103" fill="white" font-size="18">{total_solved}</text>

<rect x="740" y="55" width="220" height="60" rx="10" fill="#161b22"/>
<text x="755" y="80" fill="#8b949e">Max Streak</text>
<text x="755" y="103" fill="white" font-size="18">{leetcode["dailyActivityStatsResponse"]["maxStreak"]}</text>

<!-- GRAPH -->
<rect x="20" y="140" width="940" height="220" rx="12" fill="#161b22"/>

<polygon fill="rgba(168,85,247,0.2)" points="{area_points}"/>

<polyline fill="none" stroke="#a855f7" stroke-width="3"
points="{polyline_points}"/>

{"".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#a855f7"/>' for x, y in points)}

<!-- FOOTER -->
<text x="40" y="405" fill="white" font-size="13">
🔥 Active Days (Total): {total_active_days}
</text>

<text x="260" y="405" fill="#ffa116" font-size="13">
🟠 LeetCode: {lc_solved}
</text>

<text x="460" y="405" fill="#22c55e" font-size="13">
🟢 GFG: {gfg_solved}
</text>

<text x="620" y="405" fill="#60a5fa" font-size="13">
🔵 CF: {cf_solved}
</text>

<text x="780" y="405" fill="#a855f7" font-size="13">
🏆 Contests: {len(ratings)}
</text>

</svg>
"""

with open("assets/codolio-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("SVG generated successfully.")