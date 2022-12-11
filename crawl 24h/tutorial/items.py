# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy

# class TutorialItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

from scrapy.item import Item, Field

class QuoteItem(Item):
    title = Field()
    content = Field()
    date = Field()
    url = Field()
    category = Field()
    image = Field()
