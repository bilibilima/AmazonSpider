# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

def remove_currency(value):
    return value.replace("$", "").strip()

def convert_value(value):
    try:
        return float(value)

    except ValueError:
        return float(value.replace(",", ""))


# classe per le info estratte
class AmazonItem(Item):
    # define the fields for your item here like:
    asin = Field()
    name = Field(input_processor = MapCompose(str.strip), output_processor = TakeFirst())
    price = Field(input_processor = MapCompose(remove_currency, convert_value), output_processor = TakeFirst())
    info = Field()
    link = Field()

    
    