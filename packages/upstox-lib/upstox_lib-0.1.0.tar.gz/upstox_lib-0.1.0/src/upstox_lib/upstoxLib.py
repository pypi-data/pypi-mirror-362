import pandas as pd
import requests
from datetime import datetime, timedelta
def filter_instruments(
    exchange=None,
    instrument_type=None,
    option_type=None,
    strike=None,
    expiry=None,
    tradingsymbol_contains=None,
    name_contains=None,
    min_price=None,
    max_price=None
):
    """
    Filter instruments from the Upstox instrument master list.

    Parameters:
    ----------
    exchange : str or list[str], optional
        Exchange name(s), e.g., 'NSE_FO', 'BSE_EQ', 'NSE_EQ'.

    instrument_type : str or list[str], optional
        e.g., 'OPTIDX', 'OPTSTK', 'FUTIDX', 'EQUITY'.

    option_type : str or list[str], optional
        e.g., 'CE', 'PE'.

    strike : float or list[float], optional
        Exact strike price(s) to match.

    expiry : str or list[str], optional
        Expiry date(s) as 'M/D/YYYY', e.g., '6/19/2025'.

    tradingsymbol_contains : str, optional
        Substring that should be present in the trading symbol.

    name_contains : str, optional
        Substring that should be present in the name.

    min_price : float, optional
        Minimum last price.

    max_price : float, optional
        Maximum last price.

    Returns:
    --------
    pd.DataFrame
        Filtered DataFrame of matching instruments.
    """
    file_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    df = pd.read_csv(file_url)

    # Apply filters
    if exchange:
        if isinstance(exchange, str):
            exchange = [exchange]
        df = df[df['exchange'].isin(exchange)]

    if instrument_type:
        if isinstance(instrument_type, str):
            instrument_type = [instrument_type]
        df = df[df['instrument_type'].isin(instrument_type)]

    if option_type:
        if isinstance(option_type, str):
            option_type = [option_type]
        df = df[df['option_type'].isin(option_type)]

    if strike:
        if isinstance(strike, (float, int)):
            strike = [strike]
        df = df[df['strike'].isin(strike)]

    if expiry:
        if isinstance(expiry, str):
            expiry = [expiry]
        df = df[df['expiry'].isin(expiry)]

    if tradingsymbol_contains:
        df = df[df['tradingsymbol'].str.contains(tradingsymbol_contains, case=False, na=False)]

    if name_contains:
        df = df[df['name'].str.contains(name_contains, case=False, na=False)]

    if min_price is not None:
        df = df[df['last_price'] >= min_price]

    if max_price is not None:
        df = df[df['last_price'] <= max_price]

    return df.reset_index(drop=True)



def get_contractFile():
    """
    Fetch and return the Upstox instrument master list as a DataFrame.

    Source:
    -------
    https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz

    Returns:
    --------
    pd.DataFrame
        Complete instrument data from Upstox.
    """
    file_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    symboldf = pd.read_csv(file_url)
    return symboldf

def get_symbols(exchange):
    """
    Return a list of trading symbols for a given exchange from Upstox instrument master.

    Parameters:
    -----------
    exchange : str
        The exchange name (e.g., 'NSE_EQ', 'NSE_FO', 'BSE_EQ').

    Returns:
    --------
    list[str]
        List of trading symbols available on the given exchange.
    """
    file_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    df = pd.read_csv(file_url)

    filtered = df[df['exchange'] == exchange]
    return filtered['tradingsymbol'].dropna().unique().tolist()

def get_fno_contracts(prefix, instrument_type=None, exchange='NSE_FO'):
    """
    Get Futures and Options contracts by symbol prefix from Upstox instrument master.
    The prefix is extracted from the beginning of the trading symbol (e.g., 'NIFTY', 'LTF', 'RELIANCE').

    Parameters:
    -----------
    prefix : str
        Prefix of the trading symbol (e.g., 'NIFTY', 'LTF').

    instrument_type : str or list[str], optional
        Filter by instrument types like 'OPTIDX', 'FUTIDX', 'OPTSTK', 'FUTSTK'.
        If None, all F&O types are returned.

    exchange : str, optional
        Exchange to filter (default is 'NSE_FO').

    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: tradingsymbol, expiry, strike, lot_size, instrument_type, option_type
    """
    file_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    df = pd.read_csv(file_url)

    # Filter exchange and tradingsymbol prefix
    filtered = df[
        (df['exchange'] == exchange) &
        (df['tradingsymbol'].str.startswith(prefix.upper()))
    ]

    # Optional instrument type filter
    if instrument_type:
        if isinstance(instrument_type, str):
            instrument_type = [instrument_type]
        filtered = filtered[filtered['instrument_type'].isin(instrument_type)]

    return filtered[[
        'tradingsymbol',
        'expiry',
        'strike',
        'lot_size',
        'instrument_type',
        'option_type'
    ]].reset_index(drop=True)

def get_trading_day_status(date_str):
    """
    Check if the given date is a trading day, holiday, or weekend.
    
    Parameters:
    -----------
    date_str : str
        Date in 'YYYY-MM-DD' format.

    Returns:
    --------
    dict
        {
            'date': '2024-01-01',
            'is_trading_day': False,
            'reason': 'New Year Day (Trading Holiday)'
        }
    """
    url = f"https://api.upstox.com/v2/market/holidays/{date_str}"
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {
            'date': date_str,
            'is_trading_day': None,
            'reason': f"API error: {response.status_code}"
        }

    data = response.json()
    holiday_entries = data.get("data", [])

    # Check if it's explicitly marked as a holiday
    for holiday in holiday_entries:
        if holiday["date"] == date_str and holiday["holiday_type"] == "TRADING_HOLIDAY":
            closed = holiday.get("closed_exchanges", [])
            if "NSE" in closed and "BSE" in closed:
                return {
                    'date': date_str,
                    'is_trading_day': False,
                    'reason': f"{holiday['description']} (Trading Holiday)"
                }
            else:
                open_exchanges = [entry["exchange"] for entry in holiday.get("open_exchanges", [])]
                return {
                    'date': date_str,
                    'is_trading_day': True,
                    'reason': f"{holiday['description']} (Partial Trading Day on {', '.join(open_exchanges)})"
                }

    # Not listed as a trading holiday: check if weekend
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    if date_obj.weekday() in [5, 6]:  # Saturday or Sunday
        for holiday in holiday_entries:
            open_exchanges = [entry["exchange"] for entry in holiday.get("open_exchanges", [])]
            if "NSE" in open_exchanges or "BSE" in open_exchanges:
                return {
                    'date': date_str,
                    'is_trading_day': True,
                    'reason': f"Special Weekend Trading Day ({', '.join(open_exchanges)} open)"
                }
        return {
            'date': date_str,
            'is_trading_day': False,
            'reason': "Weekend (No Trading)"
        }

    # Regular weekday with no holiday info
    return {
        'date': date_str,
        'is_trading_day': True,
        'reason': "Normal Trading Day"
    }

def fetch_candle_data(symbols, end_date, start_date,interval_unit='minutes', interval_value=1):
    """
    Fetch historical candle data for given trading symbols from Upstox.

    Parameters:
    ----------
    symbols : list[str]
        List of trading symbols (e.g., ['TCS', 'HDFCBANK']).

    from_date : str
        Start date in 'YYYY-MM-DD' format.

    to_date : str
        End date in 'YYYY-MM-DD' format.

    interval_unit : str, optional
        Time unit for candle interval. Options:
            - 'minutes'
            - 'hours'
            - 'days'
            - 'weeks'
            - 'months'
        Default is 'minutes'.

    interval_value : int, optional
        Interval value based on selected unit. E.g., 1 for 1-minute, 15 for 15-minutes.
        Default is 1.

    Returns:
    -------
    pd.DataFrame
        DataFrame with columns:
        ['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        sorted by Ticker, Date, Time.

    Notes:
    ------
    🕒 Historical Availability & Limits:

    | Unit     | Interval Options    | Historical Availability      | Max Retrieval Limit               |
    |----------|---------------------|------------------------------|-----------------------------------|
    | minutes  | 1 to 300            | Available from Jan 2022      | 1 month (for 1-15 min intervals)  |
    |          |                     |                              | 1 quarter (for >15 min intervals) |
    | hours    | 1 to 5              | Available from Jan 2022      | 1 quarter                         |
    | days     | 1                   | Available from Jan 2000      | 1 decade                          |
    | weeks    | 1                   | Available from Jan 2000      | No limit                          |
    | months   | 1                   | Available from Jan 2000      | No limit                          |

    Example:
    --------
    >>> from upstox_lib.upstoxLib import fetch_candle_data
        import pandas as pd
        def test_fetch_candle_data():
        symbols = ['RELIANCE', 'TCS', 'HDFCBANK']
        start_date = '2025-06-01'
        end_date = '2025-06-19'
        unit = 'days'
        value = 1
        result = fetch_candle_data(symbols, start_date=start_date, end_date=end_date, interval_unit=unit, interval_value=value)
        result.to_csv('test_output.csv', index=False)  
        print(result.head())  

    """
    file_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    symboldf = pd.read_csv(file_url)
    symbols = [s.upper().strip() for s in symbols]

    all_data = []

    for symbol in symbols:
        match = symboldf[symboldf['tradingsymbol'] == symbol]
        if match.empty:
            print(f"❌ Symbol not found: {symbol}")
            continue

        instrument_key = match.iloc[0]['instrument_key']
        url = f'https://api.upstox.com/v3/historical-candle/{instrument_key}/{interval_unit}/{interval_value}/{end_date}/{start_date}'
        headers = {'Accept': 'application/json'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            candles = data.get("data", {}).get("candles", [])
            if not candles:
                print(f"⚠️ No candle data for: {symbol}")
                continue

            df = pd.DataFrame(candles, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI'])

            # Convert datetime and extract date and time separately
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df['Date'] = df['Datetime'].dt.strftime('%Y-%m-%d')       # e.g., 2025-06-19
            df['Time'] = df['Datetime'].dt.strftime('%H:%M:%S')       # e.g., 15:29:00

            df['Ticker'] = symbol

            # Final columns
            df = df[['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]

            all_data.append(df)
        else:
            print(f"❌ API Error for {symbol}: {response.status_code} - {response.text}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)

        # Sort by Ticker, Date, Time
        final_df = final_df.sort_values(by=['Ticker', 'Date', 'Time']).reset_index(drop=True)

        return final_df
    else:
        return pd.DataFrame(columns=['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    
def fetch_Intraday_candle_data(symbols,interval_unit='minutes', interval_value=1):
    """
    Fetch historical candle data for given trading symbols from Upstox.

    Parameters:
    ----------
    symbols : list[str]
        List of trading symbols (e.g., ['TCS', 'HDFCBANK']).

    interval_unit : str, optional
        Time unit for candle interval. Options:
            - 'minutes'
            - 'hours'
            - 'days'
        Default is 'minutes'.

    interval_value : int, optional
        Interval value based on selected unit. E.g., 1 for 1-minute, 15 for 15-minutes.
        Default is 1.

    Returns:
    -------
    pd.DataFrame
        DataFrame with columns:
        ['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        sorted by Ticker, Date, Time.

    Notes:
    ------
    🕒 Historical Availability & Limits:

    | Unit     | Interval Options    | Max Retrieval Limit          |
    |----------|---------------------|------------------------------|
    | minutes  | 1 to 300            |   Intraday                   |
    |          |                     |                              | 
    | hours    | 1 to 5              |   Intraday                   |
    | days     | 1                   |   Intraday                   |
    
    Example:
    --------
    >>> from upstox_lib.upstoxLib import fetch_candle_data
        import pandas as pd
        def test_fetch_candle_data():
        symbols = ['RELIANCE', 'TCS', 'HDFCBANK']
        start_date = '2025-06-01'
        end_date = '2025-06-19'
        unit = 'days'
        value = 1
        result = fetch_candle_data(symbols, start_date=start_date, end_date=end_date, interval_unit=unit, interval_value=value)
        result.to_csv('test_output.csv', index=False)  
        print(result.head())  

    """
    file_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    symboldf = pd.read_csv(file_url)
    symbols = [s.upper().strip() for s in symbols]

    all_data = []

    for symbol in symbols:
        match = symboldf[symboldf['tradingsymbol'] == symbol]
        if match.empty:
            print(f"❌ Symbol not found: {symbol}")
            continue

        instrument_key = match.iloc[0]['instrument_key']
        url = f'https://api.upstox.com/v3/historical-candle/intraday/{instrument_key}/{interval_unit}/{interval_value}'
        headers = {'Accept': 'application/json'}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            candles = data.get("data", {}).get("candles", [])
            if not candles:
                print(f"⚠️ No candle data for: {symbol}")
                continue

            df = pd.DataFrame(candles, columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI'])

            # Convert datetime and extract date and time separately
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df['Date'] = df['Datetime'].dt.strftime('%Y-%m-%d')       
            df['Time'] = df['Datetime'].dt.strftime('%H:%M:%S')      

            df['Ticker'] = symbol

            # Final columns
            df = df[['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]

            all_data.append(df)
        else:
            print(f"❌ API Error for {symbol}: {response.status_code} - {response.text}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)

        # Sort by Ticker, Date, Time
        final_df = final_df.sort_values(by=['Ticker', 'Date', 'Time']).reset_index(drop=True)

        return final_df
    else:
        return pd.DataFrame(columns=['Ticker', 'Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
