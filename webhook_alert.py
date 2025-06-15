import json
import requests
from datetime import datetime
from pytz import timezone

# Load cached props
with open("props_cache.json", "r") as f:
    props_cache = json.load(f)

# Set player and matchup to pull
player_name = "Tyrese Haliburton"
player_key = player_name.lower()
matchup = "IND @ BOS"

# ✅ Your live webhook URL
webhook_url = "https://discord.com/api/webhooks/1383639399790546995/ZnI3bHlOrlcRc9FKtHOkIsvTKASuJGoXYte_aoVLF2BwJ7sjWKhtxwLD2n0lyGqG7Ncp"

# Team emoji + logo map
team_data = {
    "IND": {
        "emoji": "🔵",
        "logo": "https://loodibee.com/wp-content/uploads/nba-indiana-pacers-logo.png"
    },
    "BOS": {
        "emoji": "☘️",
        "logo": "https://loodibee.com/wp-content/uploads/nba-boston-celtics-logo.png"
    }
    # Add more teams and sports here
}

# Pull player data
player_data = props_cache.get("nba", {}).get(player_key)
if not player_data:
    print(f"❌ No props found for {player_name}")
    exit()

props = player_data.get("props", {})
team_code = matchup.split(" @ ")[0].strip()

emoji = team_data.get(team_code, {}).get("emoji", "🏀")
logo = team_data.get(team_code, {}).get("logo", "")

# Build Discord embed
embed = {
    "title": f"{emoji} {player_name} - NBA",
    "description": f"📊 **Matchup:** `{matchup}`",
    "color": 5814783,
    "footer": {
        "text": f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    },
    "fields": [],
}

if logo:
    embed["thumbnail"] = {"url": logo}

for stat, books in props.items():
    fd = books.get("fanduel", {})
    dk = books.get("draftkings", {})
    embed["fields"].append({
        "name": f"**{stat.title()}**",
        "value": f"📉 **FD:** {fd.get('line', 'N/A')} @ {fd.get('odds', 'N/A')} | **DK:** {dk.get('line', 'N/A')} @ {dk.get('odds', 'N/A')}",
        "inline": False
    })

# Send to Discord
payload = {
    "username": "Prop Sharks Bot",
    "avatar_url": "https://i.imgur.com/E7wGd5Y.png",
    "embeds": [embed]
}

r = requests.post(webhook_url, json=payload)
print("✅ Webhook sent" if r.status_code == 204 else f"❌ Failed to send: {r.status_code}")
