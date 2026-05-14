from flask import Blueprint

users = Blueprint("users", __name__)

from Book_Store.users import routes
