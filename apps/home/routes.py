# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import psycopg2
from apps.home import blueprint
from flask import render_template, request, redirect, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound


from apps.costyl import costyl,get_questionnaire,get_coctail_sommelier,get_barmans, get_sommeliers, get_coctails
import psycopg2
import random

@blueprint.route('/index')
@login_required
def index():
    # costyl()

    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()

    querry_cotails = "select * FROM \"koktajl\" "
    cur.execute(querry_cotails)
    all_coctails = cur.fetchall()

    random_indexes = random.sample(range(len(all_coctails)), 9)
    
    coctails = []
    for index in random_indexes:
        coctails.append(all_coctails[index])
     

    cur.close()
    conn.close()
 
    return render_template('home/index.html', segment='index', coctails=coctails)


@blueprint.route('/index/<coctail_name>')
def product_page(coctail_name):

    coctail_name =  " ".join(coctail_name.split('-'))

    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cur = conn.cursor()
        querry_cotails = "select * FROM \"koktajl\" WHERE nazwa=\'{}\'".format(coctail_name)
        cur.execute(querry_cotails)
        coctail = cur.fetchone()
        cur.close()
        conn.close()

        if coctail == None:
            return render_template('home/page-404.html'), 404
    except Exception as err:
        print(f'error occurred: {err}')
    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cur = conn.cursor()
        querry_cotails = "select * FROM \"przepis\" WHERE nazwa_przepisa=\'{}\'".format(coctail_name)
        cur.execute(querry_cotails)
        recipe = cur.fetchone()

        querry_ingredients = "select * FROM \"skladnik_przepis\" WHERE przepis_nazwa_przepisa=\'{}\'".format(coctail_name)
        cur.execute(querry_ingredients)
        ingredients = cur.fetchall()

        print(ingredients)

        querry_category =  "select * FROM \"kategoria_koktajli_koktajl\" WHERE koktajl_nazwa=\'{}\'".format(coctail_name)
        cur.execute(querry_category)
        category = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as err:
        print(f'error occurred: {err}')
    
    return render_template('home/coctail.html', coctail=coctail, recipe=recipe, ingredients = ingredients, category= category)


@blueprint.route('/sommelier.html',methods=('GET', 'POST'))
# @login_required
def sommelier():

    if request.method == 'POST':
        name = request.form['name']
        coctail = request.form['coctail']
        recencja = request.form['recencja']
        ocena = request.form['ocena']

        # print(username, email, password, github)

        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cur = conn.cursor()
        querry_add_user = 'INSERT INTO \"sommelier\" VALUES (\'{}\', \'{}\', \'{}\');'.format(name, recencja, ocena)
        querry_add_coctail = 'INSERT INTO \"sommelier_koktajl\" VALUES (\'{}\', \'{}\');'.format(name, coctail)
        cur.execute(querry_add_user)
        cur.execute(querry_add_coctail)

     
        conn.commit()
        cur.close()
        conn.close()
        return redirect('sommelier.html')


    try:
        users = get_sommeliers()
        coctails = get_coctails()
        coctails_som = get_coctail_sommelier()
        # Serve the file (if exists) from app/templates/home/FILE.html
        segment = get_segment(request)
        return render_template("home/sommelier.html" , segment=segment, users=users, len = len(users), coctails = coctails, coctails_som = coctails_som)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/questionnaire.html',methods=('GET', 'POST'))
# @login_required
def questionnaire():
    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']

        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cur = conn.cursor()
        querry_add_user = 'INSERT INTO \"ankieta\" VALUES (\'{}\', \'{}\');'.format(name, count)
        cur.execute(querry_add_user)
        conn.commit()

        for i in range(int(count)):
            question_name = request.form['question_name'+str(i)]
            text = request.form['question_text'+str(i)]
            
            try: 
                querry_add_pytanie = 'INSERT INTO \"pytanie\" VALUES (\'{}\', \'{}\');'.format(question_name, text)
                cur.execute(querry_add_pytanie)
            except Exception as err:
                print(f'error occurred: {err}')

            querry_add_ankieta_pytanie = 'INSERT INTO \"ankieta_pytanie\" VALUES (\'{}\', \'{}\');'.format(name, question_name)
            conn.commit()
            cur.execute(querry_add_ankieta_pytanie)

        conn.commit()
        cur.close()
        conn.close()
        return redirect('questionnaire.html')


    try:
        users = get_questionnaire()
        segment = get_segment(request)
        return render_template("home/questionnaire.html" , segment=segment, users=users)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/delete-questionnaire', methods=['DELETE'])
def delete_questionnaire():
    # user_id = request.json
    name = request.form.get('name')

    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cursor = conn.cursor()
        querry_delete_ankieta_pytanie = f"DELETE FROM \"ankieta_pytanie\" WHERE ankieta_nazwa=\'{name}\'"
        querry_delete_ankieta = f"DELETE FROM \"ankieta\" WHERE nazwa=\'{name}\'"
        cursor.execute(querry_delete_ankieta_pytanie)
        conn.commit()
        cursor.execute(querry_delete_ankieta)
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return jsonify({"message": f"{count} user deleted"}), 200
        # return redirect('/', code=302)

    except (Exception, psycopg2.Error) as error :
        return jsonify({"error": str(error)}), 500


@blueprint.route('/coctails_cards.html',methods=('GET', 'POST'))
def coctails_cards():

    if request.method == 'POST':
        nazwa = request.form['nazwa']
        obraz = request.form['obraz']
        category = request.form['coctail']
        # srednia_ocena_uzytkownika = request.form['srednia_ocena_uzytkownika']
        # srednia_ocena_sommelier = request.form['srednia_ocena_sommelier']
        notatka = request.form['notatka']
        count = request.form['count']
        

        # print(username, email, password, github)

        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cur = conn.cursor()
        querry_add_przepis = 'INSERT INTO \"przepis\" VALUES (\'{}\', \'{}\', \'{}\');'.format(nazwa, count, notatka)
        querry_add_coctail = 'INSERT INTO \"koktajl\" VALUES (\'{}\', \'{}\');'.format(nazwa, obraz)


        # try: 
        #     querry_add_category = 'INSERT INTO \"kategoria_koktajli\" VALUES (\'{}\');'.format(category)
        #     cur.execute(querry_add_category)
        # except Exception as err:
        #     print(f'error occurred: {err}')



        cur.execute(querry_add_przepis)
        cur.execute(querry_add_coctail)

        conn.commit()

        
        querry_add_category_koktail = 'INSERT INTO \"kategoria_koktajli_koktajl\" VALUES (\'{}\', \'{}\');'.format(category, nazwa)
        cur.execute(querry_add_category_koktail)

        conn.commit()


        for i in range(int(count)):
            skladnik = request.form['ingredient'+str(i)]
            miara = request.form['measure'+str(i)]
            
            try: 
                querry_add_skladnik = 'INSERT INTO \"skladnik\" VALUES (\'{}\');'.format(skladnik)
                cur.execute(querry_add_skladnik)
            except Exception as err:
                print(f'error occurred: {err}')

            querry_add_skladnik_przepis = 'INSERT INTO \"skladnik_przepis\" VALUES (\'{}\', \'{}\', \'{}\');'.format(skladnik, nazwa, miara)
            conn.commit()
            cur.execute(querry_add_skladnik_przepis)
     
        conn.commit()
        cur.close()
        conn.close()
        return redirect('coctails_cards.html')


    try:
        users = get_coctails()
        # Serve the file (if exists) from app/templates/home/FILE.html
        segment = get_segment(request)
        return render_template("home/coctails_cards.html" , segment=segment, users=users)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/delete-sommelier', methods=['DELETE'])
def delete_sommelier():
    # user_id = request.json
    name = request.form.get('name')
    
    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cursor = conn.cursor()
        query = f"DELETE FROM \"sommelier\" WHERE pseudonim=\'{name}\'"
        cursor.execute(query)
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return jsonify({"message": f"{count} user deleted"}), 200
        # return redirect('/', code=302)

    except (Exception, psycopg2.Error) as error :
        return jsonify({"error": str(error)}), 500


@blueprint.route('/modify-barman', methods=['PUT'])
def modifyBarman():
    id = request.form.get('id')
    name = request.form.get('name')
    surname = request.form.get('surname')
    phone = request.form.get('phone')
    adress = request.form.get('adress')

    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cursor = conn.cursor()
        query = f"UPDATE \"barman\" SET imie=\'{name}\',nazwisko=\'{surname}\',numer_telefonu=\'{phone}\',adres=\'{adress}\' WHERE id=\'{id}\';"
        cursor.execute(query)
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return jsonify({"message": f"{count} user modified"}), 200
    except (Exception, psycopg2.Error) as error :
        return jsonify({"error": str(error)}), 500 


@blueprint.route('/get-barman-data', methods=(['GET']))
def getBarmanData():
    name = request.args.get('name')
    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cursor = conn.cursor()
        query = f"SELECT * FROM \"barman\" WHERE imie=\'{name}\'"
        cursor.execute(query)
        barman_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"name": barman_data[0], "surname": barman_data[1],"phone": barman_data[2], "address": barman_data[3],"id": barman_data[4], }), 200

    except (Exception, psycopg2.Error) as error :
        return jsonify({"error": str(error)}), 500


  
@blueprint.route('/delete-barman', methods=['DELETE'])
def delete_user():
    # user_id = request.json
    name = request.form.get('name')

    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cursor = conn.cursor()
        query = f"DELETE FROM \"barman\" WHERE imie=\'{name}\'"
        cursor.execute(query)
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return jsonify({"message": f"{count} user deleted"}), 200
        # return redirect('/', code=302)

    except (Exception, psycopg2.Error) as error :
        return jsonify({"error": str(error)}), 500
        

@blueprint.route('/delete-user', methods=['DELETE'])
def delete_users():
    # user_id = request.json
    name = request.form.get('name')

    try:
        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cursor = conn.cursor()
        query = f"DELETE FROM \"koktajl\" WHERE nazwa=\'{name}\'"
        querry_delete_przepis = f"DELETE FROM \"przepis\" WHERE nazwa_przepisa=\'{name}\'"

        cursor.execute(query)
        cursor.execute(querry_delete_przepis)
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return jsonify({"message": f"{count} user deleted"}), 200
        # return redirect('/', code=302)

    except (Exception, psycopg2.Error) as error :
        return jsonify({"error": str(error)}), 500



@blueprint.route('/barman.html',methods=('GET', 'POST'))
@login_required
def barman():
    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        adres = request.form['adres']

        # print(username, email, password, github)

        conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
        cur = conn.cursor()
        querry_add_barman = 'INSERT INTO \"barman\" VALUES (\'{}\', \'{}\', \'{}\',\'{}\');'.format(name, surname, phone, adres)
        cur.execute(querry_add_barman)
     
        conn.commit()
        cur.close()
        conn.close()
        return redirect('barman.html')

    try:
        barmans = get_barmans()
        # Serve the file (if exists) from app/templates/home/FILE.html
        segment = get_segment(request)
        return render_template("home/barman.html" , segment=segment, barmans=barmans)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
        
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
        
        # Serve the file (if exists) from app/templates/home/FILE.html
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