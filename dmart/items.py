# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DmartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_name = scrapy.Field()
    category_url = scrapy.Field()
    sub_category_name = scrapy.Field()
    sub_category_url = scrapy.Field()
    sub_subcategory_name = scrapy.Field()
    sub_subcategory_url = scrapy.Field()


class DmartProductUrls(scrapy.Item):
    product_name = scrapy.Field()
    product_url = scrapy.Field()
