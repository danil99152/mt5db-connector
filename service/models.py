from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Null, create_engine, Table, \
    MetaData

from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

metadata_obj = MetaData()


option = Table(
    "option",
    metadata_obj,

    Column('exchange_pk', Integer, ForeignKey("exchange.exchange_pk"), primary_key=True, index=True),
    Column('investor_pk', Integer, ForeignKey("exchange.account_pk"), index=True, nullable=False, unique=True),
    Column('leader_pk', Integer, ForeignKey("exchange.account_pk"), index=True, nullable=False, unique=True),
    Column('investment', String, index=True, default=Null),
    Column('deal_in_plus', Float, index=True, default=Null),
    Column('deal_in_minus', Float, index=True, default=Null),
    Column('waiting_time', Float, index=True, default=Null),
    Column('ask_an_investor', String, index=True, default=Null),
    Column('price_refund', Boolean, index=True, default=Null),
    Column('multiplier', String,  index=True, default=Null),
    Column('multiplier_value', Float, index=True, default=Null),
    Column('changing_multiplier', Boolean, index=True, default=Null),
    Column('stop_loss', String, index=True, default=Null),
    Column('stop_value', Float, index=True, default=Null),
    Column('open_trades', String, index=True, default=Null),
    Column('shutdown_initiator', String, index=True, default=Null),
    Column('disconnect', Boolean, index=True, default=Null),
    Column('open_trades_disconnect', String, index=True, default=Null),
    Column('notification', Boolean, index=True, default=Null),
    Column('blacklist', Boolean, index=True, default=Null),
    Column('accompany_transactions', Boolean, index=True, default=Null),
    Column('closed_deals_myself', Boolean, index=True, default=Null),
    Column('reconnected', Boolean, index=True, default=Null),
    Column('not_enough_margin', String, index=True, default=Null),
    Column('accounts_in_diff_curr', String, index=True, default=Null),
    Column('synchronize_deals', Boolean, index=True, default=Null),
    Column('deals_not_opened', Boolean, index=True, default=Null),
    Column('closed_deal_investor', Boolean, index=True, default=Null),
    Column('is_investor', Boolean, index=True, default=Null),
)


container = Table(
    "container",
    metadata_obj,

    Column('exchange_pk', Integer, ForeignKey("exchange.exchange_pk"), nullable=False, primary_key=True, index=True,
           unique=True),
    Column('name', String, index=True, nullable=False),
)

exchange = Table(
    "exchange",
    metadata_obj,

    Column('exchange_pk', Integer, primary_key=True, index=True, nullable=False, unique=True),
    Column('account_pk', Integer, index=True, nullable=False, unique=True),
    Column('login', String, index=True, nullable=False),
    Column('password', String, index=True, nullable=False),
    Column('server', String, index=True, nullable=False),
    Column('balance', Float, index=True, nullable=False),
    Column('equity', Float, index=True, nullable=False),
    Column('currency', String, index=True),
    Column('access_dcs',  Boolean, index=True, nullable=False),
    Column('investment_size', Float, index=True, nullable=False, default=0),
    Column('type', String, index=True, nullable=False),
)


position = Table(
    "position",
    metadata_obj,

    Column('ticket', Integer, primary_key=True, index=True),
    Column('exchange_pk', Integer, ForeignKey("exchange.exchange_pk"), nullable=False),

    Column('time', Integer, index=True, nullable=False),
    Column('time_update', Integer, index=True, nullable=False),
    Column('type', Integer, index=True, nullable=False),
    Column('magic', Integer, index=True, nullable=False),
    Column('volume', Float, index=True, nullable=False),
    Column('price_open', Float, index=True, nullable=False),
    Column('tp', Float, index=True, nullable=False),
    Column('sl', Float, index=True, nullable=False),
    Column('price_current', Float, index=True, nullable=False),
    Column('symbol', String, index=True, nullable=False),
    Column('comment', String, index=True, nullable=False),
    Column('price_close', Float, index=True, nullable=False),
    Column('time_close', Integer, index=True, nullable=False),
    Column('active', Boolean, index=True, nullable=False),
    Column('profit', Float, index=True, default=0),
    Column('investment_size', Float, index=True, nullable=False, default=0),
)

position_history = Table(
    "position_history",
    metadata_obj,

    Column('id', Integer, primary_key=True, index=True),
    Column('ticket', Integer, ForeignKey("position.ticket"), nullable=False),

    Column('exchange', String, index=True, nullable=False),
    Column('user_id', String, index=True, nullable=False),
    Column('api_key', String, index=True, nullable=False),
    Column('secret_key', String, index=True, nullable=False),
    Column('account', String, index=True, nullable=False),
    Column('strategy', String, index=True, nullable=False),
    Column('investment', Float, index=True, nullable=False),
    Column('multiplicator', Float, index=True, nullable=False),
    Column('stop_out', Float, index=True, nullable=False),
    Column('symbol', String, index=True, nullable=False),
    Column('type', String, index=True, nullable=False),
    Column('position', String, index=True, nullable=False),
    Column('side', String, index=True, nullable=False),
    Column('currency', String, index=True, nullable=False),
    Column('slippage_percent', Float, index=True, nullable=False),
    Column('slippage_time', Float, index=True, nullable=False),
    Column('size', Float, index=True, nullable=False),
    Column('lots', Float, index=True, nullable=False),
    Column('lever', Float, index=True, nullable=False),
    Column('balance_percent', Float, index=True, nullable=False),
    Column('volume_percent', Float, index=True, nullable=False),
    Column('open_time', Integer, index=True, nullable=False),
    Column('open_price', Float, index=True, nullable=False),
    Column('stop_loss', Float, index=True, nullable=False),
    Column('take_profit', Float, index=True, nullable=False),
    Column('close_time', Integer, index=True, nullable=False),
    Column('close_price', Float, index=True, nullable=False),
    Column('change_percent', Float, index=True, nullable=False),
    Column('gross_p_l', Float, index=True, nullable=False),
    Column('commision', Float, index=True, nullable=False),
    Column('swap', Float, index=True, nullable=False),
    Column('costs', Float, index=True, nullable=False),
    Column('net_p_l', Float, index=True, nullable=False),
    Column('roi', Float, index=True, nullable=False),
    Column('balance', Float, index=True, nullable=False),
    Column('equity', Float, index=True, nullable=False),
    Column('float_p_l', Float, index=True, nullable=False),
    Column('duration', Float, index=True, nullable=False),
    Column('minimum', Float, index=True, nullable=False),
    Column('maximum', Float, index=True, nullable=False),
    Column('risk_reward', String, index=True, nullable=False),
    Column('roi_missed', Float, index=True, nullable=False),
    Column('slip_percent', Float, index=True, nullable=False),
    Column('slip_time', Float, index=True, nullable=False),
    Column('magic', String, index=True, nullable=False),
    Column('comment', String, index=True, nullable=False),
    Column('drawdown', Float, index=True, nullable=False),
)
