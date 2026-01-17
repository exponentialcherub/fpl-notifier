import logging

from api.fpl_api import FplAPI
from commands.command import Command
from commands.cup.full_fixtures_command import FullFixturesCommand
from commands.cup.group_tables_command import GroupTablesCommand
from commands.cup.next_fixtures_command import NextFixturesCommand
from commands.cup.results_command import ResultsCommand
from commands.help_command import HelpCommand
from commands.standings_command import StandingsCommand
from commands.standrings_command import StandringsCommand
from config.cup_config import CupConfig
from config.manager_config import ManagerConfig


class CommandProcessor(object):
    def __init__(self, fpl_api: FplAPI, manager_config: ManagerConfig, cup_config: CupConfig, league_id: int):
        self.logger = logging.getLogger(__name__)

        self.fpl_api = fpl_api
        self.manager_config = manager_config
        self.cup_config = cup_config
        self.league_id = league_id

        self.commands : dict[str, Command] = {
            "!standings": StandingsCommand(fpl_api, league_id),
            "!standrings": StandringsCommand(fpl_api, league_id),
            "!results": ResultsCommand(fpl_api, league_id, manager_config, cup_config),
            "!group": GroupTablesCommand(fpl_api, league_id, manager_config, cup_config),
            "!full-fixtures": FullFixturesCommand(fpl_api, league_id, manager_config, cup_config),
            "!fixtures": NextFixturesCommand(fpl_api, league_id, manager_config, cup_config),
            "!help": HelpCommand(),
        }

    def process(self, action):
        if action in self.commands:
            self.logger.info("Processing: " + action)
            return self.commands[action].run()
        elif action:
            self.logger.info("Unsupported: " + action)
            return "Unsupported command.\n" + HelpCommand().run()
        return None
