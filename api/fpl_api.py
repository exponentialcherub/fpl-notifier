from datetime import timezone, datetime
from typing import List

import requests_cache
import os
import json

from requests_cache import DO_NOT_CACHE

class FplTeam(object):
    def __init__(self, team):
        self.id = team['id']
        self.entry_id = team['entry_id']
        self.name = team['entry_name']

class FplTeams(object):
    def __init__(self, teams: List[FplTeam]):
        self.by_id = {t.id: t for t in teams}
        self.by_entry_id = {t.entry_id: t for t in teams}

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
            f'{draft_domain}/entry/*/history': 60,
            '*': DO_NOT_CACHE,
        }

        self.session = requests_cache.CachedSession('fpl_api', urls_expire_after=urls_expire_after)

    def _get_details(self, league_id):
        r = self.session.get(f"{self.draft_domain}/league/{league_id}/details")
        r.raise_for_status()
        return r.json()

    def get_teams(self, league_id):
        league_details = self._get_details(league_id)
        return FplTeams([FplTeam(t) for t in league_details['league_entries']])

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

    def get_current_gameweek(self):
        now = datetime.now(timezone.utc)

        gameweek_details = self.get_gameweek_details()

        # Find current gameweek
        for event in gameweek_details:
            deadline = datetime.fromisoformat(event['deadline_time'])
            if now < deadline:
                # Current gameweek is the one before the next deadline
                return max(1, event['id'] - 1)

        # If no future deadline found, return last gameweek
        return gameweek_details[-1]['id']

    def get_gameweek_scores(self, entry_id, gameweek):
        url = f"{self.draft_domain}/entry/{entry_id}/history"
        r = self.session.get(url)
        r.raise_for_status()
        data = r.json()

        # Find the specific gameweek in the history
        gameweek_data = next(
            (gw for gw in data['history'] if gw['event'] == gameweek),
            None
        )

        return gameweek_data.get('points', 0)

    def get_league_gameweek_scores(self, league_id, gameweek):
        """Get all points for a specific gameweek for given managers"""

        teams = self.get_teams(league_id)
        
        scores = {}
        for entry_id in teams.by_entry_id:
            team = teams.by_entry_id[entry_id]
            team_scores = self.get_gameweek_scores(entry_id, gameweek)
            scores[team.id] = team_scores

        return scores
