from pydantic import BaseModel


class Options(BaseModel):
    id: int
    investor_pk: int
    investment: str
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


class Position(BaseModel):
    position_pk: int
    account_pk: int
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


class Account(BaseModel):
    account_pk: int
    login: str
    password: str
    server: str
    balance: float
    equity: float
    currency: str
    access_dcs: bool
