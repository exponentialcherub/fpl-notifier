from commands.command import Command
from formatter.standings_formatter import format_standings


class StandringsCommand(Command):
    def run(self):
        teams = self.fpl_api.get_teams(self.league_id)
        standings = self.fpl_api.get_standings(self.league_id)
        jordy = next((x for x in standings if x["league_entry"] == 51760), None)
        standings = [{"league_entry": 51760, "rank": i, "total": jordy["total"]} for i in range(1, 11)]
        return format_standings(standings, teams)