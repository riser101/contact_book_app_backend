from flask import Blueprint

operations = Blueprint('operations', __name__)

from . import views