# Dynamic Insert query
def insert_into(table_name, cols, placeholders):
    insert_query = f'''INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders});'''
    return insert_query


dmart_cat_sub_cat_links_table_query = '''CREATE TABLE IF NOT EXISTS `dmart_cat_sub_cat_links` (
                                            id INT PRIMARY KEY AUTO_INCREMENT,
                                            category_name VARCHAR(255),
                                            category_url VARCHAR(255),
                                            sub_category_name VARCHAR(255),
                                            sub_category_url VARCHAR(255),
                                            sub_subcategory_name VARCHAR(255),
                                            sub_subcategory_url VARCHAR(255),
                                            url_status VARCHAR(255) DEFAULT 'Pending',
                                            UNIQUE (sub_category_url, sub_subcategory_url)
                                            );'''

dmart_product_links_table_query = '''CREATE TABLE IF NOT EXISTS `dmart_products_urls` (
                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                        product_name VARCHAR(255),
                                        product_url VARCHAR(255) UNIQUE,
                                        url_status VARCHAR(255) DEFAULT 'Pending'
                                        );'''