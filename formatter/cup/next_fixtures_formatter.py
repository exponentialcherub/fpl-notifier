# formatter/next_fixtures_formatter.py
from config.cup_config import Fixtures

MAX_GW = 38

def _get_next_fixture_gameweek(fixtures: Fixtures, current_gameweek: int):
    next_gw = current_gameweek + 1

    # Find the next gameweek with fixtures
    while next_gw <= MAX_GW:
        has_fixtures = any(
            any(fixture.gameweek == next_gw for fixture in group_fixtures)
            for group_fixtures in [fixtures.group_A, fixtures.group_B]
        )
        if has_fixtures:
            break
        next_gw += 1

    return next_gw

def _format_next_group_fixtures(group_name, group_fixtures, next_gw: int):
    output = []
    next_fixtures = [f for f in group_fixtures if f.gameweek == next_gw]

    if next_fixtures:
        output.append(f"\n{'=' * 100}")
        output.append(f"GROUP {group_name}")
        output.append(f"{'=' * 100}")
        output.append(f"\n{'Home Team':<25} vs {'Away Team':<25}")
        output.append("-" * 55)
        for fixture in next_fixtures:
            output.append(f"{fixture.home:<25} vs {fixture.away:<25}")

    return output


def format_next_fixtures(fixtures: Fixtures, current_gameweek):
    """Return next week's fixtures as a formatted string"""
    next_gw = _get_next_fixture_gameweek(fixtures, current_gameweek)

    output = []
    if next_gw > MAX_GW:
        output.append("=" * 100)
        output.append("FPL DRAFT CUP - NO UPCOMING FIXTURES")
        output.append("=" * 100)
        output.append("\nAll cup fixtures have been completed!")
        output.append("\n" + "=" * 100)
        return "\n".join(output)

    output.append("=" * 100)
    output.append(f"FPL DRAFT CUP - NEXT FIXTURES (GW{next_gw})")
    output.append("=" * 100)

    output.extend(_format_next_group_fixtures('A', fixtures.group_A, next_gw))
    output.extend(_format_next_group_fixtures('B', fixtures.group_B, next_gw))

    output.append("\n" + "=" * 100)
    return "\n".join(output)
