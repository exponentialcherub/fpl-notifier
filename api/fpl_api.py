import requests_cache
import os
import json

from requests_cache import DO_NOT_CACHE


class FplAPI(object):
    def __init__(self, draft_domain):
        self.draft_domain = draft_domain
        self._gameweeks_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "resources", "gameweeks.json"
        )

        urls_expire_after = {
            f'{draft_domain}/league/*/details': 60,
            f'{draft_domain}/bootstrap-static': 60*60*60*12,
            '*': DO_NOT_CACHE,
        }

        self.session = requests_cache.CachedSession('fpl_api', urls_expire_after=urls_expire_after)

    def _get_details(self, league_id):
        return self.session.get(f"{self.draft_domain}/league/{league_id}/details").json()

    def get_teams(self, league_id):
        league_details = self._get_details(league_id)
        teams = {team['id']: team['entry_name'] for team in league_details['league_entries']}
        return teams

    def get_standings(self, league_id):
        league_details = self._get_details(league_id)
        standings = league_details["standings"]
        return standings

    def get_players(self):
        bootstrap = self.session.get(f"{self.draft_domain}/bootstrap-static").json()
        players = {p['id']: p['web_name'] for p in bootstrap['elements']}
        return players

    def get_transactions(self, league_id):
        url = f"{self.draft_domain}/draft/league/{league_id}/trades"
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()['trades']

    def get_gameweek_details(self):
        gameweeks_path = os.path.abspath(self._gameweeks_path)
        if os.path.exists(gameweeks_path):
            with open(gameweeks_path, "r") as f:
                return json.load(f).get("events")["data"]
        return None
