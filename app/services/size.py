from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from .common_service import service_handler

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
@service_handler()
def create_size():
    return SizeController.create(request.json)


@size.route('/', methods=PUT)
@service_handler()
def update_size():
    return SizeController.update(request.json)


@size.route('/id/<_id>', methods=GET)
@service_handler()
def get_size_by_id(_id: int):
    return SizeController.get_by_id(_id)


@size.route('/', methods=GET)
@service_handler()
def get_all_sizes():
    return SizeController.get_all()
