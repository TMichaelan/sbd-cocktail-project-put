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


ingritients = ['strIngredient1', 'strIngredient2', 'strIngredient3', 'strIngredient4', 'strIngredient5', 'strIngredient6', 'strIngredient7', 
'strIngredient8', 'strIngredient9', 'strIngredient10', 'strIngredient11', 'strIngredient12', 'strIngredient13', 'strIngredient14', 'strIngredient15']

measures = ['strMeasure1', 'strMeasure2', 'strMeasure3', 'strMeasure4', 'strMeasure5', 'strMeasure6', 'strMeasure7', 'strMeasure8', 'strMeasure9', 
'strMeasure10', 'strMeasure11', 'strMeasure12', 'strMeasure13', 'strMeasure14', 'strMeasure15']

# print(round(random.uniform(3, 5), 2))

coctail_name = ''
coctail_tags = ''
coctail_image = ''
coctail_instruction = ''
coctail_alc = ''
coctail_ingritients = []
coctail_measures = []

def parse_coctail(number):
    global coctail_name, coctail_tags, coctail_image, coctail_instruction, coctail_alc, coctail_ingritients, coctail_measures
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

                if drink in ingritients:
                    if edited_response[drink] != None:
                        coctail_ingritients.append(edited_response[drink])
                if drink in measures:
                    if edited_response[drink] != None:
                        coctail_measures.append(edited_response[drink])
                    
                #  print( '\'' + str(i) + '\','  )
                # print(edited_response[drink])

        #     print( '\'' + str(i) + '\','  ) 
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

db_url = 'postgresql://joramba:admin@localhost:5432/bazy_danych'
def przepis():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    querry = 'INSERT INTO \"przepis\" VALUES (\'{}\', \'{}\', \'{}\');'.format(coctail_name,len(coctail_ingritients),coctail_instruction) 
    cur.execute(querry)
    conn.commit()
    cur.close()
    conn.close()

def koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    ocena1 = round(random.uniform(3, 5), 2)
    ocena2 = round(random.uniform(3, 5), 2)
    querry = 'INSERT INTO \"Koktajl\" VALUES (\'{}\', \'{}\', \'{}\',\'{}\');'.format(coctail_name,coctail_image,ocena1,ocena2) 
    cur.execute(querry)
    conn.commit()
    cur.close()
    conn.close()

def kategoria_koktajl():
    print(coctail_alc)

def czynnosc():
    pass

def skladnik():
    pass

number = 11009
# number = 11009

for i in range(25):
    number+=1
    parse_coctail(number)
    try:
        przepis()
        koktajl()
    except Exception as err:
        print(f'error occurred: {err}')