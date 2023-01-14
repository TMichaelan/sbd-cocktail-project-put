import requests
from requests.exceptions import HTTPError
import random
import psycopg2

data = [
        'strDrink',
        'strTags',
        'strAlcoholic',
        'strIngredient1',
        'strIngredient2',
        'strIngredient3',
        'strIngredient4',
        'strIngredient5',
        'strIngredient6',
        'strIngredient7',
        'strIngredient8',
        'strIngredient9',
        'strIngredient10',
        'strIngredient11',
        'strIngredient12',
        'strIngredient13',
        'strIngredient14',
        'strIngredient15',
        'strMeasure1',
        'strMeasure2',
        'strMeasure3',
        'strMeasure4',
        'strMeasure5',
        'strMeasure6',
        'strMeasure7',
        'strMeasure8',
        'strMeasure9',
        'strMeasure10',
        'strMeasure11',
        'strMeasure12',
        'strMeasure13',
        'strMeasure14',
        'strMeasure15',
        'strDrinkThumb',
        'strInstructions',
    ]


ingridients = ['strIngredient1', 'strIngredient2', 'strIngredient3', 'strIngredient4', 'strIngredient5', 'strIngredient6', 'strIngredient7', 
'strIngredient8', 'strIngredient9', 'strIngredient10', 'strIngredient11', 'strIngredient12', 'strIngredient13', 'strIngredient14', 'strIngredient15']

measures = ['strMeasure1', 'strMeasure2', 'strMeasure3', 'strMeasure4', 'strMeasure5', 'strMeasure6', 'strMeasure7', 'strMeasure8', 'strMeasure9', 
'strMeasure10', 'strMeasure11', 'strMeasure12', 'strMeasure13', 'strMeasure14', 'strMeasure15']

coctail_name = ''
coctail_tags = ''
coctail_image = ''
coctail_instruction = ''
coctail_alc = ''
coctail_ingridients = []
coctail_measures = []

def parse_coctail(number):
    global coctail_name, coctail_tags, coctail_image, coctail_instruction, coctail_alc, coctail_ingridients, coctail_measures
    try:
        id = number
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={}'.format(id))
        response.raise_for_status()
        jsonResponse = response.json()

        edited_response = jsonResponse['drinks'][0]
        for drink in edited_response:
            if drink in data:
                if drink == 'strDrink':
                    coctail_name = edited_response[drink]
                elif drink == 'strTags':
                    coctail_tags = edited_response[drink]
                elif drink == 'strDrinkThumb':
                    coctail_image = edited_response[drink]
                elif drink == 'strInstructions':
                    coctail_instruction = edited_response[drink]
                elif drink == 'strAlcoholic':
                    coctail_alc = edited_response[drink]
                elif drink == 'strInstructions':
                    coctail_instruction = edited_response[drink]
                elif drink == 'strInstructions':
                    coctail_instruction = edited_response[drink]

                if drink in ingridients:
                    if edited_response[drink] != None:
                        coctail_ingridients.append(edited_response[drink])
                if drink in measures:
                    if edited_response[drink] != None:
                        coctail_measures.append(edited_response[drink])
                    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

db_url = 'postgresql://joramba:admin@localhost:5432/bazy_danych'
def przepis():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    querry = 'INSERT INTO \"przepis\" VALUES (\'{}\', \'{}\', \'{}\');'.format(coctail_name,len(coctail_ingridients),coctail_instruction) 
    cur.execute(querry)
    conn.commit()
    cur.close()
    conn.close()

def koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    ocena1 = round(random.uniform(3, 5), 2)
    ocena2 = round(random.uniform(3, 5), 2)
    querry = 'INSERT INTO \"koktajl\" VALUES (\'{}\', \'{}\', \'{}\',\'{}\');'.format(coctail_name,coctail_image,ocena1,ocena2) 
    cur.execute(querry)
    conn.commit()
    cur.close()
    conn.close()

def kategoria_koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    querry = 'INSERT INTO \"kategoria_koktajli\" VALUES (\'{}\');'.format(coctail_alc) 
    cur.execute(querry)
    conn.commit()
    cur.close()
    conn.close()
    

def kategoria_koktajli_koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    querry = 'INSERT INTO \"kategoria_koktajli_koktajl\" VALUES (\'{}\', \'{}\');'.format(coctail_alc,coctail_name) 
    cur.execute(querry)
    conn.commit()
    cur.close()
    conn.close()

def czynnosc():
    pass

def skladnik():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    for ingredient in coctail_ingridients:
        querry = 'INSERT INTO \"skladnik\" VALUES (\'{}\');'.format(ingredient) 
        cur.execute(querry)
        conn.commit()

    cur.close()
    conn.close()

def skladnik_przepis():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    for ingr_measure in range(len(coctail_ingridients)):
        querry = 'INSERT INTO \"skladnik_przepis\" VALUES (\'{}\',\'{}\',\'{}\');'.format(coctail_ingridients[ingr_measure],coctail_name,coctail_measures[ingr_measure]) 
        # print(querry)
        cur.execute(querry)
        conn.commit()
    cur.close()
    conn.close()

amount = 30
number = 11000

for i in range(0,amount):
    number+=1
    parse_coctail(number)
    try:
        przepis()
        koktajl()
        kategoria_koktajl()
    except Exception as err:
        print(f'error occurred: {err}')
    
    try:
        kategoria_koktajli_koktajl()
    except Exception as err:
        print(f'error occurred: {err}')

amount = 30
number = 12560

for i in range(0,amount):
    number+=1
    parse_coctail(number)
    try:
        pass
        przepis()
        koktajl()
        kategoria_koktajl()
        skladnik()
    except Exception as err:
        print(f'error occurred: {err}')
    
    try:
        kategoria_koktajli_koktajl()
        skladnik_przepis()
    except Exception as err:
        print(f'error occurred: {err}')

