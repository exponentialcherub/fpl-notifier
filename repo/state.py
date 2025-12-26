import os
import json

DEFAULT_WAIVER_GAMEWEEK = 18

class State(object):
    def __init__(self, last_trade_file_path, notified_log_file_path):
        self._last_trade_file_path = last_trade_file_path
        self._notified_log_file_path = notified_log_file_path
        self.last_trade_id = _load_last_trade_id(last_trade_file_path)
        self.last_notified_waiver_gameweek = _get_last_notified_waiver_gameweek(notified_log_file_path)

    def save_last_trade_id(self, trade_id):
        with open(self._last_trade_file_path, "w") as f:
            json.dump({"last_trade_id": trade_id}, f)
        self.last_trade_id = trade_id

    def save_waiver_gameweek(self, waiver_gameweek):
        with open(self._notified_log_file_path, "w") as f:
            json.dump({"waiver_gameweek": waiver_gameweek}, f)
        self.last_notified_waiver_gameweek = waiver_gameweek

def _load_last_trade_id(last_trade_file_path):
    if os.path.exists(last_trade_file_path):
        with open(last_trade_file_path, "r") as f:
            return json.load(f).get("last_trade_id")
    return None

def _get_last_notified_waiver_gameweek(notified_log_file_path):
    if os.path.exists(notified_log_file_path):
        with open(notified_log_file_path, "r") as f:
            return json.load(f).get("waiver_gameweek")
    return DEFAULT_WAIVER_GAMEWEEK