from pydantic import BaseModel


class Options(BaseModel):
    id: int
    investor_pk: int
    leader_login: str
    leader_password: str
    leader_server: str
    investor_one_login: str
    investor_one_password: str
    investor_one_server: str
    investment_one_size: str
    investor_two_login: str
    investor_two_password: str
    investor_two_server: str
    investment_two_size: str
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
    synchronize_deals: bool
    deals_not_opened: bool
    closed_deal_investor: bool
    access: bool


class PostPosition(BaseModel):
    leader_pk: int
    ticket: int
    time: int
    time_update: int
    type: int
    magic: int
    volume: float
    price_open: float
    tp: float
    sl: float
    price_current: float
    symbol: str
    comment: str
    price_close: float
    time_close: int
    active: bool


class Position(PostPosition):
    position_pk: int
