from api.fpl_api import FplAPI
from commands.FplCommand import FplCommand
from config.cup_config import CupConfig
from config.manager_config import ManagerConfig


class CupCommand(FplCommand):
    def __init__(self, fpl_api: FplAPI, league_id, manager_config: ManagerConfig, cup_config: CupConfig):
        super().__init__(fpl_api, league_id)
        self.manager_config = manager_config
        self.cup_config = cup_config

    def run(self):
        raise NotImplementedError