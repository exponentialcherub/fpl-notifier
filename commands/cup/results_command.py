from commands.cup.cup_command import CupCommand
from cup.results_calculator import calculate_results
from formatter.cup.results_formatter import format_results


class ResultsCommand(CupCommand):
    def run(self):
        current_gameweek = self.fpl_api.get_current_gameweek()

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
            current_gameweek
        )

        return format_results(results_a, results_b, current_gameweek)