from flask import Blueprint, jsonify

from app.common.http_methods import GET
from app.controllers import OrderController, OrderDetailController

report = Blueprint('report', __name__)


@report.route("/ingredients", methods=GET)
def get_report():
    top_ingredient = OrderDetailController.get_top_ingredient()
    status_code = 200 if top_ingredient else 400
    return jsonify(top_ingredient), status_code


@report.route("/customers", methods=GET)
def get_report_customers():
    top_customers = OrderController.get_top_customers()
    status_code = 200 if top_customers else 400
    return jsonify(top_customers), status_code


@report.route("/month", methods=GET)
def get_report_month():
    top_month = OrderController.get_top_month()
    status_code = 200 if top_month else 400
    return jsonify(top_month), status_code
