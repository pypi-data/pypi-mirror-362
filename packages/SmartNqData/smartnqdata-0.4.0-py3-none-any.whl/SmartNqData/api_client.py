# SmartNqData/api_client.py

import requests
import pandas as pd
from datetime import datetime
import pytz
from .utils import is_valid_timeframe, format_indicator
from .enums import Timeframe, Indicator

class SmartNqClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.est = pytz.timezone('US/Eastern')

    def GetFutureData(self, contract_symbol, start_datetime, end_datetime, timeframe, indicators):
        if not all(is_valid_timeframe(indicator_timeframe, timeframe) for indicator, indicator_timeframe in indicators):
            raise ValueError("Indicator timeframe must be less granular than the main requested timeframe.")
        
        formatted_indicators = [format_indicator(indicator, indicator_timeframe, timeframe) for indicator, indicator_timeframe in indicators]
        
        payload = {
            "contractSymbol": contract_symbol,
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "timeframe": timeframe.value,
            "requestedIndicators": formatted_indicators
        }

        headers = {
            'x-api-key': self.api_key
        }

        response = requests.post(f'{self.base_url}/api/data/query', json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        
        candles = data['candles']
        formatted_data = []

        for candle in candles:
            # Convert to Eastern Time and then to naive datetime
            naive_time = datetime.fromtimestamp(candle['t'], self.est).replace(tzinfo=None)
            row = {
                'datetime': naive_time,
                'open': candle['o'],
                'high': candle['h'],
                'low': candle['l'],
                'close': candle['c'],
                'volume': candle['v']
            }
            
            # Add label fields if they exist
            for label_key in ['l5', 'l6', 'l7', 'l8', 'l9', 'l10', 'l11']:
                if label_key in candle:
                    row[label_key] = candle[label_key]
            
            # Add indicators
            row.update(candle['i'])
            formatted_data.append(row)

        df = pd.DataFrame(formatted_data)

        return df
