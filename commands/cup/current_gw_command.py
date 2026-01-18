from commands.cup.cup_command import CupCommand
from formatter.cup.current_gw_formatter import current_gw_formatter


class CurrentGWCommand(CupCommand):
    def run(self):
        current_gameweek = self.fpl_api.get_current_gameweek()
        return current_gw_formatter(self.cup_config.fixtures, current_gameweek)