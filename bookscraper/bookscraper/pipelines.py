# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


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
