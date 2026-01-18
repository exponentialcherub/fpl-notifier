# formatter/current_gw_formatter.py
from config.cup_config import Fixtures
from config.manager_config import ManagerConfig
from api.fpl_api import FplAPI

MAX_GW = 38


def _format_current_group_fixtures(group_name, group_fixtures, current_gw: int, scores: dict, manager_config: ManagerConfig):
    """Format current gameweek fixtures with live scores"""
    output = []
    current_fixtures = [f for f in group_fixtures if f.gameweek == current_gw]

    if current_fixtures:
        output.append(f"\n{'=' * 100}")
        output.append(f"GROUP {group_name}")
        output.append(f"{'=' * 100}")
        output.append(f"\n{'Home Team':<25} {'Pts':>6}  -  {'Pts':<6} {'Away Team':<25}")
        output.append("-" * 70)
        for fixture in current_fixtures:
            # Get manager codes to lookup scores
            home_code = manager_config.by_name.get(fixture.home)
            away_code = manager_config.by_name.get(fixture.away)
            
            home_points = scores.get(home_code.code, 0) if home_code else 0
            away_points = scores.get(away_code.code, 0) if away_code else 0
            
            output.append(f"{fixture.home:<25} {home_points:>6}  -  {away_points:<6} {fixture.away:<25}")

    return output


def current_gw_formatter(fixtures: Fixtures, current_gameweek: int, fpl_api: FplAPI, league_id: int, manager_config: ManagerConfig):
    """Return current gameweek's fixtures with live scores as a formatted string"""
    output = []
    
    if current_gameweek > MAX_GW:
        output.append("=" * 100)
        output.append("FPL DRAFT CUP - NO UPCOMING FIXTURES")
        output.append("=" * 100)
        output.append("\nAll cup fixtures have been completed!")
        output.append("\n" + "=" * 100)
        return "\n".join(output)

    # Get current scores for this gameweek
    scores = fpl_api.get_league_gameweek_scores(league_id, current_gameweek)

    output.append("=" * 100)
    output.append(f"FPL DRAFT CUP - LIVE SCORES (GW{current_gameweek})")
    output.append("=" * 100)

    output.extend(_format_current_group_fixtures('A', fixtures.group_A, current_gameweek, scores, manager_config))
    output.extend(_format_current_group_fixtures('B', fixtures.group_B, current_gameweek, scores, manager_config))
    output.append("\n" + "=" * 100)
    return "\n".join(output)
