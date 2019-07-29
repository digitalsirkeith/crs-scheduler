from flask import Blueprint, render_template, request
from flaskr.blueprints import helper

bp = Blueprint('root', __name__)

@bp.route('/', methods=('GET',))
def root():
    if request.method == 'GET':
        from flaskr.library import scraper
        scraper.scrape()
        return render_template('home.html', helper=helper)