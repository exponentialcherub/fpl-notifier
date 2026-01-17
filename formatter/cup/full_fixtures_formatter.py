# formatter/full_fixtures_formatter.py
from formatter.formatting_constants import alignment_width

SEPARATOR_WIDTH = 25

def _format_group_fixtures(group_name, fixtures, current_gameweek):
    output = []
    output.append(f"\n{'=' * SEPARATOR_WIDTH}")
    output.append(f"GROUP {group_name}")
    output.append(f"{'=' * SEPARATOR_WIDTH}")

    output.append(f"\n{'GW':<5} {'Home':<{alignment_width}} vs {'Away':<{alignment_width}}")
    output.append("-" * SEPARATOR_WIDTH)

    for fixture in fixtures:
        gw = fixture.gameweek
        if gw >= current_gameweek:
            output.append(f"GW{gw:<3} {fixture.home:<{alignment_width}} vs {fixture.away:<{alignment_width}}")

    return output
def format_full_fixtures(fixtures, current_gameweek):
    output = []
    output.append("=" * SEPARATOR_WIDTH)
    output.append(f"FULL FIXTURES \n(Current: GW{current_gameweek})")
    output.append("=" * SEPARATOR_WIDTH)

    output.extend(_format_group_fixtures('A', fixtures.group_A, current_gameweek))
    output.extend(_format_group_fixtures('B', fixtures.group_B, current_gameweek))

    output.append("\n" + "=" * SEPARATOR_WIDTH)
    return "\n".join(output)
