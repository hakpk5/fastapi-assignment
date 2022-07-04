from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Trades(Base):
  __tablename__ = 'trade'
  
  buySellIndicator = Column(String, nullable=False)
  price = Column (Float, nullable=False)
  quantity = Column (Integer, nullable=False)
  asset_class = Column (String, nullable=True)
  counterparty = Column (String, nullable=True) 
  instrument_id = Column(String, nullable=False)
  instrument_name = Column(String, nullable=False)
  trade_date_time = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text('now()'))

  trade_id = Column(Integer, primary_key=True, nullable=False) #if id is str, then validation is needed when operations are done in db and response needs to be sent in accordance with that.
  trader = Column (String, nullable=False)


