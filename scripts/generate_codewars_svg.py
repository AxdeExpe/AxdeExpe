import requests
from datetime import datetime

USERNAME = "AxdeExpe"
OUTPUT_FILE = "codewars_stats.svg"

url = f"https://www.codewars.com/api/v1/users/{USERNAME}"
res = requests.get(url)
if res.status_code != 200:
    raise Exception(f"Fehler beim Abrufen der API: {res.status_code}")

data = res.json()
honor = data.get("honor", 0)
overall_rank = data.get("ranks", {}).get("overall", {}).get("name", "Unknown")
completed_katas = data.get("codeChallenges", {}).get("totalCompleted", 0)

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="350" height="170" viewBox="0 0 350 170">
    <defs>
        <linearGradient id="headerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#0d1117" />
            <stop offset="100%" stop-color="#161b22" />
        </linearGradient>
    </defs>
    
    <!-- Hintergrund -->
    <rect width="350" height="170" fill="#0d1117" rx="8" ry="8"/>
    
    <!-- Header-Bereich -->
    <rect width="350" height="40" fill="url(#headerGradient)" rx="8" ry="8"/>
    <text x="175" y="25" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600" fill="#c4c4c4">Codewars Statistics</text>
    
    <!-- Trennlinie -->
    <line x1="20" y1="50" x2="330" y2="50" stroke="#c4c4c4" stroke-width="0.5" opacity="0.5"/>
    
    <!-- Statistik-Werte -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#f0f6fc">
        <text x="20" y="75">Username:</text>
        <text x="120" y="75" font-weight="600" fill="#c4c4c4">{USERNAME}</text>
        
        <text x="20" y="100">Honor:</text>
        <text x="120" y="100" font-weight="600" fill="#c4c4c4">{honor}</text>
        
        <text x="20" y="125">Rank:</text>
        <text x="120" y="125" font-weight="600" fill="#c4c4c4">{overall_rank}</text>
        
        <text x="20" y="150">Katas:</text>
        <text x="120" y="150" font-weight="600" fill="#c4c4c4">{completed_katas}</text>
    </g>
    
    <!-- Akzent-Element -->
    <rect x="330" y="60" width="8" height="8" fill="#c4c4c4" opacity="0.7" rx="1"/>
    <rect x="315" y="75" width="8" height="8" fill="#c4c4c4" opacity="0.5" rx="1"/>
    <rect x="330" y="90" width="8" height="8" fill="#c4c4c4" opacity="0.3" rx="1"/>
    
    <!-- Update-Zeit -->
    <text x="175" y="165" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#8b949e" opacity="0.8">
        Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
    </text>
</svg>'''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"SVG erfolgreich erstellt: {OUTPUT_FILE}")
