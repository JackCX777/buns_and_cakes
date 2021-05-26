import os
from dotenv import load_dotenv
import peewee


# Get secrets from environment
load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Connect to database
database = peewee.PostgresqlDatabase(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)


class BaseModel(peewee.Model):
    """
            The BaseModel class contains correct database for connect.
            Inherited from the Model class from peewee.
    """
    class Meta:
        # database for connect
        database = database


class Categories(BaseModel):
    """
            The Categories class provides work with database table categories.
            Inherited from the BaseModel class.
    """
    name = peewee.CharField()
    label = peewee.CharField()


class Products(BaseModel):
    """
            The Products class provides work with database table products.
            Inherited from the BaseModel class.
    """
    name = peewee.CharField()
    label = peewee.CharField()
    media_id = peewee.IntegerField()
    img_path = peewee.TextField()
    description = peewee.TextField()
    category = peewee.ForeignKeyField(model=Categories,
                                      related_name='products',
                                      backref='products',
                                      on_delete='CASCADE',
                                      lazy_load=False)


def create_tables():
    """
            The create_tables function provides creation of the tables in database if needed.

            Returns:
                None
    """
    with database:
        database.create_tables([Categories, Products])
        pass
