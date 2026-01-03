import requests
import os
import json

class FplAPI(object):
    def __init__(self, draft_domain):
        self.draft_domain = draft_domain
        self._gameweeks_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "resources", "gameweeks.json"
        )

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

    def get_gameweek_details(self):
        gameweeks_path = os.path.abspath(self._gameweeks_path)
        if os.path.exists(gameweeks_path):
            with open(gameweeks_path, "r") as f:
                return json.load(f).get("events")["data"]
        return None

    def get_team_gameweek_points(self, team_id, gameweek):
        """Get points for a specific team in a specific gameweek"""
        url = f"{self.draft_domain}/entry/{team_id}/event/{gameweek}/picks"
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def get_league_gameweek_scores(self, league_id, gameweek):
        """Get all managers' points for a specific gameweek using manager IDs"""
        # Load managers config
        managers_config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "config", "managers_config.json"
        )
        
        with open(managers_config_path, 'r') as f:
            managers_data = json.load(f)
        
        scores = {}
        for manager in managers_data['managers']:
            entry_id = manager['code']
            manager_name = manager['name']
            
            try:
                url = f"{self.draft_domain}/entry/{entry_id}/history"
                r = requests.get(url)
                r.raise_for_status()
                data = r.json()
                
                # Find the specific gameweek in the history
                gameweek_data = next(
                    (gw for gw in data['history'] if gw['event'] == gameweek),
                    None
                )
                
                if gameweek_data:
                    scores[entry_id] = {
                        'manager_name': manager_name,
                        'abbreviation': manager['abbreviation'],
                        'points': gameweek_data['points'],
                        'total_points': gameweek_data['total_points'],
                        'points_on_bench': gameweek_data.get('points_on_bench', 0)
                    }
                else:
                    scores[entry_id] = {
                        'manager_name': manager_name,
                        'abbreviation': manager['abbreviation'],
                        'points': 0,
                        'total_points': 0,
                        'error': f'No data for gameweek {gameweek}'
                    }
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    scores[entry_id] = {
                        'manager_name': manager_name,
                        'abbreviation': manager['abbreviation'],
                        'points': 0,
                        'total_points': 0,
                        'error': f'No data available for gameweek {gameweek}'
                    }
                else:
                    scores[entry_id] = {
                        'manager_name': manager_name,
                        'abbreviation': manager['abbreviation'],
                        'points': 0,
                        'error': str(e)
                    }
            except Exception as e:
                scores[entry_id] = {
                    'manager_name': manager_name,
                    'abbreviation': manager['abbreviation'],
                    'points': 0,
                    'error': str(e)
                }
        
        return scores
