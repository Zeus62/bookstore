from flask import Blueprint

main = Blueprint("main", __name__)

from Book_Store.Main import routes
