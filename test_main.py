import sys

from api.fpl_api import FplAPI
from config.config import Config

from config.cup_config import CupConfig
from config.manager_config import ManagerConfig
from cup.league_table_calculator import calculate_league_table
from cup.results_calculator import calculate_results
from formatter.full_fixtures_formatter import format_full_fixtures
from formatter.group_table_formatter import format_group_tables
from formatter.next_fixtures_formatter import format_next_fixtures
from formatter.results_formatter import format_results

def main():
    # Parse command line argument
    request_type = sys.argv[1] if len(sys.argv) > 1 else 'group'
    
    # Load configuration
    config = Config()
    cup_config = CupConfig()
    manager_config = ManagerConfig()
    
    # Initialize FPL API
    fpl_api = FplAPI(config.fpl_domain)

    current_gameweek = fpl_api.get_current_gameweek()
    league_id = config.league_id

    teams_a = cup_config.groups['A'].teams
    teams_b = cup_config.groups['B'].teams
    results_a = calculate_results(league_id, fpl_api, cup_config.fixtures.group_A, manager_config, current_gameweek)
    results_b = calculate_results(league_id, fpl_api, cup_config.fixtures.group_B, manager_config, current_gameweek)
    table_a = calculate_league_table(results_a, teams_a)
    table_b = calculate_league_table(results_b, teams_b)

    # Handle different request types
    if request_type == 'group':
        #show_group_tables(fpl_api, cup_config, manager_config, current_gameweek)

        print(format_group_tables(table_a, table_b, current_gameweek))
    elif request_type == 'fixtures':
        #show_next_fixtures(cup_config, current_gameweek)

        print(format_next_fixtures(cup_config.fixtures, current_gameweek))
    elif request_type == 'results':
        #show_results(fpl_api, cup_config, manager_config, current_gameweek)

        print(format_results(results_a, results_b, current_gameweek))
    elif request_type == 'all-fixtures':
        #show_full_fixtures(cup_config, current_gameweek)

        print(format_full_fixtures(cup_config.fixtures, current_gameweek))
    else:
        print(f"Unknown request type: {request_type}")
        print("Usage: python test_main.py [group|fixtures|results|all-fixtures]")
        print("  group        - Show current league tables")
        print("  fixtures     - Show next week's fixtures")
        print("  results      - Show latest round and all previous results")
        print("  all-fixtures - Show complete fixture list")

if __name__ == "__main__":
    main()
