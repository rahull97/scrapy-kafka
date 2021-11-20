from scrapy.utils.serialize import ScrapyJSONEncoder
from kafka import KafkaProducer


class KafkaWriterPipeline(object):
    """
    Class to write the scraped and processed
    record into a Kafka topic.
    """

    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        """
        Convert the item object(dict) into
        a json string and then into bytes.
        After that write a record to a
        Kafka topic
        """
        msg = self.encoder.encode(item).encode("utf-8")
        self.producer.send(self.topic, msg)

    def close_spider(self, spider):
        self.producer.close()

    @classmethod
    def from_crawler(cls, crawler):
        """
        Access the Kafka hosts and topic
        defined in settings.py file and
        instantiate a Kafka producer instance.
        Finally instantiate KafkaWriterPipeline
        object.
        """
        settings = crawler.settings
        hosts = settings.get("SCRAPY_KAFKA_HOSTS")
        topic = settings.get("SCRAPY_KAFKA_WRITE_TOPIC")
        conn = KafkaProducer(
            bootstrap_servers=hosts,
        )
        return cls(conn, topic)
