# Saleor GraphQL Loader

`saleor-gql-loader` is small python package that allows you to quickly and easily
create entities such as categories, warehouses, products on your saleor website
using the graphQL endpoint exposed by saleor.

As of now, `saleor-gql-loader` allows to create the following entities:

- [x] warehouse
- [x] shipping_zone
- [x] attribute
- [x] attribute_value
- [x] product_type
- [x] category
- [x] product
- [x] product_variant
- [x] product_image

PR for supporting more graphQL mutations and/or queries are more than welcome.

In it's current state, the project is in very early alpha, might be unstable
and no tests are provided.

_disclaimer: This project is not connected nor it has been endorsed by saleor
team/community._

## installation

using Pypi:

```bash
pip install saleor-gql-loader requests-toolbelt Django
```

Or cloning the repo:

```bash
git clone https://github.com/grll/saleor-gql-loader.git
```

## usage

### prerequisities

The first requirement is to have a running saleor installation with the latest
version installed (2.9).

Before being able to use the package to create entities you need to create a
saleor app with the necessary permissions to create the entities you need.

One way of doing that is to use the specific django cli custom command `create_app`:

```bash
python manage.py create_app etl --permission account.manage_users \
                                --permission account.manage_staff \
                                --permission app.manage_apps \
                                --permission app.manage_apps \
                                --permission discount.manage_discounts \
                                --permission plugins.manage_plugins \
                                --permission giftcard.manage_gift_card \
                                --permission menu.manage_menus \
                                --permission order.manage_orders \
                                --permission page.manage_pages \
                                --permission product.manage_products \
                                --permission shipping.manage_shipping \
                                --permission site.manage_settings \
                                --permission site.manage_translations \
                                --permission webhook.manage_webhooks \
                                --permission checkout.manage_checkouts
```

> This command will return a token. Keep it somewhere as it will be need to use the
> loader.

### loading data

`saleor-gql-loader` package exposes a single class that needs to be initialized
with the authentication token generated in the section above. Then for each entity
that you want to create there is a corresponding method on the class.

```python
from saleor_gql_loader import ETLDataLoader

# initialize the data_loader (optionally provide an endpoint url as second parameter)
data_loader = ETLDataLoader("LcLNVgUt8mu8yKJ0Wrh3nADnTT21uv")

# create a warehouse
warehouse_id = etl_data_loader.create_warehouse()
```

by default the `ETLDataLoader` will create a warehouse with sensible default values
in order to not make the query fail. You can override any parameter from the graphQL
type corresponding to the input of the underlying mutation.

For example, to set the name and email of my warehouse:

```python
# create a warehouse with specified name and email
warehouse_id = etl_data_loader.create_warehouse(name="my warehouse name", email="email@example.com")
```

When a input field is mandatory it will need to be passed as first argument for example
you can't create an attribute_value without specifying on which attribute id:

```python
# create a year attribute
year_attribute_id = etl_data_loader.create_attribute(name="year")

# add the following year value to the year attribute
possible_year_values = [2020, 2019, 2018, 2017]
for year in possible_year_values:
    etl_data_loader.create_attribute_value(year_attribute_id, name=year)
```

That's all there is to it. I added a jupyter notebook as an example with more usage [here](https://github.com/grll/saleor-gql-loader/blob/master/saleor_gql_loader/example.ipynb) where you will find a full
example that I used to populate my data.

For more details, I recommend you to check out the [code](https://github.com/grll/saleor-gql-loader/blob/master/saleor_gql_loader/data_loader.py), I tried to document it as much
as possible (it's only one module with one class).

once again for any new features additions comments, feel free to open an issue or
even better make a Pull Request.
