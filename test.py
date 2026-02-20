import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.cup_config import CupConfig
from config.config import Config
from config.manager_config import ManagerConfig
from api.fpl_api import FplAPI
from commands.cup.full_fixtures_command import FullFixturesCommand

# Load configs
cup = CupConfig()
config = Config()
manager_config = ManagerConfig()
fpl_api = FplAPI(config.fpl_domain)

# Initialize command
full_fixtures_cmd = FullFixturesCommand(fpl_api, config.league_id, manager_config, cup)

print("=" * 80)
print("RUNNING get_data() - Returns raw data structure")
print("=" * 80)
data = full_fixtures_cmd.get_data()
print(f"\nCurrent Gameweek: {data['current_gameweek']}")
print(f"\nGroup A fixtures count: {len(data['fixtures_a'])}")
print("First 3 Group A fixtures:")
for f in data['fixtures_a'][:3]:
    print(f"  GW{f.gameweek}: {f.home} vs {f.away}")

print(f"\nGroup B fixtures count: {len(data['fixtures_b'])}")
print("First 3 Group B fixtures:")
for f in data['fixtures_b'][:3]:
    print(f"  GW{f.gameweek}: {f.home} vs {f.away}")

print("\n" + "=" * 80)
print("RUNNING run() - Returns formatted string for display")
print("=" * 80)
result = full_fixtures_cmd.run()
print(result)
