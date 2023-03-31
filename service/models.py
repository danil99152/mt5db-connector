from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Null, DateTime

from .database import Base


class AtimexOptions(Base):
    __tablename__ = "atimex_options"

    atimex_options_pk = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investor.investor_pk"), nullable=False)

    deal_plus = Column(Float, index=True, default=Null)
    deal_minus = Column(Float, index=True, default=Null)
    waiting_time = Column(Float, index=True, default=Null)
    ask_investor = Column(String, index=True, default=Null)
    return_cost = Column(Boolean, index=True, default=Null)
    multiplier = Column(String,  index=True, default=Null)
    multiplier_value = Column(Float, index=True, default=Null)
    change_multiplier = Column(Boolean, index=True, default=Null)
    stop_loss = Column(String, index=True, default=Null)
    stop_value = Column(Float, index=True, default=Null)
    open_deals = Column(String, index=True, default=Null)
    off_initiator = Column(String, index=True, default=Null)
    switch_off = Column(Boolean, index=True, default=Null)
    close_opened_deals = Column(String, index=True, default=Null)
    notification = Column(Boolean, index=True, default=Null)
    blacklist = Column(Boolean, index=True, default=Null)
    accompany_transactions = Column(Boolean, index=True, default=Null)
    exchange_connect = Column(Boolean, index=True, default=Null)
    apikey_expired = Column(Boolean, index=True, default=Null)
    closed_deals_myself = Column(Boolean, index=True, default=Null)
    reconnected = Column(Boolean, index=True, default=Null)
    recavery_model = Column(Boolean, index=True, default=Null)
    buyhold_model = Column(Boolean, index=True, default=Null)
    not_enough_margin = Column(String, index=True, default=Null)
    accounts_in_different_currencies = Column(String, index=True, default=Null)
    synchronize_deals = Column(Boolean, index=True, default=Null)
    deals_not_opened = Column(Boolean, index=True, default=Null)
    investor_closed_deals = Column(Boolean, index=True, default=Null)


class Leader(Base):
    __tablename__ = "leader"

    leader_pk = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True, nullable=False)
    password = Column(String, index=True, nullable=False)
    server = Column(String, index=True, nullable=False)
    balance = Column(String, index=True, nullable=False)


class Investor(Base):
    __tablename__ = "investor"

    investor_pk = Column(Integer, primary_key=True, index=True)
    leader_id = Column(Integer, ForeignKey("leader.leader_pk"), nullable=False)
    login = Column(String, index=True, nullable=False)
    password = Column(String, index=True, nullable=False)
    server = Column(String, index=True, nullable=False)
    balance = Column(Float, index=True, nullable=False)


class Position(Base):
    __tablename__ = "position"

    position_pk = Column(Integer, primary_key=True, index=True)
    leader_id = Column(Integer, ForeignKey("leader.leader_pk"), nullable=False)

    ticket = Column(Integer, index=True, nullable=False, unique=True)
    time = Column(DateTime, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    volume = Column(Float, index=True, nullable=False)
    sell_price = Column(Float, index=True, nullable=False)
    buy_price = Column(Float, index=True, nullable=False)
    profit = Column(Float, index=True, nullable=False)
