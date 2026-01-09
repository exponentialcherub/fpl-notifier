from commands.fpl_command import FplCommand
from commands.command import Command
from formatter.standings_formatter import format_standings


class StandingsCommand(FplCommand):
    def run(self):
        teams = self.fpl_api.get_teams(self.league_id)
        standings = self.fpl_api.get_standings(self.league_id)
        return format_standings(standings, teams)