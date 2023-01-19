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

def get_odpowiedz_koktajl():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"odpowiedz_koktajl\"")
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
    
    