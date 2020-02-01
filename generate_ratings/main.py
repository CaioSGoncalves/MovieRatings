from kafka import KafkaProducer


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['10.158.0.57:9092'], api_version=(0, 10))  # , api_version=(0, 10)
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer


if __name__ == '__main__':
    kafka_producer = connect_kafka_producer()
    publish_message(kafka_producer, 'movieRatings', "teste", "{'userId': 1, 'movieId': 296, 'rating': 5.0, 'timestamp': 1147880044}")

    if kafka_producer is not None:
        kafka_producer.close()
