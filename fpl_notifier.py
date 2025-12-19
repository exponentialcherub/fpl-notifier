import requests
import json
import os

# === CONFIG ===
LEAGUE_ID = "12557"  # your FPL Draft league ID

LAST_TRADE_FILE = "last_trade_id.json"

def get_teams():
    league_details = requests.get(f"https://draft.premierleague.com/api/league/{LEAGUE_ID}/details").json()
    teams = {team['entry_id']: team['entry_name'] for team in league_details['league_entries']}
    return teams

def get_players():
    bootstrap = requests.get("https://draft.premierleague.com/api/bootstrap-static").json()
    players = {p['id']: p['web_name'] for p in bootstrap['elements']}
    return players

def get_transactions():
    url = f"https://draft.premierleague.com/api/draft/league/{LEAGUE_ID}/trades"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()['trades']

def load_last_trade_id():
    if os.path.exists(LAST_TRADE_FILE):
        with open(LAST_TRADE_FILE, "r") as f:
            return json.load(f).get("last_trade_id")
    return None

def save_last_trade_id(trade_id):
    with open(LAST_TRADE_FILE, "w") as f:
        json.dump({"last_trade_id": trade_id}, f)

def send_whatsapp_message(body):
    queue_publish_url = "http://localhost:5001/publish/notify"
    print("Sending message to queue: " + queue_publish_url)
    response = requests.post(queue_publish_url, json={"message": body})
    print(response.text)

def main():
    transactions = get_transactions()
    players = get_players()
    teams = get_teams()
    last_seen = load_last_trade_id()

    # Sort by most recent first
    sorted_tx = sorted(transactions, key=lambda x: x['response_time'], reverse=True)

    for tx in sorted_tx:
        trade_id = tx["id"]
        if trade_id != last_seen:
            # Build trade message
            offered_team = teams[tx['offered_entry']]
            received_team = teams[tx['received_entry']]
            ins = "\n".join([players[trade_item['element_in']] for trade_item in tx['tradeitem_set']])
            outs = "\n".join([players[trade_item['element_out']] for trade_item in tx['tradeitem_set']])
            message = f"🚨 New Trade Alert 🚨\n*{offered_team}*\n{ins}\n ↔️ \n*{received_team}*\n{outs}"
            print(message)
            send_whatsapp_message(message)
            save_last_trade_id(trade_id)
        break  # Only alert on newest trade

if __name__ == "__main__":
    main()
