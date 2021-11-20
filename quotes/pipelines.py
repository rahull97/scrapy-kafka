import json
from kafka import KafkaProducer
from itemadapter import ItemAdapter


class KafkaWriterPipeline:

    topic_name = "quotes"

    def open_spider(self, spider):
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )

    def close_spider(self, spider):
        self.producer.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        row = adapter.asdict()
        self.producer.send(self.topic_name, value=row)
