# import gzip
# import hashlib
# import json
# import os
# from typing import Iterable
#
# import pymysql
# import scrapy
# from scrapy import Request
# from scrapy.cmdline import execute
#
#
# def ensure_dir_exists(dir_path: str):
#     # Check if directory exists, if not, create it
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path)
#         print(f'Directory {dir_path} Created')  # Print confirmation of directory creation
#
#
# project_name = 'Dmart'
# project_files_dir = f'C:\\Project Files (using Scrapy)\\{project_name}_Project_Files'
# ensure_dir_exists(dir_path=project_files_dir)
#
#
# class ProductsSpider(scrapy.Spider):
#     name = "products"
#
#     # allowed_domains = ["abc.com"]
#     # start_urls = ["https://abc.com/"]
#
#     def __init__(self):
#         super().__init__()
#
#         # Connecting to Database
#         self.client = pymysql.Connect(
#             database='dmart_db',
#             user='root',
#             password='actowiz',
#             autocommit=True,
#         )
#         self.cursor = self.client.cursor()
#
#     def start_requests(self) -> Iterable[Request]:
#         fetch_query = '''SELECT * FROM dmart_cat_sub_cat_links WHERE url_status = 'Pending' and id between 1 and 505;'''
#         self.cursor.execute(query=fetch_query)
#         rows = self.cursor.fetchall()
#         print(f'Fetched {len(rows)} data.')
#
#         for row in rows:
#             id_ = row[0]
#             url = row[-2] if row[-2] != 'N/A' else row[-4]
#             print('Working on:', url)
#             yield scrapy.Request(
#                 url=url,
#                 method='GET',
#                 callback=self.parse,
#                 cb_kwargs={'id': id_}
#             )
#
#     def parse(self, response, **kwargs):
#         json_response = json.loads(response.body)
#
#         filename = hashlib.sha256(response.url.encode()).hexdigest() + '.html.gz'
#         print('Filename is:', filename)
#         file_path = os.path.join(project_files_dir, 'Product_Pages', filename)
#         with gzip.open(filename=file_path, mode='wb') as file:
#             file.write(json_response)
#             print('Page Saved')
#
#
# if __name__ == '__main__':
#     execute(f'scrapy crawl {ProductsSpider.name}'.split())
