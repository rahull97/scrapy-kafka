from itemloaders.processors import TakeFirst
from scrapy import Field, Item


def remove_tilted_quotes(iterable):
    text = iterable[0]
    return text.replace("\u201c", "").replace("\u201d", "")


class QuotesItem(Item):
    text = Field(
        input_processor=remove_tilted_quotes, output_processor=TakeFirst()
    )
    author = Field(output_processor=TakeFirst())
    tags = Field()
