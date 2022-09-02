from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from .common_service import service_handler

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
def create_size():
    return service_handler(SizeController.create(request.json))


@size.route('/', methods=PUT)
def update_size():
    return service_handler(SizeController.update(request.json))


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return service_handler(SizeController.get_by_id(_id))


@size.route('/', methods=GET)
def get_all_sizes():
    return service_handler(SizeController.get_all())
