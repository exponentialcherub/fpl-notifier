import json
import os

class Group:
    def __init__(self, name, data):
        self.name = name
        self.teams = data.get("teams", [])
        self.matches_per_opponent = data.get("matches_per_opponent", 0)

class Schedule:
    def __init__(self, data):
        self.group_stage = data.get("group_stage", {})

class Fixture:
    def __init__(self, gameweek, home, away):
        self.gameweek = gameweek
        self.home = home
        self.away = away

class Fixtures:
    def __init__(self, data):
        self.group_A = [Fixture(**f) for f in data.get("group_A", [])]
        self.group_B = [Fixture(**f) for f in data.get("group_B", [])]

class Rules:
    def __init__(self, data):
        self.match_winner = data.get("match_winner")
        self.points_for_win = data.get("points_for_win")
        self.points_for_draw = data.get("points_for_draw")
        self.points_for_loss = data.get("points_for_loss")
        self.tiebreakers = data.get("tiebreakers", [])

class Advancement:
    def __init__(self, data):
        self.group_A_qualifiers = data.get("group_A_quAlifiers")
        self.group_B_qualifiers = data.get("group_B_quAlifiers")
        self.total_qualifiers = data.get("total_quAlifiers")
        self.description = data.get("description")
        self.seeding = data.get("seeding")

class KnockoutStage:
    def __init__(self, data):
        self.quarter_finals = data.get("quarter_finals", {})
        self.semi_finals = data.get("semi_finals", {})
        self.final = data.get("final", {})

class RelegationPlayoff:
    def __init__(self, data):
        self.gameweek = data.get("gameweek")
        self.participants = data.get("participants", [])
        self.description = data.get("description")
        self.note = data.get("note")

class CupConfig(object):
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "cup_config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, 'r') as f:
            data = json.load(f)

        self.competition_name = data.get("competition_name")
        self.format = data.get("format")
        self.scoring = data.get("scoring")

        self.groups = {k: Group(k, v) for k, v in data.get("groups", {}).items()}
        self.schedule = Schedule(data.get("schedule", {}))
        self.fixtures = Fixtures(data.get("fixtures", {}))
        self.rules = Rules(data.get("rules", {}))
        self.advancement = Advancement(data.get("advancement", {}))
        self.knockout_stage = KnockoutStage(data.get("knockout_stage", {}))
        self.relegation_playoff = RelegationPlayoff(data.get("relegation_playoff", {}))
