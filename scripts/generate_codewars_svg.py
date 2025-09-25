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
for lang, data in sorted_languages[:4]:
    lang_name = lang.capitalize()
    lang_rank = data.get("name", "Unknown")
    lang_score = data.get("score", 0)
    top_languages.append((lang_name, lang_rank, lang_score))

# Chart-Daten
max_score = max([lang[2] for lang in top_languages]) if top_languages else 1
current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="320" viewBox="0 0 500 320">
    <defs>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0f1525"/>
            <stop offset="100%" stop-color="#1a1f30"/>
        </linearGradient>
        
        <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#c4c4c4"/>
            <stop offset="100%" stop-color="#0059ff"/>
        </linearGradient>
        
        <filter id="neonGlow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        
        <filter id="textGlow">
            <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#0059ff" flood-opacity="0.6"/>
        </filter>
    </defs>
    
    <!-- Hintergrund -->
    <rect width="500" height="320" fill="url(#bgGradient)" rx="8" ry="8"/>
    
    <!-- Header -->
    <text x="250" y="40" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700" fill="url(#textGradient)" filter="url(#textGlow)">
        Codewars Stats
    </text>
    
    <text x="250" y="60" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="rgba(255,255,255,0.7)">
        @{USERNAME}
    </text>
    
    <!-- Hauptdaten - groß und prominent -->
    <g font-family="Segoe UI, Arial, sans-serif">
        <!-- Honor -->
        <text x="100" y="100" text-anchor="middle" font-size="14" fill="rgba(255,255,255,0.8)">Honor</text>
        <text x="100" y="125" text-anchor="middle" font-size="28" font-weight="700" fill="url(#textGradient)" filter="url(#neonGlow)">{honor}</text>
        
        <!-- Rank -->
        <text x="250" y="100" text-anchor="middle" font-size="14" fill="rgba(255,255,255,0.8)">Global Rank</text>
        <text x="250" y="125" text-anchor="middle" font-size="28" font-weight="700" fill="url(#textGradient)" filter="url(#neonGlow)">
            #{leaderboard_position if leaderboard_position != "N/A" else "N/A"}
        </text>
        
        <!-- Katas -->
        <text x="400" y="100" text-anchor="middle" font-size="14" fill="rgba(255,255,255,0.8)">Katas</text>
        <text x="400" y="125" text-anchor="middle" font-size="28" font-weight="700" fill="url(#textGradient)" filter="url(#neonGlow)">{completed_katas}</text>
    </g>
    
    <!-- Rank Info -->
    <rect x="125" y="150" width="250" height="40" fill="rgba(255,255,255,0.05)" rx="6" ry="6"/>
    <text x="250" y="165" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="rgba(255,255,255,0.9)">Overall Rank</text>
    <text x="250" y="185" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600" fill="url(#textGradient)">{overall_rank} ({rank_score} pts)</text>
    
    <!-- Sprachen Chart -->
    <text x="250" y="220" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600" fill="rgba(255,255,255,0.9)">Top Languages</text>
    
    <g transform="translate(50 235)">'''

# Sprach-Balken
bar_height = 20
bar_spacing = 8
for i, (lang_name, lang_rank, lang_score) in enumerate(top_languages):
    bar_width = (lang_score / max_score) * 360
    y_pos = i * (bar_height + bar_spacing)
    
    svg_content += f'''
        <rect x="0" y="{y_pos}" width="400" height="{bar_height}" fill="rgba(255,255,255,0.1)" rx="3" ry="3"/>
        <rect x="0" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="rgba(0,89,255,0.6)" rx="3" ry="3"/>
        <text x="5" y="{y_pos + 14}" font-size="12" fill="#ffffff" font-weight="600">{lang_name}</text>
        <text x="395" y="{y_pos + 14}" text-anchor="end" font-size="11" fill="rgba(255,255,255,0.8)">{lang_score} pts</text>'''

svg_content += f'''
    </g>
    
    <!-- Footer -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="11" fill="rgba(255,255,255,0.6)">
        <text x="20" y="310">Authored: {authored_katas}</text>
        <text x="250" y="310" text-anchor="middle">Updated: {current_time}</text>
    </g>
    
    <!-- Neon-Effekte -->
    <circle cx="480" cy="20" r="3" fill="rgba(0,89,255,0.6)" filter="url(#neonGlow)"/>
    <circle cx="490" cy="30" r="2" fill="rgba(0,89,255,0.4)" filter="url(#neonGlow)"/>
</svg>'''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Neon-SVG erfolgreich erstellt: {OUTPUT_FILE}")
