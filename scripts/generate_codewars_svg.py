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
        
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&display=swap');
        </style>
    </defs>
    
    <!-- Hintergrund -->
    <rect width="540" height="360" fill="url(#bgGradient)" rx="8" ry="8"/>
    
    <!-- Header Box -->
    <rect x="20" y="20" width="500" height="60" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="20" width="500" height="2" fill="url(#accentGradient)"/>
    <text x="270" y="45" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="18" font-weight="600" fill="#e6edf3">
        CODEWARS STATISTICS
    </text>
    <text x="270" y="62" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="11" fill="#7d8590">
        @{USERNAME}
    </text>
    
    <!-- Hauptdaten Boxen -->
    <g font-family="JetBrains Mono, monospace">
        <!-- Honor Box -->
        <rect x="20" y="100" width="150" height="80" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <rect x="20" y="100" width="150" height="2" fill="url(#accentGradient)"/>
        <text x="95" y="125" text-anchor="middle" font-size="12" fill="#7d8590">HONOR</text>
        <text x="95" y="150" text-anchor="middle" font-size="24" font-weight="600" fill="#e6edf3">{honor}</text>
        
        <!-- Rank Box -->
        <rect x="185" y="100" width="150" height="80" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <rect x="185" y="100" width="150" height="2" fill="url(#accentGradient)"/>
        <text x="260" y="125" text-anchor="middle" font-size="12" fill="#7d8590">GLOBAL RANK</text>
        <text x="260" y="150" text-anchor="middle" font-size="24" font-weight="600" fill="#e6edf3">
            #{leaderboard_position if leaderboard_position != "N/A" else "N/A"}
        </text>
        
        <!-- Katas Box -->
        <rect x="350" y="100" width="150" height="80" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <rect x="350" y="100" width="150" height="2" fill="url(#accentGradient)"/>
        <text x="425" y="125" text-anchor="middle" font-size="12" fill="#7d8590">KATAS SOLVED</text>
        <text x="425" y="150" text-anchor="middle" font-size="24" font-weight="600" fill="#e6edf3">{completed_katas}</text>
    </g>
    
    <!-- Rank Info Box -->
    <rect x="20" y="200" width="500" height="50" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="200" width="500" height="2" fill="url(#accentGradient)"/>
    <text x="270" y="220" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" fill="#7d8590">OVERALL RANK</text>
    <text x="270" y="240" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="14" font-weight="600" fill="#e6edf3">
        {overall_rank} • {rank_score} POINTS
    </text>
    
    <!-- Sprachen Box -->
    <rect x="20" y="270" width="500" height="60" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="270" width="500" height="2" fill="url(#accentGradient)"/>
    <text x="270" y="290" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" font-weight="600" fill="#e6edf3">TOP LANGUAGES</text>
    
    <!-- Sprach-Balken -->
    <g transform="translate(40 305)">
        <g font-family="JetBrains Mono, monospace" font-size="11">'''

# Sprach-Balken mit korrekter Einrückung
bar_width = 420
bar_height = 6
bar_spacing = 12

for i, (lang_name, lang_rank, lang_score) in enumerate(top_languages):
    fill_width = (lang_score / max_score) * bar_width if max_score > 0 else 0
    y_pos = i * (bar_height + bar_spacing)
    
    svg_content += f'''
            <!-- {lang_name} -->
            <text x="0" y="{y_pos + 5}" fill="#7d8590">{lang_name.upper()}</text>
            <rect x="80" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="rgba(125, 133, 144, 0.2)" rx="3" ry="3"/>
            <rect x="80" y="{y_pos}" width="{fill_width}" height="{bar_height}" fill="#e6edf3" rx="3" ry="3"/>
            <text x="{bar_width + 85}" y="{y_pos + 5}" fill="#7d8590" text-anchor="end">{lang_score}</text>'''

svg_content += f'''
        </g>
    </g>
    
    <!-- Footer Box -->
    <rect x="20" y="345" width="500" height="30" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <rect x="20" y="345" width="500" height="2" fill="url(#accentGradient)"/>
    <g font-family="JetBrains Mono, monospace" font-size="10" fill="#7d8590">
        <text x="40" y="362">AUTHORED: <tspan fill="#e6edf3" font-weight="600">{authored_katas}</tspan></text>
        <text x="270" y="362" text-anchor="middle">UPDATED: {current_time}</text>
        <text x="480" y="362" text-anchor="end">RANK: <tspan fill="#e6edf3" font-weight="600">{overall_rank}</tspan></text>
    </g>
</svg>'''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Technisches SVG erfolgreich erstellt: {OUTPUT_FILE}")
