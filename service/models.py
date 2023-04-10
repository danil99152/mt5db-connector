from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Null, create_engine, Table, \
    MetaData

from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

metadata_obj = MetaData()


atimex_options = Table(
    "atimex_options",
    metadata_obj,

    Column('id', Integer, primary_key=True, index=True),
    Column('investor_pk', Integer, ForeignKey("investor.investor_pk"), nullable=False),
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
    Column('no_exchange_connection', Boolean, index=True, default=Null),
    Column('api_key_expired', Boolean, index=True, default=Null),
    Column('closed_deals_myself', Boolean, index=True, default=Null),
    Column('reconnected', Boolean, index=True, default=Null),
    Column('recovery_model', Boolean, index=True, default=Null),
    Column('buy_hold_model', Boolean, index=True, default=Null),
    Column('not_enough_margin', String, index=True, default=Null),
    Column('accounts_in_diff_curr', String, index=True, default=Null),
    Column('synchronize_deals', Boolean, index=True, default=Null),
    Column('deals_not_opened', Boolean, index=True, default=Null),
    Column('closed_deal_investor', Boolean, index=True, default=Null),
    Column('access', Boolean, index=True, default=Null),
)


leader = Table(
    "leader",
    metadata_obj,

    Column('leader_pk', Integer, primary_key=True, index=True, autoincrement=False),
    Column('account_pk', Integer, ForeignKey("account.account_pk"), nullable=False),

)


investor = Table(
    "investor",
    metadata_obj,

    Column('investor_pk', Integer, primary_key=True, index=True, autoincrement=False),
    Column('leader_pk', Integer, ForeignKey("leader.leader_pk"), nullable=False),
    Column('account_pk', Integer, ForeignKey("account.account_pk"), nullable=False),
)

container = Table(
    "container",
    metadata_obj,

    Column('container_pk', Integer, primary_key=True, index=True),
    Column('account_pk', Integer, ForeignKey("account.account_pk"), nullable=False),
    Column('port', Integer, index=True, nullable=False),
)

account = Table(
    "account",
    metadata_obj,

    Column('account_pk', Integer, primary_key=True, index=True, autoincrement=False),
    Column('login', String, index=True, nullable=False),
    Column('password', String, index=True, nullable=False),
    Column('server', String, index=True, nullable=False),
    Column('balance', Float, index=True, nullable=False),
    Column('equity', Float, index=True, nullable=False),
    Column('currency', String, index=True, nullable=False),
)


position = Table(
    "position",
    metadata_obj,

    Column('position_pk', Integer, primary_key=True, index=True),
    Column('account_pk', Integer, ForeignKey("account.account_pk"), nullable=False),

    Column('ticket', Integer, index=True, nullable=False),
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
)
