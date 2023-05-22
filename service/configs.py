from pydantic import BaseModel


class Options(BaseModel):
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
    closed_deals_myself: bool
    reconnected: bool
    not_enough_margin: str
    accounts_in_diff_curr: str
    synchronize_deals: bool
    deals_not_opened: bool
    closed_deal_investor: bool


class Position(BaseModel):
    ticket: int
    exchange_pk: int
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
    profit: float
    investment_size: float


class Exchange(BaseModel):
    exchange_pk: int
    login: str
    password: str
    server: str
    balance: float
    equity: float
    currency: str
    access_dcs: bool
    investment_size: float
    type: str


class PositionHistory(BaseModel):
    ticket: int
    exchange: str
    user_id: str
    api_key: str
    secret_key: str
    account: str
    strategy: str
    investment: float
    multiplicator: float
    stop_out: float
    symbol: str
    type: str
    position: str
    side: str
    currency: str
    slippage_percent: float
    slippage_time: float
    size: float
    lots: float
    lever: float
    balance_percent: float
    volume_percent: float
    open_time: float
    open_price: float
    stop_loss: float
    take_profit: float
    close_time: int
    close_price: float
    change_percent: float
    gross_p_l: float
    commision: float
    swap: float
    costs: float
    net_p_l: float
    roi: float
    balance: float
    equity: float
    float_p_l: float
    duration: float
    minimum: float
    maximum: float
    risk_reward: float
    roi_missed: float
    slip_percent: float
    slip_time: float
    magic: str
    comment: str
    drawdown: float


class ConnectExchange(BaseModel):
    user_id: int
    login: str
    password: str
    server: str

class ConnectData(BaseModel):
    investor_id: int
    leaders_ids: list[int]
    exchanges: list[ConnectExchange]
    options: list[Options]