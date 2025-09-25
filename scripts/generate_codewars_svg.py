import requests
from datetime import datetime
import math

USERNAME = "AxdeExpe"
OUTPUT_FILE = "codewars_stats.svg"

# API-Abfrage
url = f"https://www.codewars.com/api/v1/users/{USERNAME}"
res = requests.get(url)
if res.status_code != 200:
    raise Exception(f"Fehler beim Abrufen der API: {res.status_code}")

data = res.json()

# Erweiterte Daten-Extraktion
honor = data.get("honor", 0)
leaderboard_position = data.get("leaderboardPosition", "N/A")
overall_rank = data.get("ranks", {}).get("overall", {}).get("name", "Unknown")
rank_score = data.get("ranks", {}).get("overall", {}).get("score", 0)
completed_katas = data.get("codeChallenges", {}).get("totalCompleted", 0)
authored_katas = data.get("codeChallenges", {}).get("totalAuthored", 0)

# Sprachendaten mit mehr Details
languages = data.get("ranks", {}).get("languages", {})
sorted_languages = sorted(
    languages.items(), 
    key=lambda x: x[1].get("score", 0), 
    reverse=True
)

# Top 6 Sprachen mit kompletter Datennutzung
top_languages = []
for lang, lang_data in sorted_languages[:6]:
    lang_name = lang.capitalize()
    lang_rank = lang_data.get("name", "Unknown")
    lang_score = lang_data.get("score", 0)
    lang_rank_id = lang_data.get("rank", 0)
    lang_color = lang_data.get("color", "#ffffff")
    top_languages.append((lang_name, lang_rank, lang_score, lang_rank_id, lang_color))

# Chart-Parameter berechnen
max_score = max([lang[2] for lang in top_languages]) if top_languages else 1
chart_height = 120
bar_spacing = 5
available_height = chart_height - (len(top_languages) * bar_spacing)
bar_height = available_height / len(top_languages) if top_languages else 20

# Fortschrittsberechnungen
progress_width = min(440, max(0, (rank_score / 1000) * 440)) if rank_score > 0 else 0
completion_ratio = min(1.0, completed_katas / 500)  # Annahme: 500 als Ziel

# Datum und Zeit
current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# SVG mit modernem Design und Charts
svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="540" height="360" viewBox="0 0 540 360">
    <defs>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0a0f1c"/>
            <stop offset="100%" stop-color="#13182b"/>
        </linearGradient>
        
        <linearGradient id="glassGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="rgba(0,89,255,0.3)"/>
            <stop offset="100%" stop-color="rgba(0,89,255,0.1)"/>
        </linearGradient>
        
        <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="rgba(0,89,255,0.8)"/>
            <stop offset="100%" stop-color="rgba(0,200,255,0.8)"/>
        </linearGradient>
        
        <filter id="glassEffect" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>
            <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" result="glass"/>
        </filter>
        
        <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Hintergrund mit modernem Gradient -->
    <rect width="540" height="360" fill="url(#bgGradient)" rx="12" ry="12"/>
    
    <!-- Glas-Effekt Header -->
    <rect width="540" height="70" fill="url(#glassGradient)" filter="url(#glassEffect)" rx="12" ry="12"/>
    <rect x="10" y="10" width="520" height="50" fill="rgba(0,89,255,0.15)" rx="8" ry="8"/>
    
    <!-- Haupttitel -->
    <text x="270" y="42" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="700" fill="#ffffff" filter="url(#glow)">
        {USERNAME}'s Codewars Statistics
    </text>
    
    <!-- Statistische Karten -->
    <g font-family="Segoe UI, Arial, sans-serif">
        <!-- Honor Card -->
        <rect x="20" y="80" width="150" height="80" fill="rgba(255,255,255,0.05)" rx="8" ry="8"/>
        <text x="95" y="105" text-anchor="middle" font-size="16" font-weight="600" fill="#ffffff">Honor</text>
        <text x="95" y="135" text-anchor="middle" font-size="24" font-weight="700" fill="rgba(0,89,255,0.9)">{honor}</text>
        
        <!-- Rank Card -->
        <rect x="185" y="80" width="150" height="80" fill="rgba(255,255,255,0.05)" rx="8" ry="8"/>
        <text x="260" y="105" text-anchor="middle" font-size="16" font-weight="600" fill="#ffffff">Global Rank</text>
        <text x="260" y="135" text-anchor="middle" font-size="24" font-weight="700" fill="rgba(0,89,255,0.9)">
            #{leaderboard_position if leaderboard_position != "N/A" else "N/A"}
        </text>
        
        <!-- Katas Card -->
        <rect x="350" y="80" width="170" height="80" fill="rgba(255,255,255,0.05)" rx="8" ry="8"/>
        <text x="435" y="105" text-anchor="middle" font-size="16" font-weight="600" fill="#ffffff">Katas Completed</text>
        <text x="435" y="135" text-anchor="middle" font-size="24" font-weight="700" fill="rgba(0,89,255,0.9)">{completed_katas}</text>
    </g>
    
    <!-- Sprachen-Chart Bereich -->
    <rect x="20" y="180" width="500" height="140" fill="rgba(255,255,255,0.02)" rx="8" ry="8"/>
    <text x="270" y="200" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600" fill="#ffffff">
        Top Languages Score Distribution
    </text>
    
    <!-- Balkendiagramm für Sprachen -->
    <g transform="translate(30 210)">'''

# Dynamische Balken für Sprachen-Chart
for i, (lang_name, lang_rank, lang_score, lang_rank_id, lang_color) in enumerate(top_languages):
    bar_width = max(5, (lang_score / max_score) * 400) if max_score > 0 else 5
    y_pos = i * (bar_height + bar_spacing)
    
    svg_content += f'''
        <!-- {lang_name} Bar -->
        <rect x="0" y="{y_pos}" width="400" height="{bar_height}" fill="rgba(255,255,255,0.1)" rx="3" ry="3"/>
        <rect x="0" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="{lang_color}" opacity="0.8" rx="3" ry="3"/>
        <text x="5" y="{y_pos + bar_height - 4}" font-size="11" fill="#ffffff">{lang_name}</text>
        <text x="410" y="{y_pos + bar_height - 4}" font-size="11" fill="rgba(255,255,255,0.7)">{lang_score} pts</text>'''

svg_content += f'''
    </g>
    
    <!-- Progress Bars -->
    <g transform="translate(20 330)">
        <!-- Rank Progress -->
        <text x="0" y="15" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="rgba(255,255,255,0.8)">Rank Progress: {overall_rank}</text>
        <rect x="0" y="20" width="440" height="8" fill="rgba(255,255,255,0.1)" rx="4" ry="4"/>
        <rect x="0" y="20" width="{progress_width}" height="8" fill="url(#progressGradient)" rx="4" ry="4"/>
        
        <!-- Completion Progress -->
        <text x="0" y="45" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="rgba(255,255,255,0.8)">Katas Completion</text>
        <rect x="0" y="50" width="440" height="8" fill="rgba(255,255,255,0.1)" rx="4" ry="4"/>
        <rect x="0" y="50" width="{completion_ratio * 440}" height="8" fill="rgba(0,200,255,0.8)" rx="4" ry="4"/>
    </g>
    
    <!-- Footer mit Authored Katas und Update-Time -->
    <g font-family="Segoe UI, Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.6)">
        <text x="20" y="355">Authored Katas: {authored_katas}</text>
        <text x="270" y="355" text-anchor="middle">Updated: {current_time}</text>
        <text x="520" y="355" text-anchor="end">@{USERNAME}</text>
    </g>
    
    <!-- Dekorative Elemente -->
    <circle cx="520" cy="30" r="4" fill="rgba(0,89,255,0.6)"/>
    <circle cx="530" cy="20" r="3" fill="rgba(0,89,255,0.4)"/>
    <circle cx="510" cy="40" r="2" fill="rgba(0,89,255,0.3)"/>
</svg>'''

# SVG speichern
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Modernes SVG erfolgreich erstellt: {OUTPUT_FILE}")
