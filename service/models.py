from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Null, create_engine, Table, \
    MetaData, DateTime

from settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

metadata_obj = MetaData()


atimex_options = Table(
    "atimex_options",
    metadata_obj,

    Column('id', Integer, primary_key=True, index=True),
    Column('investor_pk', Integer, ForeignKey("investor.investor_pk"), nullable=False),
    Column('leader_login', String, index=True, default=Null),
    Column('leader_password', String, index=True, default=Null),
    Column('leader_server', String, index=True, default=Null),
    Column('investor_one_login', String, index=True, default=Null),
    Column('investor_one_password', String, index=True, default=Null),
    Column('investor_one_server', String, index=True, default=Null),
    Column('investment_one_size', String, index=True, default=Null),
    Column('investor_two_login', String, index=True, default=Null),
    Column('investor_two_password', String, index=True, default=Null),
    Column('investor_two_server', String, index=True, default=Null),
    Column('investment_two_size', String, index=True, default=Null),
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
)


leader = Table(
    "leader",
    metadata_obj,

    Column('leader_pk', Integer, primary_key=True, index=True),
    Column('login', String, index=True, nullable=False),
    Column('password', String, index=True, nullable=False),
    Column('server', String, index=True, nullable=False),
    Column('balance', String, index=True, nullable=False),
)


investor = Table(
    "investor",
    metadata_obj,

    Column('investor_pk', Integer, primary_key=True, index=True),
    Column('leader_pk', Integer, ForeignKey("leader.leader_pk"), nullable=False),
    Column('login', String, index=True, nullable=False),
    Column('password', String, index=True, nullable=False),
    Column('server', String, index=True, nullable=False),
    Column('balance', Float, index=True, nullable=False),
)


position = Table(
    "position",
    metadata_obj,

    Column('position_pk', Integer, primary_key=True, index=True),
    Column('leader_pk', Integer, ForeignKey("leader.leader_pk"), nullable=False),

    Column('ticket', Integer, index=True, nullable=False, unique=True),
    Column('time', DateTime, index=True, nullable=False),
    Column('type', String, index=True, nullable=False),
    Column('volume', Float, index=True, nullable=False),
    Column('sell_price', Float, index=True, nullable=False),
    Column('buy_price', Float, index=True, nullable=False),
    Column('profit', Float, index=True, nullable=False),
)
