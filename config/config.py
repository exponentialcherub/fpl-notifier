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
        self.last_trade_file_path = data['last_trade_file_path']
        self.fpl_domain = data['fpl_domain']
        queue = data.get('queue', {})
        self.queue = QueueConfig(
            domain=queue.get('domain', ''),
            consume_subject=queue.get('consume_subject', ''),
            notify_subject=queue.get('notify_subject', ''),
            poll_interval=queue.get('poll_interval', 100)
        )

class QueueConfig:
    def __init__(self, domain: str, consume_subject: str, notify_subject: str, poll_interval: int):
        self.domain = domain
        self.consume_subject = consume_subject
        self.notify_subject = notify_subject
        self.poll_interval = poll_interval
