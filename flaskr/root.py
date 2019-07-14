from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('root', __name__)

@bp.route('/', methods=('GET',))
def root():
    if request.method == 'GET':
        return render_template('home.html')