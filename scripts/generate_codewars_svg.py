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

# Top 5 Sprachen vorbereiten
top_languages = []
for lang, data in sorted_languages[:5]:
    lang_name = lang.capitalize()
    lang_rank = data.get("name", "Unknown")
    lang_score = data.get("score", 0)
    top_languages.append((lang_name, lang_rank, lang_score))

# Aktuelles Datum und Uhrzeit
current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Fortschrittsbalken berechnen (vereinfachte Darstellung)
progress_width = min(440, max(0, (rank_score / 1000) * 440)) if rank_score > 0 else 0

# 2️⃣ SVG generieren mit dynamischen Daten
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="300" viewBox="0 0 500 300">
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
    <rect width="500" height="300" fill="#0d1117" rx="10" ry="10"/>
    
    <!-- Header-Bereich -->
    <rect width="500" height="50" fill="url(#headerGradient)" rx="10" ry="10"/>
    <text x="250" y="32" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#c4c4c4" filter="url(#glow)">Codewars Statistics</text>
    
    <!-- Trennlinien -->
    <line x1="20" y1="60" x2="480" y2="60" stroke="#c4c4c4" stroke-width="0.5" opacity="0.3"/>
    <line x1="250" y1="80" x2="250" y2="240" stroke="#c4c4c4" stroke-width="0.5" opacity="0.3"/>
    <line x1="20" y1="240" x2="480" y2="240" stroke="#c4c4c4" stroke-width="0.5" opacity="0.3"/>
    
    <!-- Linke Spalte - Hauptstatistiken -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#f0f6fc">
        <text x="30" y="85" font-size="16" font-weight="600" fill="#c4c4c4">Overview</text>
        
        <text x="30" y="115">Username:</text>
        <text x="180" y="115" font-weight="600" fill="#c4c4c4">{USERNAME}</text>
        
        <text x="30" y="140">Honor:</text>
        <text x="180" y="140" font-weight="600" fill="#c4c4c4">{honor}</text>
        
        <text x="30" y="165">Global Rank:</text>
        <text x="180" y="165" font-weight="600" fill="#c4c4c4">#{leaderboard_position if leaderboard_position != "N/A" else "N/A"}</text>
        
        <text x="30" y="190">Overall Rank:</text>
        <text x="180" y="190" font-weight="600" fill="#c4c4c4" font-size="13">{overall_rank}</text>
        <text x="180" y="205" font-weight="600" fill="#c4c4c4" font-size="12">({rank_score} pts)</text>
        
        <text x="30" y="230">Completed Katas:</text>
        <text x="180" y="230" font-weight="600" fill="#c4c4c4">{completed_katas}</text>
    </g>
    
    <!-- Rechte Spalte - Sprachenstatistiken -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#f0f6fc">
        <text x="270" y="85" font-size="16" font-weight="600" fill="#c4c4c4">Top Languages</text>
        
        <!-- Dynamische Sprachenanzeige -->'''

# Top-Sprachen dynamisch einfügen
y_pos = 115
for i, (lang_name, lang_rank, lang_score) in enumerate(top_languages):
    svg_content += f'''
        <text x="270" y="{y_pos + i * 25}">{lang_name}:</text>
        <text x="400" y="{y_pos + i * 25}" font-weight="600" fill="#c4c4c4">{lang_rank} ({lang_score} pts)</text>'''

# Rest des SVG-Codes
svg_content += f'''
        
        <text x="270" y="240">Authored Katas:</text>
        <text x="400" y="240" font-weight="600" fill="#c4c4c4">{authored_katas}</text>
    </g>
    
    <!-- Dekorative Elemente -->
    <circle cx="480" cy="30" r="5" fill="#c4c4c4" opacity="0.7"/>
    <circle cx="465" cy="45" r="5" fill="#c4c4c4" opacity="0.5"/>
    <circle cx="450" cy="30" r="5" fill="#c4c4c4" opacity="0.3"/>
    
    <!-- Fortschrittsbalken für Gesamtrank -->
    <rect x="30" y="255" width="440" height="10" fill="#2d333b" rx="5" ry="5"/>
    <rect x="30" y="255" width="{progress_width}" height="10" fill="#c4c4c4" rx="5" ry="5"/>
    <text x="30" y="280" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#8b949e">Rank Progress</text>
    
    <!-- Dynamische Update-Zeit -->
    <text x="250" y="295" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="#8b949e" opacity="0.8">
        Updated: {current_time}
    </text>
</svg>'''

# 3️⃣ SVG speichern
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"SVG erfolgreich erstellt: {OUTPUT_FILE}")
