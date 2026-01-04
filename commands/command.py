from api.fpl_api import FplAPI


class Command:
    def __init__(self, fpl_api: FplAPI, league_id):
        self.fpl_api = fpl_api
        self.league_id = league_id

    def run(self):
        raise NotImplementedError