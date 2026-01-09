def calculate_league_table(results, teams):
    """Calculate league table from match results"""
    table = {}

    # Initialize table
    for team in teams:
        table[team] = {
            'played': 0,
            'won': 0,
            'drawn': 0,
            'lost': 0,
            'points_for': 0,
            'points_against': 0,
            'points_diff': 0,
            'match_points': 0
        }

    # Process results
    for match in results:
        home = match['home']
        away = match['away']

        table[home]['played'] += 1
        table[away]['played'] += 1

        table[home]['points_for'] += match['home_points']
        table[home]['points_against'] += match['away_points']
        table[away]['points_for'] += match['away_points']
        table[away]['points_against'] += match['home_points']

        table[home]['match_points'] += match['home_match_points']
        table[away]['match_points'] += match['away_match_points']

        if match['result'] == 'H':
            table[home]['won'] += 1
            table[away]['lost'] += 1
        elif match['result'] == 'A':
            table[away]['won'] += 1
            table[home]['lost'] += 1
        else:
            table[home]['drawn'] += 1
            table[away]['drawn'] += 1

        table[home]['points_diff'] = table[home]['points_for'] - table[home]['points_against']
        table[away]['points_diff'] = table[away]['points_for'] - table[away]['points_against']

    # Sort by match points, then points difference, then points for
    sorted_table = sorted(
        table.items(),
        key=lambda x: (x[1]['match_points'], x[1]['points_diff'], x[1]['points_for']),
        reverse=True
    )

    return sorted_table