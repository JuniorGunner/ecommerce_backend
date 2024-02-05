import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from models.order import OrderModel
from schemas.order import OrderSchema
from services import order_service


@pytest.fixture
def mock_db_session(mocker):
    # Mock the Session object
    session = mocker.MagicMock(spec=Session)
    return session


@pytest.fixture
def order_data():
    return OrderSchema(user_id=1, product_id=2, quantity=3, status="pending")


def test_create_order(mock_db_session, order_data):
    # Mock the add, commit, and refresh methods
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    order = order_service.create_order(mock_db_session, order_data)
    assert order.user_id == order_data.user_id
    assert order.product_id == order_data.product_id
    assert order.quantity == order_data.quantity
    assert order.status == order_data.status
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_get_order(mock_db_session):
    # Mock the query.filter().first() method to return a single order
    mock_order = OrderModel(id=1, user_id=1, product_id=2, quantity=3, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order

    order = order_service.get_order(mock_db_session, 1)
    assert order.id == 1
    assert order.status == "pending"


def test_list_user_orders(mock_db_session):
    # Mock the query.filter().all() method to return a list of orders
    mock_orders = [OrderModel(id=1, user_id=1, product_id=2, quantity=3, status="pending"),
                   OrderModel(id=2, user_id=1, product_id=3, quantity=1, status="completed")]
    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_orders

    orders = order_service.list_user_orders(mock_db_session, 1)
    assert len(orders) == 2
    assert orders[0].user_id == 1
    assert orders[1].status == "completed"


def test_update_order_status(mock_db_session):
    # Mock the query.filter().first() method to simulate finding an order to update
    mock_order = OrderModel(id=1, user_id=1, product_id=2, quantity=3, status="pending")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_order

    # Mock the commit and refresh methods
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    updated_order = order_service.update_order_status(mock_db_session, 1, "completed")
    assert updated_order.id == 1
    assert updated_order.status == "completed"
    mock_db_session.commit.assert_called_once()
