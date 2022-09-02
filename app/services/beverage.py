from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from .common_service import service_handler
from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)


@beverage.route('/', methods=POST)
def create_beverage():
    return service_handler(BeverageController.create(request.json))


@beverage.route('/', methods=PUT)
def update_beverage():
    return service_handler(BeverageController.update(request.json))


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return service_handler(BeverageController.get_by_id(_id))


@beverage.route('/', methods=GET)
def get_beverages():
    return service_handler(BeverageController.get_all())
