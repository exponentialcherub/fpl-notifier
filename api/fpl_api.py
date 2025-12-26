import requests
import os
import json

GAMEWEEKS = "./resources/gameweeks.json"

class FplAPI(object):
    def __init__(self, draft_domain):
        self.draft_domain = draft_domain

    def get_teams(self, league_id):
        league_details = requests.get(f"{self.draft_domain}/league/{league_id}/details").json()
        teams = {team['entry_id']: team['entry_name'] for team in league_details['league_entries']}
        return teams

    def get_players(self):
        bootstrap = requests.get(f"{self.draft_domain}/bootstrap-static").json()
        players = {p['id']: p['web_name'] for p in bootstrap['elements']}
        return players

    def get_transactions(self, league_id):
        url = f"{self.draft_domain}/draft/league/{league_id}/trades"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()['trades']

    @staticmethod
    def get_gameweek_details():
        if os.path.exists(GAMEWEEKS):
            with open(GAMEWEEKS, "r") as f:
                return json.load(f).get("events")["data"]
        return None
