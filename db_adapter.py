import os
from dotenv import load_dotenv
import peewee


load_dotenv()
DB_NAME = os.getenv('DB_NAME')

database = peewee.PostgresqlDatabase(DB_NAME)


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Categories(BaseModel):
    name = peewee.CharField()
    label = peewee.CharField()


class Products(BaseModel):
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
    with database:
        database.create_tables([Categories, Products])
        pass


# create_tables()


# category_bread = {'name': 'bread', 'label': 'Свежий хлеб'}
# category_buns = {'name': 'buns', 'label': 'Сладкие булочки'}
# category_cakes = {'name': 'cakes', 'label': 'Чудесные кексы'}
# category_patties = {'name': 'patties', 'label': 'Горячие пирожки'}

# category_bread_row = Categories.create(**category_bread)
# print(category_bread_row.name)
# category_buns_row = Categories.create(**category_buns)
# print(category_bread_row.name)
# category_cakes_row = Categories.create(**category_cakes)
# print(category_bread_row.name)
# category_patties_row = Categories.create(**category_patties)
# print(category_bread_row.name)

# categories = [{'name': 'bread', 'label': 'Свежий хлеб'},
#               {'name': 'buns', 'label': 'Сладкие булочки'},
#               {'name': 'cakes', 'label': 'Чудесные кексы'},
#               {'name': 'patties', 'label': 'Горячие пирожки'}
#               ]
#
# for category in categories:
#     category_row = Categories.create(**category)
#     print(category_row.name)


# bread_category = Categories.get(Categories.name == 'bread')
# buns_category = Categories.get(Categories.name == 'buns')
# cakes_category = Categories.get(Categories.name == 'cakes')
# patties_category = Categories.get(Categories.name == 'patties')


# product_bread_rolls = {'name': 'bread_rolls', 'label': 'Хлебные булочки', 'media_id': 457239064,
#                        'img_path': 'imgs/Bread/bread_rolls.jpg', 'description': 'description',
#                        'category': bread_category}
# product_grain_bread = {'name': 'grain_bread', 'label': 'Хлеб зерновой', 'media_id': 457239065,
#                        'img_path': 'imgs/Bread/grain_bread.jpg', 'description': 'description',
#                        'category': bread_category}
# product_rustic_bread = {'name': 'rustic_bread', 'label': 'Хлеб деревенский', 'media_id': 457239066,
#                         'img_path': 'imgs/Bread/rustic_bread.jpg', 'description': 'description',
#                         'category': bread_category}
# product_cream_bun = {'name': 'cream_bun', 'label': 'Булочка с кремом', 'media_id': 457239067,
#                      'img_path': 'imgs/Buns/cream_bun.jpg', 'description': 'description',
#                      'category': buns_category}
# product_frosted_bun = {'name': 'frosted_bun', 'label': 'Булочка в глазури', 'media_id': 457239068,
#                        'img_path': 'imgs/Buns/frosted_bun.jpg', 'description': 'description',
#                        'category': buns_category}
# product_brownies = {'name': 'brownies', 'label': 'Брауни', 'media_id': 457239069,
#                     'img_path': 'imgs/Cakes/brownies.jpg', 'description': 'description',
#                     'category': cakes_category}
# product_chocolate_muffin = {'name': 'chocolate_muffin', 'label': 'Шоколадный маффин', 'media_id': 457239070,
#                             'img_path': 'imgs/Cakes/chocolate_muffin.jpg', 'description': 'description',
#                             'category': cakes_category}
# product_cupcake = {'name': 'cupcake', 'label': 'Кекс', 'media_id': 457239071,
#                    'img_path': 'imgs/Cakes/cupcake.jpg', 'description': 'description',
#                    'category': cakes_category}
# product_apple_patty = {'name': 'apple_patty', 'label': 'Пирожок с яблоком', 'media_id': 457239072,
#                        'img_path': 'imgs/Patties/apple_patty.jpg', 'description': 'description',
#                        'category': patties_category}
# product_meat_patty = {'name': 'meat_patty', 'label': 'Пирожок с мясом', 'media_id': 457239073,
#                       'img_path': 'imgs/Patties/meat_patty.jpg', 'description': 'description',
#                       'category': patties_category}
#
#
# product_row = Products.create(**product_meat_patty)
# print(product_row.name)

