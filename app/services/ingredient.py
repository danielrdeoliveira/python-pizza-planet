from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from .common_service import service_handler


ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
@service_handler()
def create_ingredient():
    return IngredientController.create(request.json)


@ingredient.route('/', methods=PUT)
@service_handler()
def update_ingredient():
    return IngredientController.update(request.json)


@ingredient.route('/id/<_id>', methods=GET)
@service_handler()
def get_ingredient_by_id(_id: int):
    return IngredientController.get_by_id(_id)


@ingredient.route('/', methods=GET)
@service_handler()
def get_ingredients():
    return IngredientController.get_all()
