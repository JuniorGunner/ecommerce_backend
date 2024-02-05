import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from models.product import ProductModel
from schemas.product import ProductSchema
from services import product_service


@pytest.fixture
def mock_db_session(mocker):
    # Mock the Session object
    session = mocker.MagicMock(spec=Session)
    return session


@pytest.fixture
def product_data():
    return ProductSchema(name="Test Product", description="Test Description", price=100.00)


def test_get_products(mock_db_session):
    # Mock the query.all() method to return a list of products
    mock_db_session.query.return_value.all.return_value = [ProductModel(name="Product 1", description="Description 1", price=50.00),
                                                           ProductModel(name="Product 2", description="Description 2", price=150.00)]
    products = product_service.get_products(mock_db_session)
    assert len(products) == 2
    assert products[0].name == "Product 1"
    assert products[1].price == 150.00


def test_get_product(mock_db_session):
    # Mock the query.filter().first() method to return a single product
    mock_db_session.query.return_value.filter.return_value.first.return_value = ProductModel(id=1, name="Product 1", description="Description 1", price=50.00)
    product = product_service.get_product(mock_db_session, 1)
    assert product.id == 1
    assert product.name == "Product 1"


def test_create_product(mock_db_session, product_data):
    # Mock the add, commit, and refresh methods
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    product = product_service.create_product(mock_db_session, product_data)
    assert product.name == product_data.name
    assert product.description == product_data.description
    assert product.price == product_data.price
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_update_product(mock_db_session, product_data):
    # Mock the query.filter().first() method to return an existing product
    existing_product = ProductModel(id=1, name="Old Product", description="Old Description", price=50.00)
    mock_db_session.query.return_value.filter.return_value.first.return_value = existing_product

    updated_product = product_service.update_product(mock_db_session, 1, product_data)
    assert updated_product.id == 1
    assert updated_product.name == product_data.name
    assert updated_product.description == product_data.description
    assert updated_product.price == product_data.price


def test_delete_product(mock_db_session):
    # Mock the query.filter().first() method to simulate finding a product to delete
    mock_db_session.query.return_value.filter.return_value.first.return_value = ProductModel(id=1)
    # Mock the delete and commit methods
    mock_db_session.delete = MagicMock()
    mock_db_session.commit = MagicMock()

    result = product_service.delete_product(mock_db_session, 1)
    assert result is True
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
