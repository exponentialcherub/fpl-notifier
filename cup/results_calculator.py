from typing import List

from api.fpl_api import FplAPI
from config.cup_config import Fixture
from config.manager_config import ManagerConfig


def calculate_results(league_id, fpl_api: FplAPI, fixtures: List[Fixture], manager_config: ManagerConfig, current_gameweek):
    """Process fixtures and return match results"""
    results = []

    for fixture in fixtures:
        gw = fixture.gameweek

        # Only process fixtures that have happened (before or equal to current gameweek)
        if gw > current_gameweek:
            continue

        home_team = fixture.home
        away_team = fixture.away

        # Get manager codes
        home_code = manager_config.by_name[home_team].code
        away_code = manager_config.by_name[away_team].code

        if not home_code or not away_code:
            continue

        # Get scores for this gameweek
        scores = fpl_api.get_league_gameweek_scores(league_id, gw)
        home_points = scores.get(home_code, {})
        away_points = scores.get(away_code, {})

        # Determine result
        if home_points > away_points:
            result = 'H'
            home_match_points = 3
            away_match_points = 0
        elif away_points > home_points:
            result = 'A'
            home_match_points = 0
            away_match_points = 3
        else:
            result = 'D'
            home_match_points = 1
            away_match_points = 1

        results.append({
            'gameweek': gw,
            'home': home_team,
            'away': away_team,
            'home_points': home_points,
            'away_points': away_points,
            'result': result,
            'home_match_points': home_match_points,
            'away_match_points': away_match_points
        })

    return results