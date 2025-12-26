from datetime import datetime, timezone

from api.notify_api import NotifyApi
from repo.state import State
import logging

logger = logging.getLogger(__name__)

class GameweekNotifier(object):
    def __init__(self, state: State, gameweeks, notify_time, notify_api: NotifyApi):
        self.state = state
        self.gameweeks = gameweeks
        self.notify_time = notify_time
        self.notify_api = notify_api

    def check_and_notify_waiver(self):
        next_gameweek_id = self.state.last_notified_waiver_gameweek + 1

        now = datetime.now(timezone.utc)

        next_gameweek = next(
            (item for item in self.gameweeks if item['id'] == next_gameweek_id),
            None
        )

        if next_gameweek is None:
            logger.warning(f"next_gameweek not found in gameweeks. next gameweek: {next_gameweek_id}")
            return

        next_waiver_datetime = datetime.fromisoformat(next_gameweek['waivers_time'])
        diff = next_waiver_datetime - now
        if diff.total_seconds() < self.notify_time:
            message = f"Put in your waivers numnuts! Next waiver deadline is {next_waiver_datetime} - t-minus {diff.total_seconds()} seconds!"
            logger.info(f"Sending: {message}")
            self.notify_api.notify(message)
            self.state.save_waiver_gameweek(next_gameweek_id)