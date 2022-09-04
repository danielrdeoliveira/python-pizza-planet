import pytest
from app.controllers import OrderDetailController, OrderController
from ..utils.functions import shuffle_list


def test_get_top_ingredient(client_data, create_size, create_beverages, create_ingredients):
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = create_size.json['_id']
    ingredients_count = [0]*10
    for _ in range(60):
        shuffled_ingredients = shuffle_list(ingredients)[0:3]
        order = {
            **client_data,
            'ingredients': shuffled_ingredients,
            'beverages': beverages,
            'size_id': size_id
        }
        created_order, _ = OrderController.create(order)
        for ing in shuffled_ingredients:
            ingredients_count[ing-1] += 1
    top_ingredient = OrderDetailController.get_top_ingredient()

    calc_top_ingredients = []
    max_count = max(ingredients_count)
    index_list = [index for index in range(len(ingredients_count)) if ingredients_count[index] == max_count]
    ing_ids = [index + 1 for index in index_list]
    for ing_id in ing_ids:
        calc_top_ingredients.append(
            {'request_count': max_count,
             'name': [item['name'] for item in create_ingredients if item.get('_id') == ing_id][0]})
    assert (top_ingredient[0] in calc_top_ingredients)
