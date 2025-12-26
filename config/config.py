import json
import os

class Config(object):
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, 'r') as f:
            data = json.load(f)
        self.league_id = data['league_id']
        self.notifier_state_path = data['notifier_state_path']
        self.gameweeks_path = data['gameweeks_path']
        self.notify_within_seconds = data['notify_within_seconds']
        self.queue_publish_url = data['queue_publish_url']
        self.last_trade_file_path = data['last_trade_file_path']
        self.fpl_domain = data['fpl_domain']