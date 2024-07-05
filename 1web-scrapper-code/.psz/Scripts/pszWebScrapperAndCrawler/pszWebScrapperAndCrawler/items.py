# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PszwebscrapperandcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    title = scrapy.Field()
    authors = scrapy.Field()
    genres =scrapy.Field()
    publisher = scrapy.Field()
    year =scrapy.Field()
    number_of_pages =scrapy.Field()
    cover_binding =scrapy.Field()
    format_height =scrapy.Field()
    format_width =scrapy.Field()
    description =scrapy.Field()
    price =scrapy.Field()