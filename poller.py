import logging
import time

from api.fpl_api import FplAPI
from api.queue_api import QueueApi
from commands.help_command import HelpCommand
from commands.command import Command
from commands.cup.full_fixtures_command import FullFixturesCommand
from commands.cup.group_tables_command import GroupTablesCommand
from commands.cup.next_fixtures_command import NextFixturesCommand
from commands.cup.current_gw_command import CurrentGWCommand
from commands.cup.results_command import ResultsCommand
from commands.standings_command import StandingsCommand
from commands.standrings_command import StandringsCommand
from config.config import Config
from config.cup_config import CupConfig
from config.manager_config import ManagerConfig


def _poll_queue(queue_api: QueueApi):
    logger = logging.getLogger(__name__)

    message = queue_api.consume()

    if not message:
        return None, None

    action = message["action"]
    reply_to = message["reply_to"]

    if not action.startswith("!"):
        logger.warning("Unsupported: " + action)

    return action, reply_to

def _run():
    logger = logging.getLogger(__name__)

    config = Config()
    manager_config = ManagerConfig()
    cup_config = CupConfig()

    league_id = config.league_id

    fpl_api = FplAPI(config.fpl_domain)
    queue_api = QueueApi(config.queue)

    commands: dict[str, Command] = {
        "!standings": StandingsCommand(fpl_api, league_id),
        "!standrings": StandringsCommand(fpl_api, league_id),
        "!results": ResultsCommand(fpl_api, league_id, manager_config, cup_config),
        "!group": GroupTablesCommand(fpl_api, league_id, manager_config, cup_config),
        "!full-fixtures": FullFixturesCommand(fpl_api, league_id, manager_config, cup_config),
        "!fixtures": NextFixturesCommand(fpl_api, league_id, manager_config, cup_config),
        "!current-cup-fixtures": CurrentGWCommand(fpl_api, league_id, manager_config, cup_config),
        "!help": HelpCommand(),
    }

    while True:
        time.sleep(config.queue.poll_interval / 1000)

        action, reply_to = _poll_queue(queue_api)

        if action in commands:
            logger.info("Processing: " + action)
            command = commands[action]
            message = command.run()

            queue_api.publish(reply_to, message)
        elif action:
            logger.info("Unsupported: " + action)
            message = "Unsupported command.\n" + HelpCommand().run()
            queue_api.publish(reply_to, message)

def main():
    logging.basicConfig(
        handlers=[logging.FileHandler(filename="fpl_poller.log", encoding='utf-8', mode='a+')],
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    _run()

if __name__ == "__main__":
    main()