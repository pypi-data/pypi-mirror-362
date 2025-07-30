# SmartNqData/enums.py

from enum import Enum, auto

class Timeframe(Enum):
    MINUTE = "Minute"
    FIVE_MINUTES = "FiveMinutes"
    TEN_MINUTES = "TenMinutes"
    FIFTEEN_MINUTES = "FifteenMinutes"
    THIRTY_MINUTES = "ThirtyMinutes"
    HOUR = "Hour"
    FOUR_HOURS = "FourHours"
    DAILY = "Daily"

class Indicator(Enum):
    ROC5 = auto()
    ROC10 = auto()
    ROC30 = auto()
    ROC60 = auto()
    ROC120 = auto()
    ROC240 = auto()
    ROCLPV5 = auto()
    ROCLPV6 = auto()
    ROCLPV7 = auto()
    ROCLPV8 = auto()
    ROCLPV9 = auto()
    ROCLPV10 = auto()
    ROCLPV11 = auto()
    EMA3 = auto()
    EMA5 = auto()
    EMA7 = auto()
    EMA14 = auto()
    EMA21 = auto()
    EMA50 = auto()
    EMA100 = auto()
    EMA200 = auto()
    RSI10 = auto()
    RSI30 = auto()
    RSI60 = auto()
    RSI120 = auto()
    RSI240 = auto()
    RSI480 = auto()
    MACD9 = auto()
    ATR7 = auto()
    ATR14 = auto()
    ATR30 = auto()
    ATR60 = auto()
    ATR120 = auto()
    ATRP7 = auto()
    ATRP14 = auto()
    ATRP30 = auto()
    ATRP60 = auto()
    ATRP120 = auto()
    ADX7 = auto()
    ADX14 = auto()
    ADX20 = auto()
    KDJ14 = auto()
