# formatter/results_formatter.py

def _format_group_results(group_name, results, current_gameweek):
    output = []

    output.append(f"\n{'=' * 100}")
    output.append(f"GROUP {group_name}")
    output.append(f"{'=' * 100}")

    # Latest round
    latest_round = [r for r in results if r['gameweek'] == current_gameweek]
    if latest_round:
        output.append(f"\nLATEST ROUND (GW{current_gameweek}):")
        output.append(f"{'Home Team':<20} {'Score':<10} {'Away Team':<20} {'Result':<8}")
        output.append("-" * 60)
        for match in latest_round:
            output.append(
                f"{match['home']:<20} {match['home_points']:<3}-{match['away_points']:<6} {match['away']:<20} {match['result']:<8}")

    # Aggregate results
    output.append(f"\nALL RESULTS:")
    output.append(f"{'GW':<5} {'Home Team':<20} {'Score':<10} {'Away Team':<20} {'Result':<8}")
    output.append("-" * 70)
    for match in results:
        output.append(
            f"GW{match['gameweek']:<3} {match['home']:<20} {match['home_points']:<3}-{match['away_points']:<6} {match['away']:<20} {match['result']:<8}")

    return output

def format_results(results_a, results_b, current_gameweek):
    output = []
    output.append("=" * 100)
    output.append(f"FPL DRAFT CUP - MATCH RESULTS (up to GW{current_gameweek})")
    output.append("=" * 100)

    output.extend(_format_group_results('A', results_a, current_gameweek))
    output.extend(_format_group_results('B', results_b, current_gameweek))

    output.append("\n" + "=" * 100)
    return "\n".join(output)
