#  Nikulin Vasily © 2021
from flask import Blueprint

from .api import api, socket

market = Blueprint('market', __name__, subdomain='market', template_folder='templates',
                   static_folder='static', static_url_path='/market/static')
market.register_blueprint(api)

from .index import index
from .companies import companies
from .company_panel import company_panel
from .create_company import create_company
from .game_result import game_result
from .marketplace import marketplace
from .news import news
from .game_panel import game_panel
from .sessions import sessions
from .user_panel import user_panel
from .voting import stockholders_voting
from .errors import error_page
