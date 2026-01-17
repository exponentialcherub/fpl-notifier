# formatter/results_formatter.py

SEPARATOR_WIDTH = 25

def _format_group_results(group_name, results, current_gameweek):
    output = []

    output.append(f"\n{'=' * SEPARATOR_WIDTH}")
    output.append(f"GROUP {group_name}")
    output.append(f"{'=' * SEPARATOR_WIDTH}")

    # Latest round
    latest_round = [r for r in results if r['gameweek'] == current_gameweek]
    if latest_round:
        output.append(f"\nLATEST ROUND (GW{current_gameweek}):")
        output.append(f"{'Home':<5} {'Score':<5} {'Away':<5} {'Result'}")
        output.append("-" * SEPARATOR_WIDTH)
        for match in latest_round:
            output.append(
                f"{match['home']:<5} {match['home_points']}-{match['away_points']:<3} {match['away']:<5} {match['result']}")

    # Aggregate results
    output.append(f"\nALL RESULTS:")
    output.append(f"{'GW':<5} {'Home':<5} {'Score':<5} {'Away'} {'Result':<5}")
    output.append("-" * SEPARATOR_WIDTH)
    for match in results:
        output.append(
            f"GW{match['gameweek']:<3} {match['home']:<5} {match['home_points']}-{match['away_points']:<2} {match['away']:<5} {match['result']}")

    return output

def format_results(results_a, results_b, current_gameweek):
    output = []
    output.append("=" * SEPARATOR_WIDTH)
    output.append(f"CUP RESULTS (up to GW{current_gameweek})")
    output.append("=" * SEPARATOR_WIDTH)

    output.extend(_format_group_results('A', results_a, current_gameweek))
    output.extend(_format_group_results('B', results_b, current_gameweek))

    output.append("\n" + "=" * SEPARATOR_WIDTH)
    return "\n".join(output)
