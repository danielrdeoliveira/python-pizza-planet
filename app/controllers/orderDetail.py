from ..repositories.managers import OrderDetailManager
from .base import BaseController


class OrderDetailController(BaseController):
    manager = OrderDetailManager

    @classmethod
    def get_top_ingredient(cls):
        return OrderDetailManager.get_top_ingredient()
