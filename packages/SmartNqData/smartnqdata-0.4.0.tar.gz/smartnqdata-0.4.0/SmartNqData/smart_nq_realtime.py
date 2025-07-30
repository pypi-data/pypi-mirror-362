import pika
import time
import json
import pandas as pd
from datetime import datetime
from .enums import Timeframe

class SmartNqRealtime:
    EXCHANGE_NAMES = {
        Timeframe.MINUTE: 'candle.minute',
        Timeframe.FIVE_MINUTES: 'candle.fiveminutes',
        Timeframe.TEN_MINUTES: 'candle.tenminutes',
        Timeframe.FIFTEEN_MINUTES: 'candle.fifteenminutes',
        Timeframe.THIRTY_MINUTES: 'candle.thirtyminutes',
        Timeframe.HOUR: 'candle.hour',
        Timeframe.FOUR_HOURS: 'candle.fourhours',
        Timeframe.DAILY: 'candle.daily'
    }

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.connection = None
        self.channel = None
        self.retry_delay = 5  # seconds

    def connect(self):
        while True:
            try:
                parameters = pika.ConnectionParameters(
                    self.url,
                    5672,
                    '/',
                    pika.PlainCredentials(self.user, self.password)
                )
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                break
            except Exception as e:
                print(f"Connection failed: {e}. Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

    def subscribe(self, contract_symbol, timeframe, queue_name, callback):
        self.connect()

        # Determine the exchange name from the timeframe
        exchange_name = self.EXCHANGE_NAMES.get(timeframe)
        if not exchange_name:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        # Declare the queue and bind it to the exchange
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)
            self.channel.queue_bind(queue=queue_name, exchange=exchange_name)
            
            # Purge the queue to remove any old messages
            self.channel.queue_purge(queue=queue_name)
        except pika.exceptions.ChannelClosedByBroker as e:
            print(f"Channel closed by broker: {e}.")
            return  # Exit or handle as appropriate

        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                if message['ContractSymbol'] == contract_symbol:
                    df = self._parse_message(message)
                    callback(df)
            except Exception as e:
                print(f"Error processing message: {e}")

        def start_consuming():
            while True:
                try:
                    self.channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
                    print(f"Subscribed to queue {queue_name} for contract symbol {contract_symbol} and timeframe {timeframe}. Waiting for messages...")
                    self.channel.start_consuming()
                except pika.exceptions.AMQPConnectionError as e:
                    print(f"Connection lost: {e}. Reconnecting...")
                    self.connect()
                except Exception as e:
                    print(f"Unexpected error: {e}. Reconnecting...")
                    self.connect()

        start_consuming()

    def _parse_message(self, message):
        # Flatten indicators
        indicators = json.loads(message['Indicators'])
        flat_indicators = {k: v for k, v in indicators.items()}

        # Map fields
        data = {
            'datetime': datetime.fromisoformat(message['Timestamp']),
            'open': message['Open'],
            'high': message['High'],
            'low': message['Low'],
            'close': message['Close'],
            'volume': message['Volume']
        }
        data.update(flat_indicators)

        # Convert to DataFrame
        df = pd.DataFrame([data])

        return df
