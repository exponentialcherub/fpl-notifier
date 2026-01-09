from commands.cup.cup_command import CupCommand
from formatter.cup.full_fixtures_formatter import format_full_fixtures


class FullFixturesCommand(CupCommand):
    def run(self):
        current_gameweek = self.fpl_api.get_current_gameweek()
        format_full_fixtures(self.cup_config.fixtures, current_gameweek)