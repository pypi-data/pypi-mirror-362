from upstox_lib.upstoxLib import fetch_candle_data,fetch_Intraday_candle_data
from upstox_lib.upstoxLib import get_symbols,get_contractFile,get_fno_contracts
from upstox_lib.upstoxLib import get_trading_day_status
from datetime import datetime
import pandas as pd

def test_fetch_candle_data():
    symbols = ['RELIANCE', 'TCS', 'HDFCBANK']
    start_date = '2025-06-01'
    end_date = '2025-06-19'
    unit = 'days'
    value = 1
    result = fetch_candle_data(symbols, start_date=start_date, end_date=end_date, interval_unit=unit, interval_value=value)
    assert isinstance(result, pd.DataFrame), "Result should be a Pandas DataFrame"
    assert not result.empty, "Result DataFrame should not be empty"
    result.to_csv('test_output.csv', index=False)  
    print(result.head())  

def test_instr():
    df = get_contractFile()
    print(df.head())
    
def test_symbols():
    exchange = 'NSE_FO'
    symbols = get_symbols(exchange)
    print(symbols[:5])  

def test_fno_contracts():
    contracts = get_fno_contracts("TCS",'FUTSTK')
    print(contracts.head())  
    contracts.to_csv('fno_contracts.csv', index=False)  


def test_cashData():
    start_date = '2025-06-19'
    end_date = '2025-06-19'
    ticker = get_symbols('NSE_EQ')
    unit = 'minutes'
    value = 1
    data = fetch_candle_data(symbols=ticker, start_date=start_date, end_date=end_date, interval_unit=unit, interval_value=value)
    data.to_csv('cash_data.csv', index=False)


def test_intraday_data():
    symbol = ['RELIANCE', 'TCS', 'HDFCBANK']
    unit = 'minutes'
    value = 1
    data = fetch_Intraday_candle_data(symbols=symbol, interval_unit=unit, interval_value=value)
    assert isinstance(data, pd.DataFrame)
    assert not data.empty
    data.to_csv('intraday_data.csv', index=False)

def test_check_trading_day():
    date = '2025-02-02'
    result = get_trading_day_status(date)
    print(f"Is {date} a trading day? {result}") 