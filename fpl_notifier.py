import requests
import json
import os
from datetime import datetime, timezone

# === CONFIG ===
LEAGUE_ID = "12557"  # your FPL Draft league ID

LAST_TRADE_FILE = "last_trade_id.json"
NOTIFIED_LOG = "notified_log.json"
GAMEWEEKS = "gameweeks.json"

NOTIFY_TIME = 43200

# Readers #

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

def get_last_notified_waiver_gameweek():
    if os.path.exists(NOTIFIED_LOG):
        with open(NOTIFIED_LOG, "r") as f:
            return json.load(f).get("waiver_gameweek")
    return 17

def load_gameweek_details():
    if os.path.exists(GAMEWEEKS):
        with open(GAMEWEEKS, "r") as f:
            return json.load(f).get("events")["data"]
    return None

##########

# Writers #

def save_last_trade_id(trade_id):
    with open(LAST_TRADE_FILE, "w") as f:
        json.dump({"last_trade_id": trade_id}, f)

def save_notified_log(waiver_gameweek):
    with open(NOTIFIED_LOG, "w") as f:
        json.dump({"waiver_gameweek": waiver_gameweek}, f)

def send_whatsapp_message(body):
    queue_publish_url = "http://localhost:5001/publish/notify"
    print("Sending message to queue: " + queue_publish_url)
    response = requests.post(queue_publish_url, json={"message": body})
    print(response.text)

###########

def check_and_notify_new_trade():
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

def check_and_notify_waiver():
    next_gameweek_id = get_last_notified_waiver_gameweek() + 1
    gameweeks = load_gameweek_details()

    now = datetime.now(timezone.utc)

    next_gameweek = next(
        (item for item in gameweeks if item['id'] == next_gameweek_id),
        None
    )

    if(next_gameweek):
        next_waiver_datetime = datetime.fromisoformat(next_gameweek['waivers_time'])
        print(next_waiver_datetime)
        print(now)
        diff = next_waiver_datetime - now
        if (diff.total_seconds() < NOTIFY_TIME):
            message = f"Put in your waivers numnuts! Next waiver deadline is {next_waiver_datetime} - t-minus {diff.total_seconds()} seconds!" 
            print(message)
            #send_whatsapp_message(message)
            save_notified_log(next_gameweek_id)

def main():
    #check_and_notify_new_trade()

    check_and_notify_waiver()

if __name__ == "__main__":
    main()
