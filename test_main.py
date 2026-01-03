from api.fpl_api import FplAPI
from config.config import Config

def main():
    # Load configuration
    config = Config()
    
    # Initialize FPL API
    fpl_api = FplAPI(config.fpl_domain)
    
    # Get gameweek 19 scores for all managers in the league
    gameweek = 19
    print(f"Fetching Gameweek {gameweek} scores for league {config.league_id}...\n")
    
    scores = fpl_api.get_league_gameweek_scores(config.league_id, gameweek)
    
    # Sort by points (highest first)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1].get('points', 0), reverse=True)
    
    # Print results
    print(f"{'Rank':<6} {'Manager Name':<25} {'Abbr':<6} {'GW{} Points'.format(gameweek):<15} {'Total Points':<15}")
    print("=" * 75)
    
    for rank, (entry_id, data) in enumerate(sorted_scores, 1):
        manager_name = data.get('manager_name', 'Unknown')
        abbr = data.get('abbreviation', 'N/A')
        gw_points = data.get('points', 'N/A')
        total_points = data.get('total_points', 'N/A')
        
        if 'error' in data:
            print(f"{rank:<6} {manager_name:<25} {abbr:<6} ERROR: {data['error']}")
        else:
            print(f"{rank:<6} {manager_name:<25} {abbr:<6} {gw_points:<15} {total_points:<15}")

if __name__ == "__main__":
    main()
