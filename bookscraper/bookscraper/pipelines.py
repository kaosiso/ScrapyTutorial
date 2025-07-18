# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itertools import product
from zoneinfo import available_timezones

from MySQLdb.constants.FIELD_TYPE import DECIMAL
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 1. Strip all whitespaces from strings (except 'description')
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if isinstance(value, str):
                    adapter[field_name] = value.strip()

        # 2. Convert 'category' and 'product_type' to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if isinstance(value, str):
                adapter[lowercase_key] = value.lower()

        # 3. Convert price-related fields to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if isinstance(value, str):
                value = value.replace('€', "").strip()
                try:
                    adapter[price_key] = float(value)
                except ValueError:
                    adapter[price_key] = 0.0

        # 4. Extract number of books in stock from 'availability'
        availability_string = adapter.get('availability', '')
        if isinstance(availability_string, str):
            split_string_array = availability_string.split("(")
            if len(split_string_array) < 2:
                adapter["availability"] = 0
            else:
                availability_array = split_string_array[1].split(' ')
                try:
                    adapter["availability"] = int(availability_array[0])
                except (IndexError, ValueError):
                    adapter["availability"] = 0

        # 5. Convert 'num_reviews' from string to int
        num_reviews_string = adapter.get('num_reviews')
        try:
            adapter['num_reviews'] = int(num_reviews_string)
        except (TypeError, ValueError):
            adapter['num_reviews'] = 0

        # 6. Convert star ratings from text to integer
        stars_string = adapter.get('stars', '')
        if isinstance(stars_string, str):
            split_stars_array = stars_string.split(' ')
            if len(split_stars_array) > 1:
                stars_text_value = split_stars_array[1].lower()
                stars_dict = {
                    "zero": 0,
                    "one": 1,
                    "two": 2,
                    "three": 3,
                    "four": 4,
                    "five": 5
                }
                adapter['stars'] = stars_dict.get(stars_text_value, 0)
            else:
                adapter['stars'] = 0

        return item



import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kaosisom09',
            database='books'
        )
        self.cur = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT NOT NULL AUTO_INCREMENT,
                url VARCHAR(255),
                title TEXT,
                upc VARCHAR(255),
                product_type VARCHAR(255),
                price_excl_tax DECIMAL(10, 2),
                price_incl_tax DECIMAL(10, 2),
                tax DECIMAL(10, 2),
                availability INT,
                num_reviews INT,
                stars INT,
                category VARCHAR(255),
                description TEXT,
                PRIMARY KEY (id)
            )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (
                url,
                title,
                upc,
                product_type,
                price_excl_tax,
                price_incl_tax,
                tax,
                availability,
                num_reviews,
                stars,
                category,
                description
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, (
            item.get("url", ""),
            item.get("title", ""),
            item.get("upc", ""),
            item.get("product_type", ""),
            item.get("price_excl_tax", 0.0),
            item.get("price_incl_tax", 0.0),
            item.get("tax", 0.0),
            item.get("availability", 0),
            item.get("num_reviews", 0),
            item.get("stars", 0),
            item.get("category", ""),
            item.get("description", "")
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()