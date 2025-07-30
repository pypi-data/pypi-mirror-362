# SmartNqData/utils.py

from .enums import Timeframe

TIMEFRAME_ORDER = {
    Timeframe.MINUTE: 1,
    Timeframe.FIVE_MINUTES: 2,
    Timeframe.TEN_MINUTES: 3,
    Timeframe.FIFTEEN_MINUTES: 4,
    Timeframe.THIRTY_MINUTES: 5,
    Timeframe.HOUR: 6,
    Timeframe.FOUR_HOURS: 7,
    Timeframe.DAILY: 8,
}

def is_valid_timeframe(indicator_timeframe, main_timeframe):
    return TIMEFRAME_ORDER[indicator_timeframe] >= TIMEFRAME_ORDER[main_timeframe]

def format_indicator(indicator, indicator_timeframe, main_timeframe):
    if indicator_timeframe == main_timeframe:
        return indicator.name
    return f"{indicator_timeframe.value}{indicator.name}"
