# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.costyl import costyl 
import psycopg2

@blueprint.route('/index')
@login_required
def index():
    # costyl()
    return render_template('home/index.html', segment='index')


@blueprint.route('/coctails_cards.html',methods=('GET', 'POST'))
@login_required
def coctails_cards():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        github = request.form['github']

        if username and email and password:
            conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
            cur = conn.cursor()
            querry_add_user = 'INSERT INTO \"Users\" (username, email, password, oauth_github) VALUES (\'{}\', \'{}\', \'{}\',\'{}\');'.format(username, email, password, github)
            cur.execute(querry_add_user)
        
            conn.commit()
            cur.close()
            conn.close()
            return redirect('coctails_cards.html')


    try:
        users = costyl()
        # Serve the file (if exists) from app/templates/home/FILE.html
        segment = get_segment(request)
        return render_template("home/coctails_cards.html" , segment=segment, users=users)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500



@blueprint.route('/<template>', methods=('GET', 'POST'))
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None