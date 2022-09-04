import pytest
from random import randint
from datetime import datetime

from app.controllers import (IngredientController, OrderController,
                             SizeController, BeverageController)
from app.controllers.base import BaseController
from app.test.utils.functions import get_random_choice


def __order(ingredients: list, beverages: list, size: dict, client_data: dict):
    ingredients = [ingredient.get('_id') for ingredient in ingredients]
    beverages = [beverage.get('_id') for beverage in beverages]
    size_id = size.get('_id')
    return {
        **client_data,
        'ingredients': ingredients,
        'beverages': beverages,
        'size_id': size_id
    }


def __create_items(items: list, controller: BaseController):
    created_items = []
    for item_type in items:
        created_item, _ = controller.create(item_type)
        created_items.append(created_item)
    return created_items


def __create_order_detail_items(ingredients: list, beverages: list, sizes: list):
    created_ingredients = __create_items(ingredients, IngredientController)
    created_beverages = __create_items(beverages, BeverageController)
    created_sizes = __create_items(sizes, SizeController)
    return created_sizes if len(created_sizes) > 1 else created_sizes.pop(), created_ingredients, created_beverages


def test_create(app, ingredients, beverages, size, client_data):
    created_size, created_ingredients, created_beverages = __create_order_detail_items(ingredients, beverages, [size])

    order = __order(created_ingredients, created_beverages, created_size, client_data)
    created_order, error = OrderController.create(order)
    size_id = order.pop('size_id', None)
    ingredient_ids = order.pop('ingredients', [])
    beverage_ids = order.pop('beverages', [])

    pytest.assume(error is None)
    for param, value in order.items():
        pytest.assume(param in created_order)
        pytest.assume(value == created_order[param])
        pytest.assume(created_order['_id'])
        pytest.assume(size_id == created_order['size']['_id'])

        beverages_in_detail = set(item['beverage']['_id'] for item in created_order['detail'] if item['beverage'])
        pytest.assume(not beverages_in_detail.difference(beverage_ids))
        ingredients_in_detail = set(item['ingredient']['_id'] for item in created_order['detail'] if item['ingredient'])
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))


def test_calculate_order_price(app, order: dict):
    created_order, _ = OrderController.create(order)
    created_size = created_order['size']
    size_price = created_size['price']
    beverages_in_detail = [item['beverage'] for item in created_order['detail'] if item['beverage']]
    beverages_price = sum([beverage['price'] for beverage in beverages_in_detail])
    ingredients_in_detail = [item['ingredient'] for item in created_order['detail'] if item['ingredient']]
    ingredients_price = sum([ingredient['price'] for ingredient in ingredients_in_detail])

    pytest.assume(created_order['total_price'] == round(size_price + beverages_price + ingredients_price, 2))


def test_get_by_id(app, order: dict):
    created_order, _ = OrderController.create(order)
    order_from_db, error = OrderController.get_by_id(created_order['_id'])
    size_id = order.pop('size_id', None)
    ingredient_ids = order.pop('ingredients', [])
    beverage_ids = order.pop('beverages', [])
    pytest.assume(error is None)
    for param, value in created_order.items():
        pytest.assume(order_from_db[param] == value)
        pytest.assume(size_id == created_order['size']['_id'])

        beverages_in_detail = set(item['beverage']['_id'] for item in created_order['detail'] if item['beverage'])
        pytest.assume(not beverages_in_detail.difference(beverage_ids))
        ingredients_in_detail = set(item['ingredient']['_id'] for item in created_order['detail'] if item['ingredient'])
        pytest.assume(not ingredients_in_detail.difference(ingredient_ids))


def test_get_all(app, order: dict):
    created_orders = []
    for _ in range(5):
        created_order, _ = OrderController.create(order)
        created_orders.append(created_order)

    orders_from_db, error = OrderController.get_all()
    searchable_orders = {db_order['_id']: db_order for db_order in orders_from_db}
    pytest.assume(error is None)
    for created_order in created_orders:
        current_id = created_order['_id']
        assert current_id in searchable_orders
        for param, value in created_order.items():
            pytest.assume(searchable_orders[current_id][param] == value)


def test_get_top_customer(clients_data, create_size, create_beverages, create_ingredients):

    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = create_size.json['_id']
    clients_count = {}
    for client in clients_data:
        clients_count.update({client['client_name']: 0})
    for _ in range(60):
        client = get_random_choice(clients_data)
        clients_count[client['client_name']] += 1

        order = {
            **client,
            'ingredients': ingredients,
            'beverages': beverages,
            'size_id': size_id
        }
        created_order, _ = OrderController.create(order)

    top_customers = OrderController.get_top_customers()
    top_clients = [key for key, value in clients_count.items() if value == max(clients_count.values())]

    assert top_customers[0]['client_name'] in top_clients


def test_get_top_month(order: dict):
    month_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    for _ in range(30):
        rand_date = datetime(2022, randint(1, 12), 1)
        order_with_date = order | {
            'date': rand_date
        }
        month_count[rand_date.month] += 1
        created_order, _ = OrderController.create(order_with_date)
    top_month = OrderController.get_top_month()

    top_calc_months = [key for key, value in month_count.items() if value == max(month_count.values())]

    assert int(top_month[0]['month'][0:2]) in top_calc_months
