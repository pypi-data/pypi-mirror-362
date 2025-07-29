__virtualname__ = "kafka"
__salt__ = {}
__opts__ = {}


def __virtual__():
    if "kafka.list_topics" in __salt__:
        return True
    return (False, "kafka module could not be loaded")


def present(name, config: dict = None, num_partitions=-1, replication_factor=-1):
    """
    Ensure that a topic exists in Kafka

    num_partitions and replication_factor default to -1 which lets the
    cluster determine the default values

    config is a dictionary of extra config options for the topic.
    See https://kafka.apache.org/documentation.html#topicconfigs for config values.
    """
    ret = {"name": name, "result": True, "comment": "", "changes": {}}

    if config is None:
        config = {}
    # The underlying Kafka client considers all config values as strings, so we
    # cast everything as string here to make things easier
    for key in config:
        config[key] = str(config[key])

    # Check if we need to create a new topic
    if name not in __salt__["kafka.list_topics"]():
        if __opts__["test"]:
            ret["comment"] = f"Topic {name} to be created"
            ret["changes"]["to-create"] = name
            if config:
                ret["changes"]["config"] = config
            ret["result"] = None
            return ret
        elif __salt__["kafka.create_topics"](
            name,
            config=config,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )[name]:
            ret["changes"]["created"] = name
            if config:
                ret["changes"]["config"] = config
            ret["comment"] = f"Created topic {name}"
            return ret
        else:
            ret["comment"] = f"Topic {name} error"
            ret["result"] = False
            return ret

    # Check if we need to update the config
    existing_config = __salt__["kafka.describe_topics"](name)[name]

    updated_config = {
        key: config[key] for key in config if config[key] != existing_config.get(key)
    }

    if updated_config:
        if __opts__["test"]:
            ret["result"] = None
            ret["comment"] = "Will update config"
            ret["changes"] = {
                key: f"Will change {existing_config.get(key)} to {updated_config[key]}"
                for key in updated_config
            }
        else:
            changed_config = __salt__["kafka.update_topic"](name, updated_config)
            ret["changes"] = {
                key: f"Changed {existing_config.get(key)} to {changed_config[key]}"
                for key in changed_config
            }
            ret["comment"] = "Config updated"
    else:
        ret["comment"] = "No config update needed"

    return ret


def absent(name):
    """
    Ensure the named topic is absent
    """
    ret = {"name": name, "result": True, "comment": "", "changes": {}}
    topics = __salt__["kafka.list_topics"]()
    if name not in topics:
        ret["comment"] = f"Topic {name} is not present"
        return ret

    if __opts__["test"]:
        ret["comment"] = f"Topic {name} is set for removal"
        ret["result"] = None
    elif __salt__["kafka.delete_topics"](name)[name]:
        ret["changes"][name] = "Deleted"
        ret["comment"] = f"Removed topic {name}"
    else:
        ret["comment"] = f"Topic {name} error"
        ret["result"] = False
    return ret
