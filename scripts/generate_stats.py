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

leetcode = next(
    p for p in data
    if p["platform"] == "leetcode"
)

gfg = next(
    p for p in data
    if p["platform"] == "geeksforgeeks"
)

cf = next(
    p for p in data
    if p["platform"] == "codeforces"
)

# Stats
lc_solved = leetcode["totalQuestionStats"]["totalQuestionCounts"]
lc_rating = leetcode["userStats"]["currentRating"]
lc_peak = leetcode["userStats"]["maxRating"]
lc_active = leetcode["dailyActivityStatsResponse"]["totalActiveDays"]
lc_streak = leetcode["dailyActivityStatsResponse"]["maxStreak"]

gfg_solved = gfg["totalQuestionStats"]["totalQuestionCounts"]
cf_solved = cf["totalQuestionStats"]["totalQuestionCounts"]

# Contest history (DYNAMIC)
contest_history = leetcode["contestActivityStats"]["contestActivityList"]

ratings = [
    contest["rating"]
    for contest in contest_history
]

# Graph dimensions
graph_x = 80
graph_y = 80
graph_width = 720
graph_height = 220

min_rating = min(ratings)
max_rating = max(ratings)

if min_rating == max_rating:
    max_rating += 1

points = []

for i, rating in enumerate(ratings):

    if len(ratings) == 1:
        x = graph_x + graph_width / 2
    else:
        x = graph_x + (
            i * graph_width / (len(ratings) - 1)
        )

    y = graph_y + graph_height - (
        (rating - min_rating)
        / (max_rating - min_rating)
        * graph_height
    )

    points.append((x, y, rating))

polyline_points = " ".join(
    f"{x},{y}"
    for x, y, _ in points
)

dots = ""

for x, y, rating in points:
    dots += f"""
    <circle cx="{x}" cy="{y}" r="5" fill="#FFA116"/>
    <text x="{x-12}" y="{y-12}"
          fill="white"
          font-size="11">
        {rating}
    </text>
    """

svg = f"""
<svg width="900"
     height="520"
     xmlns="http://www.w3.org/2000/svg">

<style>
.title {{
    fill:white;
    font-size:28px;
    font-family:Arial;
    font-weight:bold;
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
    font-size:24px;
    font-family:Arial;
    font-weight:bold;
}}
</style>

<rect width="100%"
      height="100%"
      fill="#0d1117"
      rx="20"/>

<text x="30"
      y="40"
      class="title">
LeetCode Rating Analytics
</text>

<!-- Rating Card -->
<rect x="30"
      y="60"
      width="180"
      height="90"
      rx="12"
      class="card"/>

<text x="50"
      y="90"
      class="label">
Current Rating
</text>

<text x="50"
      y="125"
      class="value">
{lc_rating}
</text>

<!-- Peak Card -->
<rect x="230"
      y="60"
      width="180"
      height="90"
      rx="12"
      class="card"/>

<text x="250"
      y="90"
      class="label">
Peak Rating
</text>

<text x="250"
      y="125"
      class="value">
{lc_peak}
</text>

<!-- Solved Card -->
<rect x="430"
      y="60"
      width="180"
      height="90"
      rx="12"
      class="card"/>

<text x="450"
      y="90"
      class="label">
Problems Solved
</text>

<text x="450"
      y="125"
      class="value">
{lc_solved}
</text>

<!-- Streak Card -->
<rect x="630"
      y="60"
      width="180"
      height="90"
      rx="12"
      class="card"/>

<text x="650"
      y="90"
      class="label">
Max Streak
</text>

<text x="650"
      y="125"
      class="value">
{lc_streak}
</text>

<!-- Graph Background -->
<rect x="40"
      y="180"
      width="820"
      height="280"
      rx="12"
      class="card"/>

<text x="60"
      y="210"
      fill="white"
      font-size="18">
Contest Rating History
</text>

<!-- Axes -->
<line x1="80"
      y1="410"
      x2="820"
      y2="410"
      stroke="#444"/>

<line x1="80"
      y1="230"
      x2="80"
      y2="410"
      stroke="#444"/>

<!-- Line Graph -->
<polyline
    fill="none"
    stroke="#FFA116"
    stroke-width="4"
    points="{polyline_points}"
/>

{dots}

<!-- Footer Stats -->

<text x="60"
      y="490"
      fill="white"
      font-size="15">
Active Days: {lc_active}
</text>

<text x="260"
      y="490"
      fill="white"
      font-size="15">
GFG Solved: {gfg_solved}
</text>

<text x="460"
      y="490"
      fill="white"
      font-size="15">
Codeforces Solved: {cf_solved}
</text>

<text x="670"
      y="490"
      fill="white"
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