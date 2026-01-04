from api.fpl_api import FplAPI
from api.queue_api import QueueApi
from repo.state import State
import logging

logger = logging.getLogger(__name__)

class NewTradeNotifier(object):
    def __init__(self, fpl_api: FplAPI, queue_api: QueueApi, league_id: int, state: State):
        self.fpl_api = fpl_api
        self.queue_api = queue_api
        self.league_id = league_id
        self.state = state

    def check_and_notify_new_trade(self):
        transactions = self.fpl_api.get_transactions(self.league_id)
        # Sort by most recent first
        sorted_tx = sorted(transactions, key=lambda x: x['response_time'], reverse=True)

        for tx in sorted_tx:
            trade_id = tx["id"]
            if trade_id != self.state.last_trade_id:
                teams = self.fpl_api.get_teams(self.league_id)
                players = self.fpl_api.get_players()

                # Build trade message
                offered_team = teams[tx['offered_entry']]
                received_team = teams[tx['received_entry']]
                ins = "\n".join([players[trade_item['element_in']] for trade_item in tx['tradeitem_set']])
                outs = "\n".join([players[trade_item['element_out']] for trade_item in tx['tradeitem_set']])
                message = f"🚨 New Trade Alert 🚨\n*{offered_team}*\n{ins}\n ↔️ \n*{received_team}*\n{outs}"
                logger.info(f"New trade detected, id: {trade_id}")
                self.queue_api.notify(message)
                self.state.save_last_trade_id(trade_id)
            break  # Only alert on newest trade