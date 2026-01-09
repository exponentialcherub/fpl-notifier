from commands.cup.cup_command import CupCommand
from formatter.cup.next_fixtures_formatter import format_next_fixtures


class NextFixturesCommand(CupCommand):
    def run(self):
        current_gameweek = self.fpl_api.get_current_gameweek()
        format_next_fixtures(self.cup_config.fixtures, current_gameweek)