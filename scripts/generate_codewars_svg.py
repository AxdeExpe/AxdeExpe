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

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="340" viewBox="0 0 520 340">
    <defs>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0f1117"/>
            <stop offset="100%" stop-color="#181b25"/>
        </linearGradient>
        
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#c4c4c4"/>
            <stop offset="100%" stop-color="#0059ff"/>
        </linearGradient>
        
        <filter id="softGlow">
            <feGaussianBlur stdDeviation="2" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
    </defs>
    
    <!-- Hintergrund -->
    <rect width="520" height="340" fill="url(#bgGradient)" rx="8" ry="8"/>
    
    <!-- Header Box -->
    <rect x="10" y="10" width="500" height="50" fill="rgba(22, 27, 34, 0.8)" rx="6" ry="6"/>
    <text x="260" y="35" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="18" font-weight="600" fill="#e6edf3">
        Codewars Statistics
    </text>
    <text x="260" y="50" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#7d8590">
        @{USERNAME}
    </text>
    
    <!-- Hauptdaten Boxen -->
    <g font-family="'Segoe UI', Arial, sans-serif">
        <!-- Honor Box -->
        <rect x="20" y="75" width="150" height="80" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <text x="95" y="100" text-anchor="middle" font-size="14" fill="#7d8590">Honor</text>
        <text x="95" y="125" text-anchor="middle" font-size="26" font-weight="700" fill="#e6edf3">{honor}</text>
        
        <!-- Rank Box -->
        <rect x="185" y="75" width="150" height="80" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <text x="260" y="100" text-anchor="middle" font-size="14" fill="#7d8590">Global Rank</text>
        <text x="260" y="125" text-anchor="middle" font-size="26" font-weight="700" fill="#e6edf3">
            #{leaderboard_position if leaderboard_position != "N/A" else "N/A"}
        </text>
        
        <!-- Katas Box -->
        <rect x="350" y="75" width="150" height="80" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
        <text x="425" y="100" text-anchor="middle" font-size="14" fill="#7d8590">Katas Solved</text>
        <text x="425" y="125" text-anchor="middle" font-size="26" font-weight="700" fill="#e6edf3">{completed_katas}</text>
    </g>
    
    <!-- Rank Info Box -->
    <rect x="20" y="170" width="480" height="50" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <text x="250" y="190" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="14" fill="#7d8590">Overall Rank</text>
    <text x="250" y="210" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="16" font-weight="600" fill="#e6edf3">
        {overall_rank} • {rank_score} points
    </text>
    
    <!-- Sprachen Box -->
    <rect x="20" y="235" width="480" height="70" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <text x="250" y="255" text-anchor="middle" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="600" fill="#e6edf3">Top Languages</text>
    
    <!-- Sprach-Balken -->
    <g transform="translate(40 270)">'''

# Sprach-Balken
bar_width = 400
bar_height = 8
bar_spacing = 12
y_offset = 0

for i, (lang_name, lang_rank, lang_score) in enumerate(top_languages):
    fill_width = (lang_score / max_score) * bar_width if max_score > 0 else 0
    y_pos = i * (bar_height + bar_spacing)
    
    svg_content += f'''
        <text x="0" y="{y_pos + 6}" font-size="11" fill="#7d8590">{lang_name}</text>
        <rect x="80" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="rgba(125, 133, 144, 0.2)" rx="4" ry="4"/>
        <rect x="80" y="{y_pos}" width="{fill_width}" height="{bar_height}" fill="url(#accentGradient)" rx="4" ry="4"/>
        <text x="{bar_width + 85}" y="{y_pos + 6}" font-size="10" fill="#7d8590" text-anchor="end">{lang_score}</text>'''

svg_content += f'''
    </g>
    
    <!-- Footer Box -->
    <rect x="20" y="320" width="480" height="40" fill="rgba(22, 27, 34, 0.9)" rx="6" ry="6"/>
    <g font-family="'Segoe UI', Arial, sans-serif" font-size="11" fill="#7d8590">
        <text x="40" y="335">Authored Katas: <tspan fill="#e6edf3" font-weight="600">{authored_katas}</tspan></text>
        <text x="260" y="335" text-anchor="middle">Updated: {current_time}</text>
        <text x="460" y="335" text-anchor="end">Rank: <tspan fill="#e6edf3" font-weight="600">{overall_rank}</tspan></text>
    </g>
    
    <!-- Subtile Akzente -->
    <line x1="20" y1="165" x2="500" y2="165" stroke="rgba(0,89,255,0.3)" stroke-width="1"/>
    <line x1="20" y1="230" x2="500" y2="230" stroke="rgba(0,89,255,0.3)" stroke-width="1"/>
    <line x1="20" y1="315" x2="500" y2="315" stroke="rgba(0,89,255,0.3)" stroke-width="1"/>
</svg>'''

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Technisches SVG erfolgreich erstellt: {OUTPUT_FILE}")
