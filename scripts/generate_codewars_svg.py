import requests
from datetime import datetime

USERNAME = "AxdeExpe"
OUTPUT_FILE = "codewars_stats.svg"

# 1️⃣ Codewars API abfragen
url = f"https://www.codewars.com/api/v1/users/{USERNAME}"
res = requests.get(url)
if res.status_code != 200:
    raise Exception(f"Fehler beim Abrufen der API: {res.status_code}")

data = res.json()
honor = data.get("honor", 0)
leaderboard_position = data.get("leaderboardPosition", "N/A")
overall_rank = data.get("ranks", {}).get("overall", {}).get("name", "Unknown")
rank_score = data.get("ranks", {}).get("overall", {}).get("score", 0)
completed_katas = data.get("codeChallenges", {}).get("totalCompleted", 0)
authored_katas = data.get("codeChallenges", {}).get("totalAuthored", 0)

# Sprachendaten extrahieren und sortieren
languages = data.get("ranks", {}).get("languages", {})
sorted_languages = sorted(
    languages.items(), 
    key=lambda x: x[1].get("score", 0), 
    reverse=True
)

# 2️⃣ SVG generieren mit detaillierten Statistiken
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="280" viewBox="0 0 500 280">
    <defs>
        <linearGradient id="headerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#0d1117" />
            <stop offset="100%" stop-color="#161b22" />
        </linearGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge> 
                <feMergeNode in="coloredBlur"/> 
                <feMergeNode in="SourceGraphic"/> 
            </feMerge>
        </filter>
    </defs>
    
    <!-- Hintergrund -->
    <rect width="500" height="280" fill="#0d1117" rx="10" ry="10"/>
    
    <!-- Header-Bereich -->
    <rect width="500" height="50" fill="url(#headerGradient)" rx="10" ry="10"/>
    <text x="250" y="32" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#c4c4c4" filter="url(#glow)">Codewars Statistics</text>
    
    <!-- Trennlinien -->
    <line x1="20" y1="60" x2="480" y2="60" stroke="#c4c4c4" stroke-width="0.5" opacity="0.3"/>
    <line x1="250" y1="80" x2="250" y2="220" stroke="#c4c4c4" stroke-width="0.5" opacity="0.3"/>
    <line x1="20" y1="220" x2="480" y2="220" stroke="#c4c4c4" stroke-width="0.5" opacity="0.3"/>
    
    <!-- Linke Spalte - Hauptstatistiken -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#f0f6fc">
        <text x="30" y="85" font-size="16" font-weight="600" fill="#c4c4c4">Overview</text>
        
        <text x="30" y="115">Username:</text>
        <text x="180" y="115" font-weight="600" fill="#c4c4c4">{USERNAME}</text>
        
        <text x="30" y="140">Honor:</text>
        <text x="180" y="140" font-weight="600" fill="#c4c4c4">{honor}</text>
        
        <text x="30" y="165">Global Rank:</text>
        <text x="180" y="165" font-weight="600" fill="#c4c4c4">#{leaderboard_position}</text>
        
        <text x="30" y="190">Overall Rank:</text>
        <text x="180" y="190" font-weight="600" fill="#c4c4c4">{overall_rank} ({rank_score} pts)</text>
        
        <text x="30" y="215">Completed Katas:</text>
        <text x="180" y="215" font-weight="600" fill="#c4c4c4">{completed_katas}</text>
    </g>
    
    <!-- Rechte Spalte - Sprachenstatistiken -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#f0f6fc">
        <text x="270" y="85" font-size="16" font-weight="600" fill="#c4c4c4">Top Languages</text>
        
        <!-- Top 5 Sprachen anzeigen -->
        {''.join(f'''
        <text x="270" y="{115 + i*25}">{lang[0].title()}:</text>
        <text x="400" y="{115 + i*25}" font-weight="600" fill="#c4c4c4">{lang[1].get('name', 'N/A')} ({lang[1].get('score', 0)} pts)</text>
        ''' for i, lang in enumerate(sorted_languages[:5]))}
        
        <text x="270" y="215">Authored Katas:</text>
        <text x="400" y="215" font-weight="600" fill="#c4c4c4">{authored_katas}</text>
    </g>
    
    <!-- Dekorative Elemente -->
    <circle cx="480" cy="30" r="5" fill="#c4c4c4" opacity="0.7"/>
    <circle cx="465" cy="45" r="5" fill="#c4c4c4" opacity="0.5"/>
    <circle cx="450" cy="30" r="5" fill="#c4c4c4" opacity="0.3"/>
    
    <!-- Fortschrittsbalken für Gesamtrank -->
    <rect x="30" y="235" width="440" height="10" fill="#2d333b" rx="5" ry="5"/>
    <rect x="30" y="235" width="{min(440, max(10, rank_score/1000*440))}" height="10" fill="#c4c4c4" rx="5" ry="5"/>
    <text x="30" y="260" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#8b949e">Rank Progress</text>
    
    <!-- Update-Zeit -->
    <text x="250" y="275" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#8b949e" opacity="0.8">
        Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
    </text>
</svg>'''

# 3️⃣ SVG speichern
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"SVG erfolgreich erstellt: {OUTPUT_FILE}")
