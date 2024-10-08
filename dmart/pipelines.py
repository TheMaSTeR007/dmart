# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from dmart.items import DmartItem, DmartProductUrls, DmartProductData
from dmart.customUtils import insert_into
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DmartPipeline:
    def process_item(self, item, spider):
        if isinstance(item, DmartItem):
            copy_item = item.copy()

            data_table_name = 'dmart_cat_sub_cat_links'

            cols = ', '.join(copy_item.keys())
            values = tuple(copy_item.values())
            # placeholders = (', %s' * len(copy_item)).strip(', ')
            placeholders = ', '.join(['%s'] * len(copy_item))

            insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)
            try:
                print('Inserting Data into DB Table...')
                spider.cursor.execute(query=insert_query, args=values)
                print('Inserted Data...')
            except Exception as e:
                print(e)

        elif isinstance(item, DmartProductUrls):
            copy_item = item.copy()
            # copy_item.pop('id')

            data_table_name = 'dmart_products_urls'
            data_table_name_unique = 'dmart_products_urls_notunique'

            cols = ', '.join(copy_item.keys())
            values = tuple(copy_item.values())
            placeholders = (', %s' * len(copy_item)).strip(', ')

            insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)
            # insert_query = insert_into(table_name=data_table_name_unique, cols=cols, placeholders=placeholders)
            try:
                print('Inserting Data into DB Table...')
                spider.cursor.execute(query=insert_query, args=values)
                print('Inserted Data...')
            except Exception as e:
                print(e)
        elif isinstance(item, DmartProductData):
            copy_item = item.copy()
            # copy_item.pop('id')

            data_table_name = 'products_data'

            cols = ', '.join(copy_item.keys())
            values = tuple(copy_item.values())
            placeholders = (', %s' * len(copy_item)).strip(', ')

            insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)
            # insert_query = insert_into(table_name=data_table_name_unique, cols=cols, placeholders=placeholders)
            try:
                print('Inserting Data into DB Table...')
                print(insert_query)
                spider.cursor.execute(query=insert_query, args=values)
                print('Inserted Data...')
            except Exception as e:
                print(e)
        else:
            print('THROW...')

        return item
