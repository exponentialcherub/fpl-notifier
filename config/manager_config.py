import json
import os

class Manager:
    def __init__(self, name, code, abbreviation):
        self.name = name
        self.code = code
        self.abbreviation = abbreviation

class ManagerConfig:
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(base_dir, "managers_config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Manager config file not found: {config_path}")
        with open(config_path, "r") as f:
            data = json.load(f)
        self.managers = [Manager(**m) for m in data.get("managers", [])]
        self.by_name = {m.name: m for m in self.managers}
        self.by_code = {m.code: m for m in self.managers}
        self.by_abbreviation = {m.abbreviation: m for m in self.managers}
