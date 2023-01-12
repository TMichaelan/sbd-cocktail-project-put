import psycopg2


def costyl():

    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')

    cur = conn.cursor()
    cur.execute("SELECT * FROM \"Users\"")
    # users = cur.fetchall()

    
    for i in range(20):
        name = 'jora' + str(i)
        querry = 'INSERT INTO \"Users\" (username, email, password) VALUES (\'{}\', \'gdggd@ad.ru\', \'gdgdg\');'.format(name)
        cur.execute(querry)

    # conn.commit()
    return 0
