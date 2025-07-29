# https://github.com/confluentinc/confluent-kafka-python?tab=readme-ov-file#basic-consumer-example
import logging

from salt.utils import event, json, process

log = logging.getLogger(__name__)

try:
    from confluent_kafka import Consumer
except ImportError:
    log.warning("Cannot find confluent_kafka")

__virtualname__ = "kafka_consumer"
__opts__ = {}  # For linting
__salt__ = {}  # For linting


def __virtual__():
    return True


def start(broker="localhost:9094", subscribe=dict):
    log.info("Connecting to %s with %s", broker, subscribe)
    process.appendproctitle(f"broker={broker}")
    # Connect to Kafka
    c = Consumer(
        {
            "bootstrap.servers": broker,
            "group.id": __opts__["id"],
        }
    )
    c.subscribe(list(subscribe.keys()))
    # Connect to Salt Event Bus
    if __opts__.get("__role") == "master":
        fire_master = event.get_master_event(__opts__, __opts__["sock_dir"]).fire_event
    else:
        fire_master = __salt__["event.send"]

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            log.warning("Error with Kafka %s", msg.error())
        else:
            log.debug(
                "%s [%d] at offset %d with key %s",
                msg.topic(),
                msg.partition(),
                msg.offset(),
                msg.key(),
            )
            fire_master(
                data=json.loads(msg.value().decode("utf8")),
                tag=subscribe[msg.topic()],
            )
    c.close()
