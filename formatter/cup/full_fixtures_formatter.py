# formatter/full_fixtures_formatter.py

def _format_group_fixtures(group_name, fixtures, current_gameweek):
    output = []
    output.append(f"\n{'=' * 100}")
    output.append(f"GROUP {group_name}")
    output.append(f"{'=' * 100}")

    output.append(f"\n{'GW':<5} {'Home Team':<25} vs {'Away Team':<25} {'Status':<15}")
    output.append("-" * 75)

    for fixture in fixtures:
        gw = fixture.gameweek
        status = "Completed" if gw <= current_gameweek else "Upcoming"
        output.append(f"GW{gw:<3} {fixture.home:<25} vs {fixture.away:<25} {status:<15}")

    return output
def format_full_fixtures(fixtures, current_gameweek):
    output = []
    output.append("=" * 100)
    output.append(f"FPL DRAFT CUP - FULL FIXTURE LIST (Current: GW{current_gameweek})")
    output.append("=" * 100)

    output.extend(_format_group_fixtures('A', fixtures.group_A, current_gameweek))
    output.extend(_format_group_fixtures('B', fixtures.group_B, current_gameweek))

    output.append("\n" + "=" * 100)
    return "\n".join(output)
