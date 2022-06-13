from confluent_kafka.avro import AvroConsumer
import json

def save_data(data, id):
    with open("consumed_data/mydata-{id}.json", "w") as final:
        json.dump(data, final)

def read_messages():
    consumer_config = {"bootstrap.servers": "kafka-bs.fractal-kafka.ovh:9092",
                       "schema.registry.url": "http://schemaregistry.fractal-kafka.ovh",
                       "group.id": "taxirides.avro.consumer.1",
                       "auto.offset.reset": "earliest"}

    consumer = AvroConsumer(consumer_config)
    consumer.subscribe(["nyc_yellow_taxi_rides"])
    data = []
    id = 0
    while(True):
        try:
            message = consumer.poll(5)
        except Exception as e:
            print(f"Exception while trying to poll messages - {e}")
        else:
            if message:
                data.append(message)
                if len(data) > 5:
                    id+=1
                    save_data(data, id=id)
                    data.clear()
                print(f"Successfully poll a record from "
                      f"Kafka topic: {message.topic()}, partition: {message.partition()}, offset: {message.offset()}\n"
                      f"message key: {message.key()} || message value: {message.value()}")
                consumer.commit()
            else:
                print("No new messages at this point. Try again later.")

    consumer.close()


if __name__ == "__main__":
    read_messages()