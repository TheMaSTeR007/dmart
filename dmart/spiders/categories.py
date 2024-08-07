import gzip
import hashlib
import json
import os
from typing import Iterable

import pymysql

from dmart.items import DmartItem
import scrapy
from scrapy import Request
from scrapy.cmdline import execute


def ensure_dir_exists(dir_path: str):
    # Check if directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f'Directory {dir_path} Created')  # Print confirmation of directory creation


project_name = 'Dmart'
project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
ensure_dir_exists(dir_path=project_files_dir)


def get_category_url(json_response):
    pass


def get_sub_category_url(json_response):
    pass


def get_category_urls(json_response):
    category_urls_list = list()
    categories_list = json_response.get('catArray')
    for category in categories_list:
        category_dict = {
            'category_name': category.get('name'),
            'category_url': 'https://www.dmart.in/category/' + category.get('seoToken')
        }
        category_urls_list.append(category_dict)
    return category_urls_list


def get_sub_category_urls(json_response, cat_index):
    sub_category_urls_list = list()
    sub_categories_list = json_response.get('catArray')[cat_index].get('subCatArray')
    for sub_category in sub_categories_list:
        sub_category_dict = {
            'sub_category_name': sub_category.get('name'),
            'sub_category_url': 'https://www.dmart.in/category/' + sub_category.get('seoToken')
        }
        sub_category_urls_list.append(sub_category_dict)
    return sub_category_urls_list


def get_sub_subcategory_urls(json_response, cat_index, sub_cat_index):
    sub_subcategory_urls_list = list()
    sub_subcategories_list = json_response.get('catArray')[cat_index].get('subCatArray')[sub_cat_index].get('subCatArray')
    if sub_subcategories_list:
        for sub_subcategory in sub_subcategories_list:
            print(sub_subcategory)
            sub_subcategory_dict = {
                'sub_subcategory_name': sub_subcategory.get('name'),
                'sub_subcategory_url': 'https://www.dmart.in/category/' + sub_subcategory.get('seoToken')
            }
            sub_subcategory_urls_list.append(sub_subcategory_dict)
        return sub_subcategory_urls_list
    else:
        sub_subcategory_dict = {
            'sub_subcategory_name': 'N/A',
            'sub_subcategory_url': 'N/A'
        }
        sub_subcategory_urls_list.append(sub_subcategory_dict)
        return sub_subcategory_urls_list


class CategoriesSpider(scrapy.Spider):
    name = "categories"

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

    # allowed_domains = ["digital.dmart.in"]

    # start_urls = ["https://digital.dmart.in/api/v1/categories/@top?profile=details&storeId=10151"]

    def start_requests(self) -> Iterable[Request]:
        urls = [
            "https://digital.dmart.in/api/v1/categories/@top?profile=details&storeId=10151"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_response = json.loads(response.body)

        filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
        print('Filename is:', filename)
        file_path = os.path.join(project_files_dir, 'Category_Urls_Page', filename)
        with gzip.open(filename=file_path, mode='wb') as file:
            file.write(response.body)
            print('Page Saved')

        categories_item_data = DmartItem()
        categories_list = get_category_urls(json_response)
        for category in categories_list:
            sub_categories_list = get_sub_category_urls(json_response, cat_index=categories_list.index(category))
            for sub_category in sub_categories_list:
                sub_subcategories_list = get_sub_subcategory_urls(json_response, cat_index=categories_list.index(category), sub_cat_index=sub_categories_list.index(sub_category))
                for sub_subcategory in sub_subcategories_list:
                    categories_item_data['category_name'] = category['category_name']
                    categories_item_data['category_url'] = category['category_url']
                    categories_item_data['sub_category_name'] = sub_category['sub_category_name']
                    categories_item_data['sub_category_url'] = sub_category['sub_category_url']
                    categories_item_data['sub_subcategory_name'] = sub_subcategory['sub_subcategory_name']
                    categories_item_data['sub_subcategory_url'] = sub_subcategory['sub_subcategory_url']
                    print('Sub Category:', categories_item_data)
                    print('-' * 100)
                    yield categories_item_data


if __name__ == '__main__':
    execute("scrapy crawl categories".split())
