# -*- coding: utf-8 -*-

from kafka import KafkaConsumer,KafkaProducer,TopicPartition
import json
import traceback


##################################################
# kafka function
##################################################

def kafka_consumer(topic, group, servers, offset):
    return KafkaConsumer(topic, group_id=group, bootstrap_servers=servers, auto_offset_reset=offset)

def kafka_consumer_no_offset_topic(group, servers):
    return KafkaConsumer(group_id=group, bootstrap_servers=servers)

def appoint_offset(csr, topic, _offset, partition):
    # 创建 TopicPartition 对象，指定要操作的 topic 和 partition
    partitions = csr.partitions_for_topic(topic)
    # 创建 TopicPartition 对象，指定要操作的 topic 和 partition
    tp = TopicPartition(topic, partition)
    # 设置消费者的偏移量
    csr.assign([tp])
    csr.seek(tp, _offset)

def kafka_producer_simplest(bootstrap_servers):
    return KafkaProducer(bootstrap_servers=bootstrap_servers)

def kafka_producer(bootstrap_servers):
    return KafkaProducer(bootstrap_servers=bootstrap_servers,key_serializer=lambda k: k.encode('utf-8') if k is not None else None,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_message(producer, topic, key, message, log):
    """
    发送消息到 Kafka 主题
    """
    try:
        producer.send(topic=topic, key=key, value=message)
    except Exception as e:
        log.error(f'Failed to send message: {e}, message:{message}')

def send_message_strongest(producer, topic, key, message, log):
    """
    发送消息到 Kafka 主题，自动处理序列化并记录错误日志。

    :param producer: Kafka producer 实例
    :param topic: Kafka topic 名称
    :param key: 消息的 key，支持 str 或 bytes
    :param message: 消息体，可以是 dict、str、int、float
    :param log: 日志记录器
    """
    try:
        if isinstance(key, str):
            key = key.encode('utf-8')
        elif not isinstance(key, (bytes, type(None))):
            key = str(key).encode('utf-8')
        if isinstance(message, (dict, list)):
            value = json.dumps(message).encode('utf-8')
        elif isinstance(message, str):
            value = message.encode('utf-8')
        elif isinstance(message, (int, float)):
            value = str(message).encode('utf-8')
        else:
            raise TypeError(f'Unsupported message type: {type(message)}')
        # 发送消息
        producer.send(topic=topic, key=key, value=value)

    except Exception as e:
        log.error(
            f"Failed to send message to topic '{topic}' with key '{key}': {e}\n"
            f"Message: {message}\n"
            f"Traceback:\n{traceback.format_exc()}"
        )


