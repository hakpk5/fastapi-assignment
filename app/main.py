from datetime import datetime
from pyexpat import model
import time
from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional
from .schemas import Trade
from psycopg2.extras import RealDictCursor
import psycopg2
from . import models
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session 
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True: 
  try: 
    conn = psycopg2.connect(host='localhost', database='fastapi-database', user='postgres', password='1', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connected to database")
    break
  except Exception as error:
    print("Unable to connect to the database", error)
    time.sleep(2)


@app.get('/all-trades')
def fetch_trades(db: Session = Depends(get_db)): 
  trade = db.query(models.Trades).all()
  return trade


@app.get('/trades/{id}')
def get_posts(id: str, db: Session = Depends(get_db)):
  trade = db.query(models.Trades).filter(models.Trades.trade_id == id).first()
  if not trade:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trade with id {id} not found")

  return trade

@app.get('/trades')
def search_with_query_param(search: str, db: Session = Depends(get_db)): 
  trades = db.query(models.Trades).filter(or_(  
    models.Trades.instrument_name.like(f'%{search}%'),
    models.Trades.instrument_id.like(f'%{search}%'),
    models.Trades.trader.like(f'%{search}%'),
    models.Trades.counterparty.like(f'%{search}%'),
  )).all()
  return trades


@app.get('/advance-filtering')
def advance_filtering(asset_class: Optional[str], end: Optional[datetime] , start: Optional[datetime] , minPrice: Optional[float], maxPrice: Optional[float], trade_type: Optional[str], db: Session = Depends(get_db)):
  arr = []
  if asset_class:
    arr.append(models.Trades.asset_class == asset_class)
  if end:
    arr.append(models.Trades.trade_date_time <= end)
  if start:
    arr.append(models.Trades.trade_date_time >= start)
  if minPrice:
    arr.append(models.Trades.price >= minPrice)
  if maxPrice: 
    arr.append(models.Trades.price <= maxPrice)
  if trade_type:
    arr.append(models.Trades.buySellIndicator == trade_type)
  print(arr)

  trades = db.query(models.Trades).filter(
        *arr
        ).all()
  return trades

