from itemloaders.processors import TakeFirst
from scrapy import Field, Item


def remove_tilted_quotes(iterable):
    """
    Util function to remove the tilted quote character
    from the quote text.
    input_processor requires iterable as argument and
    it may contain one or more elements, depending on
    the type of data extracted.
    :param iterable: list containing the quote text.
    :return: quote text without tilted quote.
    """
    text = iterable[0]
    return text.replace("\u201c", "").replace("\u201d", "")


class QuotesItem(Item):
    """
    Class defining the structure(fields) of each individual record.
    """

    text = Field(
        input_processor=remove_tilted_quotes, output_processor=TakeFirst()
    )
    author = Field(output_processor=TakeFirst())
    tags = Field()
