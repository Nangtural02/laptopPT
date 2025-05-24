# web.py
from .home import home
from .basic_search import basic_search_form, search_basic
from .advanced_search import advanced_search_form, search_advanced
from .results import render_results
from .detail_laptop import notebook_detail

def configure_routes(app):
    app.add_url_rule('/', view_func=home)
    app.add_url_rule('/search/basic', view_func=basic_search_form, methods=['GET'])
    app.add_url_rule('/search/basic', view_func=search_basic, methods=['POST'])
    app.add_url_rule('/search/advanced', view_func=advanced_search_form, methods=['GET'])
    app.add_url_rule('/search/advanced', view_func=search_advanced, methods=['POST'])
    app.add_url_rule('/results', view_func=render_results, methods=['GET'])
    app.add_url_rule('/results', view_func=render_results, methods=['POST'])
    app.add_url_rule('/notebook/<int:id>', view_func=notebook_detail, methods=['GET'])
