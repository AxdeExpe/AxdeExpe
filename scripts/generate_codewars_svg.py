import requests
from datetime import datetime

USERNAME = "AxdeExpe"
OUTPUT_FILE = "codewars_stats.svg"

# API-Abfrage
url = f"https://www.codewars.com/api/v1/users/{USERNAME}"
res = requests.get(url)
if res.status_code != 200:
    raise Exception(f"Fehler beim Abrufen der API: {res.status_code}")

data = res.json()

# Daten-Extraktion
honor = data.get("honor", 0)
leaderboard_position = data.get("leaderboardPosition", "N/A")
overall_rank = data.get("ranks", {}).get("overall", {}).get("name", "Unknown")
rank_score = data.get("ranks", {}).get("overall", {}).get("score", 0)
completed_katas = data.get("codeChallenges", {}).get("totalCompleted", 0)
authored_katas = data.get("codeChallenges", {}).get("totalAuthored", 0)

# Sprachendaten
languages = data.get("ranks", {}).get("languages", {})
sorted_languages = sorted(
    languages.items(), 
    key=lambda x: x[1].get("score", 0), 
    reverse=True
)

top_languages = []
for lang, data in sorted_languages[:5]:
    lang_name = lang.capitalize()
    lang_rank = data.get("name", "Unknown")
    lang_score = data.get("score", 0)
    top_languages.append((lang_name, lang_rank, lang_score))

# Chart-Daten
max_score = max([lang[2] for lang in top_languages]) if top_languages else 1
current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="360" viewBox="0 0 540 360">
    <defs>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0d1117"/>
            <stop offset="100%" stop-color="#161b22"/>
        </linearGradient>
        
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#c4c4c4"/>
            <stop offset="100%" stop-color="#0059ff"/>
        </linearGradient>
    </defs>
    
    <!-- Hintergrund -->
    <rect width="540" height="360" fill="url(#bgGradient)" rx="8" ry="8"/>
    
    <!-- Header Box -->
    <rect x="20" y="15" width="500" height="50" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="15" width="500" height="2" fill="url(#accentGradient)"/>
    <text x="270" y="35" text-anchor="middle" font-family="Consolas, Monaco, 'Courier New', monospace" font-size="16" font-weight="600" fill="#e6edf3">
        CODEWARS STATISTICS
    </text>
    <text x="270" y="50" text-anchor="middle" font-family="Consolas, Monaco, 'Courier New', monospace" font-size="10" fill="#7d8590">
        @{USERNAME}
    </text>
    
    <!-- Hauptdaten Boxen - Volle Breite nutzend -->
    <g font-family="Consolas, Monaco, 'Courier New', monospace">
        <!-- Honor Box -->
        <rect x="20" y="80" width="160" height="70" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <rect x="20" y="80" width="160" height="2" fill="url(#accentGradient)"/>
        <text x="100" y="100" text-anchor="middle" font-size="11" fill="#7d8590">HONOR</text>
        <text x="100" y="120" text-anchor="middle" font-size="20" font-weight="600" fill="#e6edf3">{honor}</text>
        
        <!-- Rank Box -->
        <rect x="190" y="80" width="160" height="70" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <rect x="190" y="80" width="160" height="2" fill="url(#accentGradient)"/>
        <text x="270" y="100" text-anchor="middle" font-size="11" fill="#7d8590">GLOBAL RANK</text>
        <text x="270" y="120" text-anchor="middle" font-size="20" font-weight="600" fill="#e6edf3">
            #{leaderboard_position if leaderboard_position != "N/A" else "N/A"}
        </text>
        
        <!-- Katas Box -->
        <rect x="360" y="80" width="160" height="70" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <rect x="360" y="80" width="160" height="2" fill="url(#accentGradient)"/>
        <text x="440" y="100" text-anchor="middle" font-size="11" fill="#7d8590">KATAS SOLVED</text>
        <text x="440" y="120" text-anchor="middle" font-size="20" font-weight="600" fill="#e6edf3">{completed_katas}</text>
    </g>
    
    <!-- Rank Info Box -->
    <rect x="20" y="165" width="500" height="40" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="165" width="500" height="2" fill="url(#accentGradient)"/>
    <text x="270" y="182" text-anchor="middle" font-family="Consolas, Monaco, 'Courier New', monospace" font-size="11" fill="#7d8590">OVERALL RANK</text>
    <text x="270" y="197" text-anchor="middle" font-family="Consolas, Monaco, 'Courier New', monospace" font-size="12" font-weight="600" fill="#e6edf3">
        {overall_rank} • {rank_score} POINTS
    </text>
    
    <!-- Sprachen Box -->
    <rect x="20" y="220" width="500" height="90" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="220" width="500" height="2" fill="url(#accentGradient)"/>
    <text x="270" y="238" text-anchor="middle" font-family="Consolas, Monaco, 'Courier New', monospace" font-size="11" font-weight="600" fill="#e6edf3">TOP LANGUAGES</text>
    
    <!-- Sprach-Balken - Innerhalb der Box -->
    <g transform="translate(40 250)">
        <g font-family="Consolas, Monaco, 'Courier New', monospace" font-size="10">'''

# Sprach-Balken mit korrekter Einrückung innerhalb der Box
bar_width = 420
bar_height = 5
bar_spacing = 8

for i, (lang_name, lang_rank, lang_score) in enumerate(top_languages):
    fill_width = (lang_score / max_score) * bar_width if max_score > 0 else 0
    y_pos = i * (bar_height + bar_spacing)
    
    svg_content += f'''
            <!-- {lang_name} -->
            <text x="0" y="{y_pos + 4}" fill="#7d8590">{lang_name.upper()}</text>
            <rect x="70" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="rgba(125, 133, 144, 0.2)" rx="2" ry="2"/>
            <rect x="70" y="{y_pos}" width="{fill_width}" height="{bar_height}" fill="#e6edf3" rx="2" ry="2"/>
            <text x="{bar_width + 75}" y="{y_pos + 4}" fill="#7d8590" text-anchor="end">{lang_score}</text>'''

svg_content += f'''
        </g>
    </g>
    
    <!-- Footer Box - Innerhalb des Bildes -->
    <rect x="20" y="325" width="500" height="25" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="325" width="500" height="2" fill="url(#accentGradient)"/>
    <g font-family="Consolas, Monaco, 'Courier New', monospace" font-size="9" fill="#7d8590">
        <text x="40" y="340">AUTHORED: <tspan fill="#e6edf3" font-weight="600">{authored_katas}</tspan></text>
        <text x="270" y="340" text-anchor="middle">UPDATED: {current_time}</text>
        <text x="480" y="340" text-anchor="end">RANK: <tspan fill="#e6edf3" font-weight="600">{overall_rank}</tspan></text>
    </g>
</svg>'''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Korrigiertes SVG erfolgreich erstellt: {OUTPUT_FILE}")
