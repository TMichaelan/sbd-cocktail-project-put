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


def get_sommeliers():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
    cur.execute("SELECT * FROM \"Sommelier\"")
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
    
    