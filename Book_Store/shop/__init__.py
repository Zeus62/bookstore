from flask import Blueprint

shop = Blueprint('shop', __name__)

from Book_Store.shop import routes
