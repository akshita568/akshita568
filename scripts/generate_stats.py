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

data = response.json()["data"]["platformProfiles"]["platformProfiles"]

leetcode = next(p for p in data if p["platform"] == "leetcode")
gfg = next(p for p in data if p["platform"] == "geeksforgeeks")
cf = next(p for p in data if p["platform"] == "codeforces")

lc_solved = leetcode["totalQuestionStats"]["totalQuestionCounts"]
lc_rating = leetcode["userStats"]["currentRating"]
lc_peak = leetcode["userStats"]["maxRating"]
lc_active = leetcode["dailyActivityStatsResponse"]["totalActiveDays"]
lc_streak = leetcode["dailyActivityStatsResponse"]["maxStreak"]

gfg_solved = gfg["totalQuestionStats"]["totalQuestionCounts"]
cf_solved = cf["totalQuestionStats"]["totalQuestionCounts"]

svg = f"""
<svg width="850" height="320" xmlns="http://www.w3.org/2000/svg">

<rect width="100%" height="100%" rx="20" fill="#0d1117"/>

<text x="30" y="45"
fill="#a371f7"
font-size="28"
font-family="Arial">
📊 Codolio Analytics
</text>

<text x="30" y="95" fill="white" font-size="20">
🟠 LeetCode Solved: {lc_solved}
</text>

<text x="30" y="135" fill="white" font-size="20">
📈 Contest Rating: {lc_rating}
</text>

<text x="30" y="175" fill="white" font-size="20">
🏆 Peak Rating: {lc_peak}
</text>

<text x="30" y="215" fill="white" font-size="20">
🔥 Max Streak: {lc_streak} days
</text>

<text x="30" y="255" fill="white" font-size="20">
📅 Active Days: {lc_active}
</text>

<text x="450" y="135" fill="white" font-size="20">
🟢 GFG Solved: {gfg_solved}
</text>

<text x="450" y="175" fill="white" font-size="20">
🔵 Codeforces Solved: {cf_solved}
</text>

</svg>
"""

with open("assets/codolio-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)