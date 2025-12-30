from api.fpl_api import FplAPI
from api.notify_api import NotifyApi
from config.config import Config
from notifiers.gameweek_notifier import GameweekNotifier
from notifiers.new_trade_notifier import NewTradeNotifier
from repo.state import State
import logging

def _run():
    config = Config()

    state = State(config.last_trade_file_path, config.notifier_state_path)

    fpl_api = FplAPI(config.fpl_domain)
    notify_api = NotifyApi(config.queue_publish_url)

    gameweeks = fpl_api.get_gameweek_details()

    gameweek_notifier = GameweekNotifier(state, gameweeks, config.notify_within_seconds, notify_api)
    new_trade_notifier = NewTradeNotifier(fpl_api, notify_api, config.league_id, state)

    gameweek_notifier.check_and_notify_waiver()
    new_trade_notifier.check_and_notify_new_trade()

def main():
    logging.basicConfig(
        filename='fpl_notifier.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logger = logging.getLogger(__name__)

    logger.info(f"Running fpl notifier")

    try:
        _run()
    except Exception as ex:
        logger.error(ex)
        return

    logger.info(f"Finished fpl notifier")

if __name__ == "__main__":
    main()