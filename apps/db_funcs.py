import psycopg2
from flask import render_template

def get_barmans():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"barman\"")
    barmans = cur.fetchall()
    cur.close()
    conn.close()
    return barmans

def get_coctails():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"koktajl\"")
    koktail = cur.fetchall()
    cur.close()
    conn.close()
    return koktail

def set_average_grade(coctail, ocena, typ):
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    if (typ == 'user'): 
        cur.execute(f'update "koktajl" set srednia_ocena_użytkownika = \'{ocena}\' where nazwa = \'{coctail}\'')
    elif (typ == 'somm'):
        cur.execute(f'update "koktajl" set srednia_ocena_sommeliera = \'{ocena}\' where nazwa = \'{coctail}\'')

    conn.commit()
    cur.close()
    conn.close()
    return 0

def update_average_grade(coctail_name):
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()

    user_grades_query = f'select ocena_uzytkownika from "odpowiedz_koktajl" where koktajl_nazwa = \'{coctail_name}\''
    somm_grades_query = f'select ocena from "koktajl_sommelier" where koktajl_nazwa = \'{coctail_name}\''

    user_grade = 0
    somm_grade = 0
    try:
        cur.execute(user_grades_query)
        user_grades = cur.fetchall()
        user_grades_edited = []

        for i in range(len(user_grades)):
            user_grades_edited.append(user_grades[i][0])

        if len(user_grades_edited) != 0:
            user_grade = round(sum(user_grades_edited)/len(user_grades_edited),2)


    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()   

    try:
        cur.execute(somm_grades_query)
        somm_grades = cur.fetchall()
        somm_grades_edited = []

        for i in range(len(somm_grades)):
            somm_grades_edited.append(somm_grades[i][0])

        if len(somm_grades_edited) != 0:
            somm_grade = round(sum(somm_grades_edited)/len(somm_grades_edited),2)
        
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()   


    try:
        cur.execute(f'update "koktajl" set srednia_ocena_użytkownika = \'{user_grade}\' where nazwa = \'{coctail_name}\'')
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()  
    try:
        cur.execute(f'update "koktajl" set srednia_ocena_sommeliera = \'{somm_grade}\' where nazwa = \'{coctail_name}\'')

    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()  

    conn.commit()
    cur.close()
    conn.close()
    return 0

def get_odpowiedz_koktajl():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"odpowiedz_koktajl\" order by id")
    koktail_review = cur.fetchall()
    cur.close()
    conn.close()
    return koktail_review

def get_questionnaire():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"ankieta\"")
    questionnaire = cur.fetchall()
    cur.close()
    conn.close()
    return questionnaire

def get_coctail_sommelier():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"koktajl_sommelier\" order by id")
    coctail_som = cur.fetchall()
    cur.close()
    conn.close()
    return coctail_som

def get_questions():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"pytanie\"")
    questionnaire = cur.fetchall()
    cur.close()
    conn.close()
    return questionnaire

def get_sommeliers():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"sommelier\"")
    sommelier = cur.fetchall()
    cur.close()
    conn.close()
    print(sommelier)
    return sommelier

def costyl():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"Users\"")
    users = cur.fetchall()
    
    # print(users[0][0])
    # return render_template('coctails_cards.html', users=users)
    # for i in range(5):
    #     name = 'Idsa' + str(i+2)
    #     querry = 'INSERT INTO \"Users\" (username, email, password) VALUES (\'{}\', \'gdggd@ad.ru\', \'gdgdg\');'.format(name)
    #     cur.execute(querry)
    cur.close()
    conn.close()
    return users
    # conn.commit()
    return 0

def postgrees_connect():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    return conn

# def postgrees_compare_users():
    
    