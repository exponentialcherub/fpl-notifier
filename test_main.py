from api.fpl_api import FplAPI
from config.config import Config
import json
import os

def load_cup_config():
    """Load the cup configuration"""
    cup_config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config", "cup_config.json"
    )
    with open(cup_config_path, 'r') as f:
        return json.load(f)

def get_manager_code(manager_name, managers_config_path):
    """Get manager code from manager name"""
    with open(managers_config_path, 'r') as f:
        managers_data = json.load(f)
    
    for manager in managers_data['managers']:
        if manager['name'] == manager_name:
            return manager['code'], manager['abbreviation']
    return None, None

def process_fixtures(fpl_api, fixtures, group_name, current_gameweek):
    """Process fixtures and return match results"""
    managers_config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config", "managers_config.json"
    )
    
    results = []
    
    for fixture in fixtures:
        gw = fixture['gameweek']
        
        # Only process fixtures that have happened (before or equal to current gameweek)
        if gw > current_gameweek:
            continue
            
        home_team = fixture['home']
        away_team = fixture['away']
        
        # Get manager codes
        home_code, home_abbr = get_manager_code(home_team, managers_config_path)
        away_code, away_abbr = get_manager_code(away_team, managers_config_path)
        
        if not home_code or not away_code:
            continue
        
        # Get scores for this gameweek
        scores = fpl_api.get_league_gameweek_scores(None, gw)
        
        home_points = scores.get(home_code, {}).get('points', 0)
        away_points = scores.get(away_code, {}).get('points', 0)
        
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

def main():
    # Load configuration
    config = Config()
    cup_config = load_cup_config()
    
    # Initialize FPL API
    fpl_api = FplAPI(config.fpl_domain)
    
    # Current gameweek to process up to
    current_gameweek = 22  # Change this to process more gameweeks
    
    print("=" * 100)
    print(f"FPL DRAFT CUP - Match Results & League Tables (up to GW{current_gameweek})")
    print("=" * 100)
    
    # Process each group
    for group_name in ['A', 'B']:
        group_key = f'group_{group_name}'
        fixtures = cup_config['fixtures'][group_key]
        teams = cup_config['groups'][group_name]['teams']
        
        print(f"\n{'=' * 100}")
        print(f"GROUP {group_name}")
        print(f"{'=' * 100}")
        
        # Process fixtures
        results = process_fixtures(fpl_api, fixtures, group_name, current_gameweek)
        
        # Print match results
        print(f"\nMATCH RESULTS:")
        print(f"{'GW':<5} {'Home Team':<20} {'Score':<10} {'Away Team':<20} {'Result':<8}")
        print("-" * 70)
        
        for match in results:
            print(f"GW{match['gameweek']:<3} {match['home']:<20} {match['home_points']:<3}-{match['away_points']:<6} {match['away']:<20} {match['result']:<8}")
        
        # Calculate and print league table
        table = calculate_league_table(results, teams)
        
        print(f"\nLEAGUE TABLE:")
        print(f"{'Pos':<5} {'Team':<20} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'PF':<6} {'PA':<6} {'Diff':<7} {'Pts':<5}")
        print("-" * 75)
        
        for pos, (team, stats) in enumerate(table, 1):
            print(f"{pos:<5} {team:<20} {stats['played']:<4} {stats['won']:<4} {stats['drawn']:<4} {stats['lost']:<4} "
                  f"{stats['points_for']:<6} {stats['points_against']:<6} {stats['points_diff']:<+7} {stats['match_points']:<5}")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    main()
