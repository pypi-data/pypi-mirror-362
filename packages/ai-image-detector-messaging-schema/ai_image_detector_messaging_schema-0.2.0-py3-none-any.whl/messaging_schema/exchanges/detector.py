from faststream.rabbit import RabbitExchange, ExchangeType


detector_exchange = RabbitExchange(
    name="detector-exchange", type=ExchangeType.DIRECT, durable=True, auto_delete=False
)
