from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Null

from .database import Base


class AtimexOptions(Base):
    __tablename__ = "atimex_options"

    atimex_options_pk = Column(Integer, primary_key=True, index=True)
    investor_id = Column(Integer, ForeignKey("investor.investor_id"))

    deal_plus = Column(Float, index=True)
    deal_minus = Column(Float, index=True)
    waiting_time = Column(Float, index=True)
    ask_investor = Column(String)
    return_cost = Column(Boolean, default=Null)
