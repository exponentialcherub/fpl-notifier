from api.fpl_api import FplAPI
from config.config import Config
import json
import os
import sys
from datetime import datetime, timezone

def load_cup_config():
    """Load the cup configuration"""
    cup_config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "config", "cup_config.json"
    )
    with open(cup_config_path, 'r') as f:
        return json.load(f)

def get_current_gameweek():
    """Get the current gameweek from gameweeks.json"""
    gameweeks_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources", "gameweeks.json"
    )
    
    with open(gameweeks_path, 'r') as f:
        data = json.load(f)
    
    now = datetime.now(timezone.utc)
    
    # Find current gameweek
    for event in data['events']['data']:
        deadline = datetime.fromisoformat(event['deadline_time'])
        if now < deadline:
            # Current gameweek is the one before the next deadline
            return max(1, event['id'] - 1)
    
    # If no future deadline found, return last gameweek
    return data['events']['data'][-1]['id']

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

def get_next_fixtures(fixtures, current_gameweek):
    """Get fixtures for the next gameweek"""
    next_gw = current_gameweek + 1
    next_fixtures = [f for f in fixtures if f['gameweek'] == next_gw]
    return next_fixtures

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

def show_group_tables(fpl_api, cup_config, current_gameweek):
    """Show current league tables for all groups"""
    print("=" * 100)
    print(f"FPL DRAFT CUP - LEAGUE TABLES (Current: GW{current_gameweek})")
    print("=" * 100)
    
    for group_name in ['A', 'B']:
        group_key = f'group_{group_name}'
        fixtures = cup_config['fixtures'][group_key]
        teams = cup_config['groups'][group_name]['teams']
        
        print(f"\n{'=' * 100}")
        print(f"GROUP {group_name}")
        print(f"{'=' * 100}")
        
        results = process_fixtures(fpl_api, fixtures, group_name, current_gameweek)
        table = calculate_league_table(results, teams)
        
        print(f"\n{'Pos':<5} {'Team':<20} {'P':<4} {'W':<4} {'D':<4} {'L':<4} {'PF':<6} {'PA':<6} {'Diff':<7} {'Pts':<5}")
        print("-" * 75)
        
        for pos, (team, stats) in enumerate(table, 1):
            print(f"{pos:<5} {team:<20} {stats['played']:<4} {stats['won']:<4} {stats['drawn']:<4} {stats['lost']:<4} "
                  f"{stats['points_for']:<6} {stats['points_against']:<6} {stats['points_diff']:<+7} {stats['match_points']:<5}")
    
    print("\n" + "=" * 100)

def show_next_fixtures(cup_config, current_gameweek):
    """Show next week's fixtures"""
    next_gw = current_gameweek + 1
    
    print("=" * 100)
    print(f"FPL DRAFT CUP - NEXT FIXTURES (GW{next_gw})")
    print("=" * 100)
    
    for group_name in ['A', 'B']:
        group_key = f'group_{group_name}'
        fixtures = cup_config['fixtures'][group_key]
        
        next_fixtures = get_next_fixtures(fixtures, current_gameweek)
        
        if next_fixtures:
            print(f"\n{'=' * 100}")
            print(f"GROUP {group_name}")
            print(f"{'=' * 100}")
            print(f"\n{'Home Team':<25} vs {'Away Team':<25}")
            print("-" * 55)
            
            for fixture in next_fixtures:
                print(f"{fixture['home']:<25} vs {fixture['away']:<25}")
        
    print("\n" + "=" * 100)

def show_results(fpl_api, cup_config, current_gameweek):
    """Show latest round and aggregate results"""
    print("=" * 100)
    print(f"FPL DRAFT CUP - MATCH RESULTS (up to GW{current_gameweek})")
    print("=" * 100)
    
    for group_name in ['A', 'B']:
        group_key = f'group_{group_name}'
        fixtures = cup_config['fixtures'][group_key]
        teams = cup_config['groups'][group_name]['teams']
        
        print(f"\n{'=' * 100}")
        print(f"GROUP {group_name}")
        print(f"{'=' * 100}")
        
        results = process_fixtures(fpl_api, fixtures, group_name, current_gameweek)
        
        # Show latest round results
        latest_round = [r for r in results if r['gameweek'] == current_gameweek]
        
        if latest_round:
            print(f"\nLATEST ROUND (GW{current_gameweek}):")
            print(f"{'Home Team':<20} {'Score':<10} {'Away Team':<20} {'Result':<8}")
            print("-" * 60)
            
            for match in latest_round:
                print(f"{match['home']:<20} {match['home_points']:<3}-{match['away_points']:<6} {match['away']:<20} {match['result']:<8}")
        
        # Show aggregate results by gameweek
        print(f"\nALL RESULTS:")
        print(f"{'GW':<5} {'Home Team':<20} {'Score':<10} {'Away Team':<20} {'Result':<8}")
        print("-" * 70)
        
        for match in results:
            print(f"GW{match['gameweek']:<3} {match['home']:<20} {match['home_points']:<3}-{match['away_points']:<6} {match['away']:<20} {match['result']:<8}")
    
    print("\n" + "=" * 100)

def main():
    # Parse command line argument
    request_type = sys.argv[1] if len(sys.argv) > 1 else 'group'
    
    # Load configuration
    config = Config()
    cup_config = load_cup_config()
    
    # Initialize FPL API
    fpl_api = FplAPI(config.fpl_domain)
    
    # Get current gameweek from gameweeks.json
    current_gameweek = get_current_gameweek()
    
    # Handle different request types
    if request_type == 'group':
        show_group_tables(fpl_api, cup_config, current_gameweek)
    elif request_type == 'fixtures':
        show_next_fixtures(cup_config, current_gameweek)
    elif request_type == 'results':
        show_results(fpl_api, cup_config, current_gameweek)
    else:
        print(f"Unknown request type: {request_type}")
        print("Usage: python test_main.py [group|fixtures|results]")
        print("  group    - Show current league tables")
        print("  fixtures - Show next week's fixtures")
        print("  results  - Show latest round and all previous results")

if __name__ == "__main__":
    main()
