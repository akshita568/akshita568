import os
import json
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
print(json.dumps(leetcode, indent=2))
gfg = next(p for p in data if p["platform"] == "geeksforgeeks")
cf = next(p for p in data if p["platform"] == "codeforces")

lc_solved = leetcode["totalQuestionStats"]["totalQuestionCounts"]
lc_rating = leetcode["userStats"]["currentRating"]
lc_peak = leetcode["userStats"]["maxRating"]
lc_active = leetcode["dailyActivityStatsResponse"]["totalActiveDays"]
lc_streak = leetcode["dailyActivityStatsResponse"]["maxStreak"]

gfg_solved = gfg["totalQuestionStats"]["totalQuestionCounts"]
cf_solved = cf["totalQuestionStats"]["totalQuestionCounts"]

print(f"LeetCode Solved: {lc_solved}")
print(f"Contest Rating: {lc_rating}")
print(f"Peak Rating: {lc_peak}")
print(f"Active Days: {lc_active}")
print(f"Max Streak: {lc_streak}")
print(f"GFG Solved: {gfg_solved}")
print(f"Codeforces Solved: {cf_solved}")

# Progress percentages
lc_solved_pct = min((lc_solved / 500) * 100, 100)
rating_pct = min((lc_rating / 2500) * 100, 100)
streak_pct = min((lc_streak / 100) * 100, 100)

svg = f"""
<svg width="900" height="450" xmlns="http://www.w3.org/2000/svg">

<style>
.title {{
    fill: white;
    font-size: 30px;
    font-family: Arial;
    font-weight: bold;
}}

.label {{
    fill: #c9d1d9;
    font-size: 16px;
    font-family: Arial;
}}

.value {{
    fill: white;
    font-size: 18px;
    font-family: Arial;
    font-weight: bold;
}}

.small {{
    fill: #8b949e;
    font-size: 14px;
    font-family: Arial;
}}
</style>

<rect width="100%" height="100%" rx="20" fill="#0d1117"/>

<text x="30" y="45" class="title">
📊 Coding Profile Analytics
</text>

<!-- LeetCode Solved -->
<text x="30" y="90" class="label">
LeetCode Solved ({lc_solved})
</text>

<rect x="30" y="100" width="320" height="18" rx="9" fill="#30363d"/>
<rect x="30" y="100" width="{3.2 * lc_solved_pct}" height="18" rx="9" fill="#FFA116"/>

<!-- Contest Rating -->
<text x="30" y="150" class="label">
Contest Rating ({lc_rating})
</text>

<rect x="30" y="160" width="320" height="18" rx="9" fill="#30363d"/>
<rect x="30" y="160" width="{3.2 * rating_pct}" height="18" rx="9" fill="#58A6FF"/>

<!-- Streak -->
<text x="30" y="210" class="label">
Max Streak ({lc_streak} days)
</text>

<rect x="30" y="220" width="320" height="18" rx="9" fill="#30363d"/>
<rect x="30" y="220" width="{3.2 * streak_pct}" height="18" rx="9" fill="#F85149"/>

<!-- Extra Stats -->
<text x="30" y="290" class="label">
Peak Rating
</text>

<text x="250" y="290" class="value">
{lc_peak}
</text>

<text x="30" y="330" class="label">
Active Days
</text>

<text x="250" y="330" class="value">
{lc_active}
</text>

<!-- Right Side -->
<text x="500" y="90" class="label">
Problems Solved Comparison
</text>

<!-- LC -->
<rect x="520" y="{350 - lc_solved}" width="60" height="{lc_solved}" fill="#FFA116"/>
<text x="530" y="380" class="small">LC</text>
<text x="520" y="{340 - lc_solved}" class="small">{lc_solved}</text>

<!-- GFG -->
<rect x="620" y="{350 - gfg_solved * 3}" width="60" height="{gfg_solved * 3}" fill="#2F8D46"/>
<text x="630" y="380" class="small">GFG</text>
<text x="620" y="{340 - gfg_solved * 3}" class="small">{gfg_solved}</text>

<!-- CF -->
<rect x="720" y="{350 - cf_solved * 20}" width="60" height="{cf_solved * 20}" fill="#58A6FF"/>
<text x="735" y="380" class="small">CF</text>
<text x="720" y="{340 - cf_solved * 20}" class="small">{cf_solved}</text>

</svg>
"""

with open("assets/codolio-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("SVG generated successfully.")