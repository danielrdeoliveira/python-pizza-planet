from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column, func, desc

from .models import Ingredient, Order, OrderDetail, Size, Beverage, db
from .serializers import (IngredientSerializer, OrderSerializer, OrderDetailSerializer,
                          SizeSerializer, BeverageSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)

        ingredients_detail = (
            OrderDetail(
                order_id=new_order._id,
                ingredient_id=ingredient._id,
                ingredient_price=ingredient.price)
            for ingredient in ingredients)
        beverages_detail = (
            OrderDetail(
                order_id=new_order._id,
                beverage_id=beverage._id,
                beverage_price=beverage.price)
            for beverage in beverages)

        cls.session.add_all(ingredients_detail)
        cls.session.add_all(beverages_detail)
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not supported for {cls.__name__}')

    @classmethod
    def get_top_customers(cls):
        customers_query = cls.session.query(
            func.count(cls.model._id).label('num_orders'),
            cls.model.client_name
        ).group_by(cls.model.client_name).order_by(desc('num_orders')).limit(3).all()
        top_customers = []
        for customer in customers_query:
            top_customers.append(
                {'client_name': customer.client_name, 'num_orders': customer.num_orders})
        return top_customers

    @classmethod
    def get_top_month(cls):
        top_months = cls.session.query(
            func.strftime('%m-%Y', cls.model.date).label('month'),
            func.sum(cls.model.total_price).label("revenue")
            ).group_by('month').order_by(desc("revenue")).limit(3).all()
        result = []
        for mon in top_months:
            result.append(
                {'month': mon.month, 'revenue': mon.revenue})
        return result


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()


class OrderDetailManager(BaseManager):
    model = OrderDetail
    serializer = OrderDetailSerializer

    @classmethod
    def get_top_ingredient(cls):
        top_ingredients = cls.session.query(
            func.count(cls.model.ingredient_id).label('request_count'),
            Ingredient.name
        ).join(Ingredient).\
            group_by(cls.model.ingredient_id).order_by(desc('request_count')).limit(3)

        result = []
        for ingredient in top_ingredients:
            result.append(
                {'request_count': ingredient.request_count, 'name': ingredient.name})
        return result
