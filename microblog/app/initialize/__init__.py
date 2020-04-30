from flask import Blueprint

bp = Blueprint('initialize', __name__)

from app.initialize import routes
