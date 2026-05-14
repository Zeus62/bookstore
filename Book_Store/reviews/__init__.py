from flask import Blueprint

reviews_bp = Blueprint("reviews_bp", __name__)

from Book_Store.reviews import routes
