from flask import render_template, Blueprint, abort, request
from flask_paginate import Pagination, get_page_parameter
from cycling_app.api_routes import get_cycling, get_cyclings

# Define the Blueprint
main_bp = Blueprint("main", __name__)


@main_bp.errorhandler(500)
def internal_server_error(e):
    """Custom error message for Internal Server Error status code 500"""
    return render_template("500.html"), 500


@main_bp.errorhandler(404)
def page_not_found(e):
    """Custom error message for Not Found error with status code 404"""
    return render_template("404.html"), 404

@main_bp.route("/")
def index():
    """Returns the home menu"""
    response = get_cyclings()
    # print(response)
    # page = request.args.get('page')

    # if page and page.isdigit():
    #     page = int(page)
    # else: 
    #     page = 1

    # pages = response.query.paginate(page=page, per_page=10)    
    return render_template("index.html", cycling_list=response)

@main_bp.route("/display_cycling/<cycling_id>")
def display_cycling(cycling_id):
    """Returns the event detail page"""
    cyc = get_cycling(cycling_id)
    if cyc:
        return render_template("cycling.html", cycling=cyc)
    else:
        abort(404)
