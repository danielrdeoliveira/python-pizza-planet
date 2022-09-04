from faker import Faker

from random import choice, sample, randint
from datetime import datetime

from app.repositories.managers import SizeManager, IngredientManager, BeverageManager, OrderManager

beverages = [
    {"name": "Coke", "price": 2.0},
    {"name": "Sprite", "price": 1.5},
    {"name": "Orange Juice", "price": 2.0},
    {"name": "Diet Coke", "price": 2.0},
    {"name": "Water", "price": 1.0}
]

sizes = [
    {'name': 'Tiny', 'price': 4},
    {'name': 'Small', 'price': 7},
    {'name': 'Medium', 'price': 9},
    {'name': 'Large', 'price': 12},
    {'name': 'Family', 'price': 15},
]

ingredients = [
    {"name": "Mozzarella", "price": 1.0},
    {"name": "Pepperoni", "price": 1.5},
    {"name": "Chicken", "price": 1.0},
    {"name": "Tuna", "price": 2.0},
    {"name": "Pineapple", "price": 1.5},
    {"name": "Ham", "price": 1.5},
    {"name": "Gorgonzola", "price": 2.0},
    {"name": "Olive", "price": 0.5},
    {"name": "Eggs", "price": 1.0},
    {"name": "Onion", "price": 0.5}
]

total_orders = 500
total_clients = 20

fakeit = Faker()


def create_client():
    return {
        "client_address": fakeit.address(),
        "client_dni": fakeit.ssn(),
        "client_name": fakeit.name(),
        "client_phone": fakeit.phone_number(),
    }


def create_sizes():
    for size in sizes:
        SizeManager.create(size)


def create_ingredients():
    for ingredient in ingredients:
        IngredientManager.create(ingredient)


def create_beverages():
    for beverage in beverages:
        BeverageManager.create(beverage)


def calculate_total_price(size, all_ingredients, all_beverages):
    price = size['price']
    price += sum([ingredient["price"] for ingredient in all_ingredients])
    price += sum([beverage["price"] for beverage in all_beverages])
    return price


def create_orders():
    clients = [create_client() for _ in range(total_clients)]
    all_sizes = SizeManager.get_all()
    all_ingredients = IngredientManager.get_all()
    all_beverages = BeverageManager.get_all()

    for _ in range(total_orders):
        size = choice(all_sizes)
        order_ingredients = sample(all_ingredients, randint(1, len(all_ingredients)))
        order_beverages = sample(all_beverages, randint(1, len(all_beverages)))
        total_price = calculate_total_price(size, order_ingredients, order_beverages)
        order_data = choice(clients) | {
            "date": fakeit.date_time_between(
                datetime(2022, 1, 1),
                datetime(2022, 12, 31)),
            "size_id": size["_id"],
            "total_price": total_price,
        }
        ingredients_list = IngredientManager.get_by_id_list(
            [ingredient["_id"] for ingredient in order_ingredients]
        )
        beverages_list = BeverageManager.get_by_id_list(
            [beverage["_id"] for beverage in order_beverages]
        )
        OrderManager.create(order_data, ingredients_list, beverages_list)


def seed_database():
    create_sizes()
    create_ingredients()
    create_beverages()
    create_orders()
