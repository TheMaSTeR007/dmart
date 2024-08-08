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

dmart_product_data_table_query = '''CREATE TABLE products_data (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    product_name VARCHAR(255),
                                    product_url VARCHAR(255),
                                    brand VARCHAR(255),
                                    weight VARCHAR(255),
                                    variant_sku_id VARCHAR(255),
                                    product_mrp VARCHAR(255),
                                    product_dmart_price VARCHAR(255),
                                    savings VARCHAR(255),
                                    product_rate_per_weight VARCHAR(255),
                                    is_Veg VARCHAR(255),
                                    description JSON,
                                    country_of_origin VARCHAR(255),
                                    disclaimer TEXT,
                                    manufacturer_info JSON,
                                    service_center JSON,
                                    extra_info JSON
                                    );'''
