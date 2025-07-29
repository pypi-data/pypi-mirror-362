"""
Kafka Admin modules for Salt

For most of these modules, we want to lightly wrap the underlying AdminClient
modules in a form that Salt can use. This usually means taking a dictionary and
changing it to the correct request classes. Most of the AdminClient modules use
plurals for the topics they request, so we match that here, even though most
state calls will only call on a single value, resulting in a call similar to

>>> some_method(name)[name]

Requires setting `kafka.bootstrap.servers` in Minion config.
"""

import datetime
import logging
import re

log = logging.getLogger(__name__)

try:
    from confluent_kafka.admin import (
        AdminClient,
        AlterConfigOpType,
        ConfigEntry,
        ConfigResource,
        NewTopic,
        ResourceType,
    )
except ImportError:
    log.warning("Cannot find confluent_kafka")
    HAS_KAFKA = False
else:
    HAS_KAFKA = True

__virtualname__ = "kafka"
__context__ = {}
__salt__ = {}


def __virtual__():
    if not HAS_KAFKA:
        return (
            False,
            "Could not import kafka returner; confluent-kafka is not installed.",
        )
    return __virtualname__


def _config(key):
    if key not in __context__:
        __context__[key] = __salt__["config.option"](f"kafka.{key}")
    return __context__[key]


def _client():
    if "_client" not in __context__:
        __context__["_client"] = AdminClient(
            {
                "bootstrap.servers": _config("bootstrap.servers"),
            }
        )
    return __context__["_client"]


TIMEDELTA_VARS = {
    "weeks": "w",
    "days": "d",
    "hours": "h",
    "minutes": "m",
    "seconds": "s",
    "milliseconds": "ms",
    "microseconds": "us",
}
TIMEDELTA_RE = re.compile(
    "".join([rf"((?P<{k}>\d+?){TIMEDELTA_VARS[k]})?" for k in TIMEDELTA_VARS])
)


def timedelta_ms(value: str) -> int:
    """
    Parse a timedelta into milliseconds as used by Kafka
    """
    parsed = TIMEDELTA_RE.match(value).groupdict()
    parts = {p: int(parsed[p]) for p in parsed if parsed[p] is not None}
    td = datetime.timedelta(**parts)
    return int(td.total_seconds() * 1000)


def list_topics():
    response = _client().list_topics(timeout=10)
    return list(response.topics)


def create_topics(
    *names: list[str], num_partitions=-1, replication_factor=-1, config=None
) -> dict[str, bool]:
    # See https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.admin.NewTopic
    request = [
        NewTopic(name, num_partitions, replication_factor, config=config)
        for name in names
    ]

    response = _client().create_topics(request)
    changes = {topic: response[topic].result() is None for topic in response}
    log.info("create_topic %s", changes)
    return changes


def delete_topics(*names: list[str]) -> dict[str, bool]:
    response = _client().delete_topics(list(names))
    changes = {topic: response[topic].result() is None for topic in response}
    log.info("delete_topics %s", response)
    return changes


def describe_topics(*names: list) -> dict:
    request = [ConfigResource(ResourceType.TOPIC, name) for name in names]
    # log.info("describe_topics %s", request)
    response = _client().describe_configs(request)
    changes = {}

    for topic in response:
        changes[topic.name] = {}
        for config in response[topic].result().values():
            changes[topic.name][config.name] = config.value

    return changes


def update_topic(name, config: dict):
    new_config = [
        ConfigEntry(
            name=key,
            value=str(config[key]),
            incremental_operation=AlterConfigOpType.SET,
        )
        for key in config
    ]
    request = [ConfigResource(ResourceType.TOPIC, name, incremental_configs=new_config)]

    response = _client().incremental_alter_configs(request)
    for cr in response:
        if response[cr].result() is None:
            return {ce.name: ce.value for ce in cr.incremental_configs}
