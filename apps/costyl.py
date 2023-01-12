import psycopg2
from flask import render_template


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
