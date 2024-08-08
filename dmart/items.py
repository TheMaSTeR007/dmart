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


class DmartProductData(scrapy.Item):
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    brand = scrapy.Field()
    weight = scrapy.Field()
    variant_sku_id = scrapy.Field()
    product_mrp = scrapy.Field()
    product_dmart_price = scrapy.Field()
    savings = scrapy.Field()
    product_rate_per_weight = scrapy.Field()
    is_Veg = scrapy.Field()
    description = scrapy.Field()
    country_of_origin = scrapy.Field()
    manufacturer_info = scrapy.Field()
    disclaimer = scrapy.Field()
    service_center = scrapy.Field()
    shelf_life = scrapy.Field()
    extra_info = scrapy.Field()

