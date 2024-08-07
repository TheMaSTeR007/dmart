import gzip
import hashlib
import json
import os
from typing import Iterable

import pymysql
import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from dmart.items import DmartProductUrls


def ensure_dir_exists(dir_path: str):
    # Check if directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


project_name = 'Dmart'
project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
ensure_dir_exists(dir_path=project_files_dir)


def get_products_urls(json_response):
    products_urls_list = list()
    products_data_list = json_response.get('props').get('pageProps').get('plpData').get('products')
    for product in products_data_list:
        product_dict = {
            'product_name': product.get('name'),
            'product_url': 'https://www.dmart.in/product/' + product.get('seo_token_ntk')
        }
        products_urls_list.append(product_dict)
    return products_urls_list


class ProductsSpider(scrapy.Spider):
    name = "products_urls"

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
        fetch_query = '''SELECT * FROM dmart_cat_sub_cat_links WHERE url_status = 'Pending' and id between 1 and 505;'''
        self.cursor.execute(query=fetch_query)
        rows = self.cursor.fetchall()
        print(f'Fetched {len(rows)} data.')

        for row in rows:
            id_ = row[0]
            url = row[-2] if row[-2] != 'N/A' else row[-4]
            print('Working on:', url)
            yield scrapy.Request(
                url=url,
                method='GET',
                callback=self.parse,
                cb_kwargs={'id': id_}
            )

    def parse(self, response, **kwargs):
        # Receiving Response from request
        json_text = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        print(json_text)
        json_response = json.loads(json_text)

        # Saving Page
        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)
        file_path = os.path.join(project_files_dir, 'Category_Pages', filename)
        with gzip.open(filename=file_path, mode='wb') as file:
            file.write(response.body)
            print('Page Saved')

        print('Response Url:', response.url)
        products_item_data = DmartProductUrls()
        products_urls_list = get_products_urls(json_response)
        for product_data in products_urls_list:
            products_item_data['product_name'] = product_data['product_name']
            products_item_data['product_url'] = product_data['product_url']
            yield products_item_data


if __name__ == '__main__':
    execute(f'scrapy crawl {ProductsSpider.name}'.split())
