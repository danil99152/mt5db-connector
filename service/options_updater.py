import json
import requests
from pydantic import BaseModel

from settings import settings


class Options(BaseModel):
    id: int
    investor_pk: int
    deal_in_plus: float
    deal_in_minus: float
    waiting_time: float
    ask_an_investor: str
    price_refund: bool
    multiplier: str
    multiplier_value: float
    changing_multiplier: bool
    stop_loss: str
    stop_value: float
    open_trades: str
    shutdown_initiator: str
    disconnect: bool
    open_trades_disconnect: str
    notification: bool
    blacklist: bool
    accompany_transactions: bool
    no_exchange_connection: bool
    api_key_expired: bool
    closed_deals_myself: bool
    reconnected: bool
    recovery_model: bool
    buy_hold_model: bool
    not_enough_margin: str
    accounts_in_diff_curr: str
    synchronize_deals: str
    deals_not_opened: bool
    closed_deal_investor: bool


class OptionsUpdater:
    __slots__ = []

    options = json.loads(requests.get(settings.host).text)[0]
    options.pop('leader_login', None)
    options.pop('leader_password', None)
    options.pop('leader_server', None)
    options.pop('investor_one_login', None)
    options.pop('investor_one_password', None)
    options.pop('investor_one_server', None)
    options.pop('investment_one_size', None)
    options.pop('investor_two_login', None)
    options.pop('investor_two_password', None)
    options.pop('investor_two_server', None)
    options.pop('investment_two_size', None)

    options.pop('opening_deal', None)
    options.pop('closing_deal', None)
    options.pop('target_and_stop', None)
    options.pop('signal_relevance', None)
    options.pop('profitability', None)
    options.pop('risk', None)
    options.pop('profit', None)
    options.pop('comment', None)
    options.pop('relevance', None)
    options.pop('access', None)
    options.pop('access_1', None)
    options.pop('access_2', None)
    options.pop('update_at', None)
    options.pop('created_at', None)
