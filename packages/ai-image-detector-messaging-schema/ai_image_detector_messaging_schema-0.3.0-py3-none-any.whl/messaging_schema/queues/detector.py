from faststream.rabbit import RabbitQueue, QueueType


detector_queue = RabbitQueue(
    name="detector-queue", durable=True, auto_delete=False, queue_type=QueueType.QUORUM
)
