"""Implements a data loader that load data into Saleor through graphQL.

Notes
-----
This module is designed and working with Saleor 2.9. Update will be necessary
for futur release if the data models changes.

No tests has been implemented as testing would need to create a fake db, which
requires a lot of dev better redo the project as a django app inside saleor
project for easier testing.

"""
from .utils import graphql_request, graphql_multipart_request, override_dict, handle_errors, get_payload


class ETLDataLoader:
    """abstraction around several graphQL query to load data into Saleor.

    Notes
    -----
    This class requires a valid `auth_token` to be provided during
    initialization. An `app` must be first created for example using django cli

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

    Attributes
    ----------
    headers : dict
        the headers used to make graphQL queries.
    endpoint_url : str
        the graphQL endpoint url to query to.

    Methods
    -------

    """

    def __init__(self, auth_token, endpoint_url="http://localhost:8000/graphql/"):
        """initialize the `DataLoader` with an auth_token and an url endpoint.

        Parameters
        ----------
        auth_token : str
            token used to identify called to the graphQL endpoint.
        endpoint_url : str, optional
            the graphQL endpoint to be used , by default "http://localhost:8000/graphql/"
        """
        self.headers = {"Authorization": "Bearer {}".format(auth_token)}
        self.endpoint_url = endpoint_url

    def update_shop_settings(self, **kwargs):
        """update shop settings.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to update the shop settings refer to the
            ShopSettingsInput graphQL type to know what can be overriden.

        Raises
        ------
        Exception
            when shopErrors is not an empty list
        """

        variables = {
            "input": kwargs
        }

        query = """
            mutation ShopSettingsUpdate($input: ShopSettingsInput!) {
              shopSettingsUpdate(input: $input) {
                shop {
                    headerText
                    description
                    includeTaxesInPrices
                    displayGrossPrices
                    chargeTaxesOnShipping
                    trackInventoryByDefault
                    defaultWeightUnit
                    automaticFulfillmentDigitalProducts
                    defaultDigitalMaxDownloads
                    defaultDigitalUrlValidDays
                    defaultMailSenderName
                    defaultMailSenderAddress
                    customerSetPasswordUrl
                }
                shopErrors {
                    field
                    message
                    code
                }
              }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["shopSettingsUpdate"]["shopErrors"]
        handle_errors(errors)

        return response["data"]["shopSettingsUpdate"]["shop"]

    def update_shop_domain(self, **kwargs):
        """update shop domain.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to update the shop domain refer to the
            SiteDomainInput graphQL type to know what can be overriden.

        Raises
        ------
        Exception
            when shopErrors is not an empty list
        """

        variables = {
            "siteDomainInput": kwargs
        }

        query = """
            mutation ShopDomainUpdate($siteDomainInput: SiteDomainInput!) {
              shopDomainUpdate(input: $siteDomainInput) {
                shop {
                    domain {
                        host
                        sslEnabled
                        url
                    }
                }
                shopErrors {
                    field
                    message
                    code
                }
              }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["shopDomainUpdate"]["shopErrors"]
        handle_errors(errors)

        return response["data"]["shopSettingsUpdate"]["shop"]["domain"]

    def update_shop_address(self, **kwargs):
        """update shop address.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to update the shop address refer to the
            AddressInput graphQL type to know what can be overriden.

        Raises
        ------
        Exception
            when shopErrors is not an empty list
        """

        variables = {
            "addressInput": kwargs
        }

        query = """
            mutation ShopAddressUpdate($addressInput: AddressInput!) {
              shopAddressUpdate(input: $addressInput) {
                shop {
                    companyAddress {
                        id
                        firstName
                        lastName
                        companyName
                        streetAddress1
                        streetAddress2
                        city
                        cityArea
                        postalCode
                        country {
                            code
                            country
                        }
                        countryArea
                        phone
                        isDefaultShippingAddress
                        isDefaultBillingAddress
                    }
                }
                shopErrors {
                    field
                    message
                    code
                }
              }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["shopAddressUpdate"]["shopErrors"]
        handle_errors(errors)

        return response["data"]["shopAddressUpdate"]["shop"]["companyAddress"]

    def create_warehouse(self, **kwargs):
        """create a warehouse.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to create the warehouse refer to the
            WarehouseCreateInput graphQL type to know what can be overriden.

        Returns
        -------
        id : str
            the id of the warehouse created

        Raises
        ------
        Exception
            when warehouseErrors is not an empty list
        """
        default_kwargs = {
            "companyName": "The Fake Company",
            "email": "fake@example.com",
            "name": "fake warehouse",
            "address": {
                "streetAddress1": "a fake street adress",
                "city": "Fake City",
                "postalCode": "1024",
                "country": "CH"
            }
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createWarehouse($input: WarehouseCreateInput!) {
                createWarehouse(input: $input) {
                    warehouse {
                        id
                    }
                    warehouseErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["createWarehouse"]["warehouseErrors"]
        handle_errors(errors)

        return response["data"]["createWarehouse"]["warehouse"]["id"]

    def create_shipping_zone(self, **kwargs):
        """create a shippingZone.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to create the shippingzone refer to
            the shippingZoneCreateInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the shippingZone created.

        Raises
        ------
        Exception
            when shippingErrors is not an empty list.
        """
        default_kwargs = {
            "name": "CH",
            "countries": [
                "CH"
            ],
            "default": False,
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createShippingZone($input: ShippingZoneCreateInput!) {
                shippingZoneCreate(input: $input) {
                    shippingZone {
                        id
                    }
                    shippingErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["shippingZoneCreate"]["shippingErrors"]
        handle_errors(errors)

        return response["data"]["shippingZoneCreate"]["shippingZone"]["id"]

    def create_attribute(self, **kwargs):
        """create a product attribute.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to create the attribute refer to
            the AttributeCreateInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the attribute created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        default_kwargs = {
            "inputType": "DROPDOWN",
            "name": "default"
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createAttribute($input: AttributeCreateInput!) {
                attributeCreate(input: $input) {
                    attribute {
                        id
                    }
                    productErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["attributeCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["attributeCreate"]["attribute"]["id"]

    def create_attribute_value(self, attribute_id, **kwargs):
        """create a product attribute value.

        Parameters
        ----------
        attribute_id : str
            id of the attribute on which to add the value.
        **kwargs : dict, optional
            overrides the default value set to create the attribute refer to
            the AttributeValueCreateInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the attribute on which the value was created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        default_kwargs = {
            "name": "default"
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "attribute": attribute_id,
            "input": default_kwargs
        }

        query = """
            mutation createAttributeValue($input: AttributeValueCreateInput!, $attribute: ID!) {
                attributeValueCreate(input: $input, attribute: $attribute) {
                    attribute{
                        id
                    }
                    productErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["attributeValueCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["attributeValueCreate"]["attribute"]["id"]

    def create_product_type(self, **kwargs):
        """create a product type.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to create the type refer to
            the ProductTypeInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the productType created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        default_kwargs = {
            "name": "default",
            "hasVariants": False,
            "productAttributes": [],
            "variantAttributes": [],
            "isDigital": "false",
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createProductType($input: ProductTypeInput!) {
                productTypeCreate(input: $input) {
                    productType {
                        id
                    }
                    productErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["productTypeCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["productTypeCreate"]["productType"]["id"]

    def create_category(self, **kwargs):
        """create a category.

        Parameters
        ----------
        **kwargs : dict, optional
            overrides the default value set to create the category refer to
            the productTypeCreateInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the productType created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        default_kwargs = {
            "name": "default"
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createCategory($input: CategoryInput!) {
                categoryCreate(input: $input) {
                    category {
                        id
                    }
                    productErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["categoryCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["categoryCreate"]["category"]["id"]

    def create_product(self, product_type_id, **kwargs):
        """create a product.

        Parameters
        ----------
        product_type_id : str
            product type id required to create the product.
        **kwargs : dict, optional
            overrides the default value set to create the product refer to
            the ProductCreateInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the product created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        default_kwargs = {
            "name": "default",
            "description": "default",
            "productType": product_type_id,
            "basePrice": 0.0,
            "sku": "default"
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createProduct($input: ProductCreateInput!) {
                productCreate(input: $input) {
                    product {
                        id
                    }
                    productErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["productCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["productCreate"]["product"]["id"]

    def create_product_variant(self, product_id, **kwargs):
        """create a product variant.

        Parameters
        ----------
        product_id : str
            id for which the product variant will be created.
        **kwargs : dict, optional
            overrides the default value set to create the product variant refer
            to the ProductVariantCreateInput graphQL type to know what can be
            overriden.

        Returns
        -------
        id : str
            the id of the product variant created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        default_kwargs = {
            "product": product_id,
            "sku": "0",
            "attributes": []
        }

        override_dict(default_kwargs, kwargs)

        variables = {
            "input": default_kwargs
        }

        query = """
            mutation createProductVariant($input: ProductVariantCreateInput!) {
                productVariantCreate(input: $input) {
                    productVariant {
                        id
                    }
                    productErrors {
                        field
                        message
                        code
                    }
                }
            }
        """

        response = graphql_request(
            query, variables, self.headers, self.endpoint_url)

        errors = response["data"]["productVariantCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["productVariantCreate"]["productVariant"]["id"]

    def create_product_image(self, product_id, file_path):
        """create a product image.

        Parameters
        ----------
        product_id : str
            id for which the product image will be created.
        file_path : str
            path to the image to upload.

        Returns
        -------
        id : str
            the id of the product image created.

        Raises
        ------
        Exception
            when productErrors is not an empty list.
        """
        body = get_payload(product_id, file_path)

        response = graphql_multipart_request(
            body, self.headers, self.endpoint_url)

        errors = response["data"]["productImageCreate"]["productErrors"]
        handle_errors(errors)

        return response["data"]["productImageCreate"]["image"]["id"]