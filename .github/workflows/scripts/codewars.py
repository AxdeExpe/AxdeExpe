import requests
from datetime import datetime

USERNAME = "AxdeExpe"  # <-- hier deinen Codewars Usernamen eintragen
OUTPUT_FILE = "codewars_stats.svg"

# 1️⃣ Codewars API abfragen
url = f"https://www.codewars.com/api/v1/users/{USERNAME}"
res = requests.get(url)
if res.status_code != 200:
    raise Exception(f"Fehler beim Abrufen der API: {res.status_code}")

data = res.json()
honor = data.get("honor", 0)
overall_rank = data.get("ranks", {}).get("overall", {}).get("name", "Unknown")
completed_katas = data.get("codeChallenges", {}).get("totalCompleted", 0)

# 2️⃣ SVG generieren
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120">
    <rect width="300" height="120" fill="#0e1116" rx="10" ry="10"/>
    <text x="20" y="35" font-family="Verdana" font-size="16" fill="#ff4500">Codewars Stats</text>
    <text x="20" y="60" font-family="Verdana" font-size="14" fill="#ffffff">Username: {USERNAME}</text>
    <text x="20" y="80" font-family="Verdana" font-size="14" fill="#ffffff">Honor: {honor}</text>
    <text x="20" y="100" font-family="Verdana" font-size="14" fill="#ffffff">Rank: {overall_rank}</text>
    <text x="150" y="100" font-family="Verdana" font-size="14" fill="#ffffff">Katas: {completed_katas}</text>
    <text x="20" y="115" font-family="Verdana" font-size="10" fill="#888888">Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</text>
</svg>'''

# 3️⃣ SVG speichern
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"SVG erfolgreich erstellt: {OUTPUT_FILE}")
