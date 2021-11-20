from scrapy.utils.serialize import ScrapyJSONEncoder
from kafka import KafkaProducer


class KafkaWriterPipeline(object):
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        msg = self.encoder.encode(item).encode("utf-8")
        self.producer.send(self.topic, msg)

    def close_spider(self, spider):
        self.producer.close()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        hosts = settings.get("SCRAPY_KAFKA_HOSTS")
        topic = settings.get("SCRAPY_KAFKA_WRITE_TOPIC")
        conn = KafkaProducer(
            bootstrap_servers=hosts,
        )
        return cls(conn, topic)
