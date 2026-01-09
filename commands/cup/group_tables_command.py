from commands.cup.cup_command import CupCommand
from cup.league_table_calculator import calculate_league_table
from cup.results_calculator import calculate_results
from formatter.cup.group_tables_formatter import format_group_tables


class GroupTablesCommand(CupCommand):
    def run(self):
        current_gameweek = self.fpl_api.get_current_gameweek()
        teams_a = self.cup_config.groups['A'].teams
        teams_b = self.cup_config.groups['B'].teams
        results_a = calculate_results(
            self.league_id,
            self.fpl_api,
            self.cup_config.fixtures.group_A,
            self.manager_config,
            current_gameweek
        )
        results_b = calculate_results(
            self.league_id,
            self.fpl_api,
            self.cup_config.fixtures.group_B,
            self.manager_config,
            current_gameweek)
        table_a = calculate_league_table(results_a, teams_a)
        table_b = calculate_league_table(results_b, teams_b)

        return format_group_tables(table_a, table_b, current_gameweek)