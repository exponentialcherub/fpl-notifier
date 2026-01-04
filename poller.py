import logging
import time

from api.fpl_api import FplAPI
from api.queue_api import QueueApi
from commands.command import Command
from commands.standings_command import StandingsCommand
from commands.standrings_command import StandringsCommand
from config.config import Config


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

    league_id = config.league_id

    fpl_api = FplAPI(config.fpl_domain)
    queue_api = QueueApi(config.queue)

    commands: dict[str, Command] = {
        "!standings": StandingsCommand(fpl_api, league_id),
        "!standrings": StandringsCommand(fpl_api, league_id),
    }

    while True:
        time.sleep(config.queue.poll_interval / 1000)

        action, reply_to = _poll_queue(queue_api)

        if action in commands:
            logger.info("Processing: " + action)
            command = commands[action]
            message = command.run()
            logger.info("Sending message to queue: " + message)

            queue_api.publish(reply_to, message)
        elif action:
            logger.info("Unsupported: " + action)

def main():
    logging.basicConfig(
        filename='fpl_poller.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    _run()

if __name__ == "__main__":
    main()