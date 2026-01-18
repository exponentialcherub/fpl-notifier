# Quick test script for current_gw_formatter
# Run from project root: python test_current_gw.py

from api.fpl_api import FplAPI
from config.config import Config
from config.cup_config import CupConfig
from config.manager_config import ManagerConfig
from formatter.cup.current_gw_formatter import current_gw_formatter


def main():
    # Load configs
    config = Config()
    cup_config = CupConfig()
    manager_config = ManagerConfig()
    
    # Initialize API
    fpl_api = FplAPI(config.fpl_domain)
    
    # Get current gameweek
    current_gw = fpl_api.get_current_gameweek()
    print(f"Current gameweek: {current_gw}\n")
    
    # Format and print live scores
    result = current_gw_formatter(
        fixtures=cup_config.fixtures,
        current_gameweek=current_gw,
        fpl_api=fpl_api,
        league_id=config.league_id,
        manager_config=manager_config
    )
    
    print(result)


if __name__ == "__main__":
    main()
