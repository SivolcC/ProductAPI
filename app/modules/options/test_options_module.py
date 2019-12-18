"""
app/modules/api/products/test_products_module.py
Unittest for products module
"""
import pytest
import json



def test_create_product_option(flask_app_client, product_test_one):
    # Create product (fixture) option
    response = flask_app_client.post('/api/products/' + str(product_test_one.id) + '/options', json={
        "Name":  "Option Test One",
        "Description": "Option for Test product One",
    })
    assert response.status_code == 200
    # Asserts response
    created_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert created_option['Name'] == "Option Test One"
    assert created_option['Description'] == "Option for Test product One"
    # Get created optiom
    response = flask_app_client.get('/api/options/' + created_option['Id'])
    assert response.status_code == 200
    # Asserts values
    created_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert created_option['Name'] == "Option Test One"
    assert created_option['Description'] == "Option for Test product One"
    # Delete option
    response = flask_app_client.delete('/api/options/' + created_option['Id'])
    assert response.status_code == 204


def test_get_product_option(flask_app_client, product_test_one):
    # Create product (fixture) option
    response = flask_app_client.post('/api/products/' + str(product_test_one.id) + '/options', json={
        "Name":  "Option Test Two",
        "Description": "Option for Test product Two",
    })
    assert response.status_code == 200
    # Asserts response
    created_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert created_option['Name'] == "Option Test Two"
    assert created_option['Description'] == "Option for Test product Two"
    # Get created optiom
    response = flask_app_client.get('/api/options/' + created_option['Id'])
    assert response.status_code == 200
    # Asserts values
    created_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert created_option['Name'] == "Option Test Two"
    assert created_option['Description'] == "Option for Test product Two"


def test_update_product_option(flask_app_client, product_test_one):
    test_option_name = "Test Option Updated"
    test_option_description = "Test Option description updated"

    # Create product (fixture) option
    response = flask_app_client.post('/api/products/' + str(product_test_one.id) + '/options', json={
        "Name":  "Test Option",
        "Description": "Test Description",
    })
    assert response.status_code == 200
    created_option = json.loads(response.data.decode('utf-8').replace("'", '"'))

    # Update option
    response = flask_app_client.put('/api/options/' + created_option['Id'], json={
        "Name": test_option_name,
        "Description": test_option_description,
    })
    assert response.status_code == 200
    # Asserts values
    updated_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    assert updated_option['Name'] == test_option_name
    assert updated_option['Description'] == test_option_description
    # Get updated option
    response = flask_app_client.get('/api/options/' + updated_option['Id'])
    updated_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    # Asserts values
    assert response.status_code == 200
    assert updated_option['Name'] == test_option_name
    assert updated_option['Description'] == test_option_description


def test_delete_product_option(flask_app_client, product_test_one):
    # Create product (fixture) option
    response = flask_app_client.post('/api/products/' + str(product_test_one.id) + '/options', json={
        "Name":  "Option Test One",
        "Description": "Option for Test product One",
    })
    assert response.status_code == 200
    created_option = json.loads(response.data.decode('utf-8').replace("'", '"'))
    # Delete option
    response = flask_app_client.delete('/api/options/' + created_option['Id'])
    assert response.status_code == 204
