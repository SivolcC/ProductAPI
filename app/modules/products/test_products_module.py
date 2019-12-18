"""
app/modules/api/products/test_products_module.py
Unittest for products module
"""
import pytest
import json


def test_list_products(flask_app_client):
    response = flask_app_client.get('/api/products')
    assert response.status_code == 200


def test_create_product(flask_app_client):
    test_product_name = "Test product"
    test_product_description = "Test product description"
    test_product_price = 54.9
    test_product_delivery_price = 19.9

    # Creates a product
    response = flask_app_client.post('/api/products', json={
        "Name": test_product_name,
        "Description": test_product_description,
        "Price": test_product_price,
        "DeliveryPrice": test_product_delivery_price
    })
    # Asserts response
    assert response.status_code == 200
    created_product = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert created_product['Name'] == test_product_name
    assert created_product['Description'] == test_product_description
    assert created_product['Price'] == test_product_price
    assert created_product['DeliveryPrice'] == test_product_delivery_price

    # Get created product
    response = flask_app_client.get('/api/products/' + created_product['Id'])
    assert response.status_code == 200
    # Assert values
    created_product = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert created_product['Name'] == test_product_name
    assert created_product['Description'] == test_product_description
    assert created_product['Price'] == test_product_price
    assert created_product['DeliveryPrice'] == test_product_delivery_price

    # Delete product
    response = flask_app_client.delete('/api/products/' + created_product['Id'])
    assert response.status_code == 204


def test_get_product(flask_app_client, product_test_one):
    # Get product (fixture)
    response = flask_app_client.get('/api/products/' + str(product_test_one.id))
    assert response.status_code == 200
    # Asserts values
    product = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert product['Name'] == "Product Test One"
    assert product['Description'] == "Test product"
    assert product['Price'] == 42
    assert product['DeliveryPrice'] == 19.9


def test_update_product(flask_app_client, product_test_one):
    test_product_name = "Test product Updated"
    test_product_description = "Test product description updated"
    test_product_price = 108.9
    test_product_delivery_price = 39.9

    # Update product (fixture)
    response = flask_app_client.put('/api/products/' + str(product_test_one.id), json={
        "Name": test_product_name,
        "Description": test_product_description,
        "Price": test_product_price,
        "DeliveryPrice": test_product_delivery_price
    })
    assert response.status_code == 200
    # Asserts response
    updated_product = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert updated_product['Name'] == test_product_name
    assert updated_product['Description'] == test_product_description
    assert updated_product['Price'] == test_product_price
    assert updated_product['DeliveryPrice'] == test_product_delivery_price

    # Get updated product
    response = flask_app_client.get('/api/products/' + updated_product['Id'])
    assert response.status_code == 200
    # Asserts values
    updated_product = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert updated_product['Name'] == test_product_name
    assert updated_product['Description'] == test_product_description
    assert updated_product['Price'] == test_product_price
    assert updated_product['DeliveryPrice'] == test_product_delivery_price


def test_delete_product(flask_app_client):
    test_product_name = "Test product"
    test_product_description = "Test product description"
    test_product_price = 54.9
    test_product_delivery_price = 19.9

    # Create product
    response = flask_app_client.post('/api/products', json={
        "Name": test_product_name,
        "Description": test_product_description,
        "Price": test_product_price,
        "DeliveryPrice": test_product_delivery_price
    })
    assert response.status_code == 200
    created_product = json.loads(response.data.decode('utf-8').replace("'", '"'))
    # Delete product
    response = flask_app_client.delete('/api/products/' + created_product['Id'])
    assert response.status_code == 204


def test_get_product_options(flask_app_client, product_test_one):
    # Create product (fixture) option
    response = flask_app_client.post('/api/products/' + str(product_test_one.id) + '/options', json={
        "Name":  "Option Test One",
        "Description": "Option for Test product One",
    })
    # Get product (fixture) options
    response = flask_app_client.get('/api/products/' + str(product_test_one.id) + '/options')
    assert response.status_code == 200
    # Asserts values
    product_options = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert response.status_code == 200
    assert len(product_options['Items']) == product_options['total'] or product_options['per_page']
    assert product_options['Items'][0]['Name'] == "Option Test One"
    assert product_options['Items'][0]['Description'] == "Option for Test product One"
