import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from models.cart import CartItemModel
from schemas.cart import CartItemCreateSchema
from services import cart_service


@pytest.fixture
def mock_db_session(mocker):
    # Mock the Session object
    session = mocker.MagicMock(spec=Session)
    return session


@pytest.fixture
def cart_item_data():
    return CartItemCreateSchema(user_id=1, product_id=2, quantity=3)


def test_add_item_to_cart(mock_db_session, cart_item_data):
    user_id = 1
    # Mock the add, commit, and refresh methods
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    cart_item = cart_service.add_item_to_cart(mock_db_session, cart_item_data, user_id)
    assert cart_item.product_id == cart_item_data.product_id
    assert cart_item.quantity == cart_item_data.quantity
    assert cart_item.user_id == user_id
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_get_cart_items(mock_db_session):
    user_id = 1
    # Mock the query.filter().all() method to return a list of cart items
    mock_db_session.query.return_value.filter.return_value.all.return_value = [
        CartItemModel(id=1, user_id=user_id, product_id=2, quantity=3),
        CartItemModel(id=2, user_id=user_id, product_id=3, quantity=1)
    ]

    cart_items = cart_service.get_cart_items(mock_db_session, user_id)
    assert len(cart_items) == 2
    assert cart_items[0].product_id == 2
    assert cart_items[1].quantity == 1


def test_remove_item_from_cart(mock_db_session):
    item_id = 1
    user_id = 1
    # Mock the query.filter().first() method to simulate finding a cart item to delete
    mock_db_session.query.return_value.filter.return_value.first.return_value = CartItemModel(id=item_id, user_id=user_id)

    # Mock the delete and commit methods
    mock_db_session.delete = MagicMock()
    mock_db_session.commit = MagicMock()

    result = cart_service.remove_item_from_cart(mock_db_session, item_id, user_id)
    assert result is True
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()
