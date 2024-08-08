import gzip
import hashlib
import json
import os
from typing import Iterable

import pymysql
import scrapy
from scrapy import Request, Selector
from scrapy.cmdline import execute
from dmart.items import DmartProductData


def ensure_dir_exists(dir_path: str):
    # Check if directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


project_name = 'Dmart'
project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
ensure_dir_exists(dir_path=project_files_dir)


# def get_tab_value(desrciption_text):
#     selector = Selector(text=desrciption_text)
#     description_tabs = selector.xpath('//p | //h')
#     description_json = list()
#     for description_tab in description_tabs:
#         print('\n\n')
#         current_desc = description_tab.xpath('.//text()')
#         current_desc_title = current_desc[0].get()
#         print(current_desc_title)
#         current_desc_description = current_desc[1:].getall()
#         print(current_desc_description)
#         desc_dict = {current_desc_title: current_desc_description}
#         description_json.append(desc_dict)
#         print('\n\n')
#     print('description json')
#     print(description_json)
#     tab_value = description_json
#     return tab_value
def get_tab_value(desrciption_text):
    selector = Selector(text=desrciption_text)
    description_tabs = selector.xpath('//p | //h')
    description_list = list()
    for description_tab in description_tabs:
        current_desc = ' '.join(description_tab.xpath('.//text()').getall())
        description_list.append(current_desc)
    tab_value = ' '.join(description_list)
    return tab_value


def get_products_data(json_response):
    product_skus_list = json_response['props']['pageProps']['pdpData']['dynamicPDP']['data']['productData']['sKUs']
    products_data_list = list()
    for product_sku in product_skus_list:
        product_dict = dict()
        product_dict['product_name'] = product_sku["name"]
        product_dict['product_url'] = json_response["props"]["pageProps"]["refererUrl"]
        product_dict['brand'] = json_response["props"]["pageProps"]["checkProductData"]["manufacturer"] if "manufacturer" in json_response["props"]["pageProps"]["checkProductData"] else 'N/A'
        product_dict['weight'] = product_sku["variantTextValue"]
        product_dict['variant_sku_id'] = product_sku["skuUniqueID"]
        product_dict['product_mrp'] = product_sku["priceMRP"]
        product_dict['product_dmart_price'] = product_sku["priceSALE"]
        product_dict['savings'] = product_sku["savePrice"]
        product_dict['product_rate_per_weight'] = product_sku["variantInfoTxtValue"]
        product_dict['is_Veg'] = ('True' if product_sku["tags"][0] == 'veg' else 'False') if product_sku["tags"] else "N/A"
        product_dict['descriptionTabs'] = list()
        for tab in product_sku["descriptionTabs"]:
            desrciption_text = tab['description']
            tab_value = get_tab_value(desrciption_text)
            describ_tab_dict = {tab['title']: tab_value}
            product_dict['descriptionTabs'].append(describ_tab_dict)
        product_dict['descriptionTabs'] = product_dict['descriptionTabs']
        products_data_list.append(product_dict)
    return products_data_list


class ProductsSpider(scrapy.Spider):
    name = "products"

    # allowed_domains = ["abc.com"]
    # start_urls = ["https://abc.com/"]

    def __init__(self):
        super().__init__()

        # Connecting to Database
        self.client = pymysql.Connect(
            database='dmart_db',
            user='root',
            password='actowiz',
            autocommit=True,
        )
        self.cursor = self.client.cursor()

    def start_requests(self) -> Iterable[Request]:
        fetch_table = 'dmart_products_urls'
        fetch_query = f'''SELECT * FROM {fetch_table} WHERE url_status = 'Pending' and id between 1 and 6815;'''
        self.cursor.execute(query=fetch_query)
        rows = self.cursor.fetchall()
        print(f'Fetched {len(rows)} data.')

        for row in rows:
            id_ = row[0]
            url = row[2]
            print('Working on:', url)
            yield scrapy.Request(
                url=url,
                method='GET',
                callback=self.parse,
                cb_kwargs={'id': id_}
            )

    def parse(self, response, **kwargs):
        json_text = response.xpath('//script[@id = "__NEXT_DATA__"]/text()').get()
        json_response = json.loads(json_text)

        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)

        file_path = os.path.join(project_files_dir, 'Product_Pages', filename)
        ensure_dir_exists(os.path.dirname(file_path))  # Ensure the 'Product_Pages' directory exists
        with gzip.open(file_path, mode='wb') as file:
            file.write(response.body)
            print('Page Saved')

        print('Response Url:', response.url)
        product_item = DmartProductData()
        products_data_list = get_products_data(json_response)

        # for product_data in products_data_list:
        #     product_item['product_name'] = product_data["product_name"]
        #     product_item['product_url'] = product_data["product_url"]
        #     product_item['brand'] = product_data["brand"]
        #     product_item['weight'] = product_data["weight"]
        #     product_item['variant_sku_id'] = product_data["variant_sku_id"]
        #     product_item['product_mrp'] = product_data["product_mrp"]
        #     product_item['product_dmart_price'] = product_data["product_dmart_price"]
        #     product_item['savings'] = product_data["savings"]
        #     product_item['product_rate_per_weight'] = product_data["product_rate_per_weight"]
        #     product_item['is_Veg'] = product_data["is_Veg"]
        #     # print('\n\n')
        #     # print(product_data["descriptionTabs"])
        #     print('\n\n')
        #     print(product_data["descriptionTabs"])
        #     for tab in product_data["descriptionTabs"]:
        #         print('TAB:', tab)
        #         for key in tab.keys():
        #             item_key = '_'.join(key.split()).lower()
        #             try:
        #                 product_item[item_key] = tab[key]
        #             except Exception as e:
        #                 print(e)
        #                 product_item['extra_info'] = tab[key]
        #     print('Product Item:', product_item)
        #     print('\n\n\n')
        for product_data in products_data_list:
            product_item['product_name'] = product_data["product_name"]
            product_item['product_url'] = product_data["product_url"]
            product_item['brand'] = product_data["brand"]
            product_item['weight'] = product_data["weight"]
            product_item['variant_sku_id'] = product_data["variant_sku_id"]
            product_item['product_mrp'] = product_data["product_mrp"]
            product_item['product_dmart_price'] = product_data["product_dmart_price"]
            product_item['savings'] = product_data["savings"]
            product_item['product_rate_per_weight'] = product_data["product_rate_per_weight"]
            product_item['is_Veg'] = product_data["is_Veg"]
            #
            # try:
            #     for tab in json.loads(product_data["descriptionTabs"]):
            #         for key, value in tab.items():
            #             item_key = '_'.join(key.split()).lower()
            #             product_item[item_key] = value
            # except Exception as e:
            #     self.logger.error(f"Error processing tabs: {e}")
            #     product_item['extra_info'] = product_data["descriptionTabs"]
            #
            # print('Product Item:', product_item)
            # print('-' * 100)
            # yield product_item
            try:
                for tab in product_data["descriptionTabs"]:
                    for key, value in tab.items():
                        item_key = '_'.join(key.split()).lower()
                        product_item[item_key] = value
            except Exception as e:
                self.logger.error(f"Error processing tabs: {e}")
                product_item['extra_info'] = json.dumps(product_data["descriptionTabs"])
            print('Product Item:', product_item)
            print('-' * 100)
            yield product_item


if __name__ == '__main__':
    execute(f'scrapy crawl {ProductsSpider.name}'.split())
