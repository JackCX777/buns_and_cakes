import os
import json
from dotenv import load_dotenv
from sql_adapters import PostgresAdapter
from vk_bots import VkBot
import main


load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


CATEGORIES_COLUMNS = [{'column_name': 'Category_Id', 'column_data_type': 'INT PRIMARY KEY'},
                      {'column_name': 'Category_name', 'column_data_type': 'TEXT'}]
categories_columns = ('Category_name')
categories_values = [('Buns'), ('Bread'), ('Patties'), ('Cakes')]

# CATEGORY_PRODUCTS_COLUMNS = [{'column_name': 'Product_Id', 'column_data_type': 'INT PRIMARY KEY'},
#                              {'column_name': 'Category_Id', 'column_data_type': 'INT REFERENCES Categories (Category_Id)'},
#                              {'column_name': 'Product_name', 'column_data_type': 'TEXT'}]
#

PRODUCTS_COLUMNS = [{'column_name': 'Product_Id', 'column_data_type': 'INT PRIMARY KEY'},
                    {'column_name': 'Product_name', 'column_data_type': 'TEXT'},
                    {'column_name': 'Product_label', 'column_data_type': 'TEXT'},
                    {'column_name': 'Product_owner_id', 'column_data_type': 'INT'},
                    {'column_name': 'Product_media_id', 'column_data_type': 'INT'},
                    {'column_name': 'Product_img_path', 'column_data_type': 'TEXT'},
                    {'column_name': 'Product_description', 'column_data_type': 'TEXT'},
                    {'column_name': 'Category_Id', 'column_data_type': 'INT REFERENCES Categories(Category_Id)'}]

products_columns = ('Product_name', 'Булочка с кремом', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description')

products_values = [('Product_name', 'Булочка с кремом', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Булочка в глазури', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Хлеб зерновой', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Хлебные булочки', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Хлеб деревенский', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Пирожок с мясом', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Пирожок с яблоком', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Брауни', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Кекс', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description'),
                   ('Product_name', 'Маффин', 'Product_owner_id',
                    'Product_media_id', 'Product_img_path', 'Product_description')
                   ]

db_adapter = PostgresAdapter(db_user=DB_USER,
                             db_password=DB_PASSWORD,
                             db_host=DB_HOST,
                             db_port=DB_PORT,
                             db_name=DB_NAME)


if __name__ == '__main__':
    try:
        db_adapter.connect_to_db()
        db_adapter.create_db_table(table_name='Categories', columns=CATEGORIES_COLUMNS)
        db_adapter.create_db_table(table_name='Products', columns=PRODUCTS_COLUMNS)
        for category_value in categories_values:
            db_adapter.insert_into_table(table_name='Categories', columns=categories_columns, values=category_value)

    except Exception as exception:
        print('Exception: ', exception)
