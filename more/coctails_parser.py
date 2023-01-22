import requests
from requests.exceptions import HTTPError
import random
import psycopg2
import time 

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


def parse_coctail(number):
    global coctail_name, coctail_tags, coctail_image, coctail_instruction, coctail_alc, coctail_ingridients, coctail_measures

    coctail_name = ''
    coctail_tags = ''
    coctail_image = ''
    coctail_instruction = ''
    coctail_alc = ''
    coctail_ingridients = []
    coctail_measures = []

    try:
        id = number
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={}'.format(id))
        response.raise_for_status()
        jsonResponse = response.json()

        if jsonResponse['drinks'] != None:  
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
    
    try:
        cur.execute(querry)
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()

    conn.commit()
    cur.close()
    conn.close()

def koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    ocena1 = round(random.uniform(3, 5), 2)
    ocena2 = round(random.uniform(3, 5), 2)
    querry = 'INSERT INTO \"koktajl\" VALUES (\'{}\', \'{}\', \'{}\',\'{}\');'.format(coctail_name,coctail_image,ocena1,ocena2) 

    try:
        cur.execute(querry)
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()

    conn.commit()
    cur.close()
    conn.close()

def kategoria_koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    querry = 'INSERT INTO \"kategoria_koktajli\" VALUES (\'{}\');'.format(coctail_alc) 
    
    try:
        cur.execute(querry)
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()
        
    conn.commit()
    cur.close()
    conn.close()
    

def kategoria_koktajli_koktajl():
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    querry = 'INSERT INTO \"kategoria_koktajli_koktajl\" VALUES (\'{}\', \'{}\');'.format(coctail_alc,coctail_name) 
    
    try:
        cur.execute(querry)
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()

    conn.commit()
    cur.close()
    conn.close()

def czynnosc():
    pass

def skladnik():
    conn = psycopg2.connect(db_url)
    for i in range(len(coctail_ingridients)):
        print(coctail_ingridients[i])
        cur = conn.cursor()
        querry = 'INSERT INTO \"skladnik\" VALUES (\'{}\');'.format(coctail_ingridients[i]) 

        try:
            cur.execute(querry)
            conn.commit()
            cur.close()    
        except Exception as err:
            print(f'error occurred: {err}')
            conn.rollback()

    conn.close()

def skladnik_przepis():
    
    conn = psycopg2.connect(db_url)
    
    for ingr_measure in range(len(coctail_ingridients)):
        cur = conn.cursor()
        try:
            querry = 'INSERT INTO \"skladnik_przepis\" VALUES (\'{}\',\'{}\',\'{}\');'.format(coctail_ingridients[ingr_measure],coctail_name,coctail_measures[ingr_measure])
        except Exception as err:
            querry = 'INSERT INTO \"skladnik_przepis\" VALUES (\'{}\',\'{}\',\'{}\');'.format(coctail_ingridients[ingr_measure],coctail_name,'  ')
            print(f'error occurred: {err}')

        try:
            cur.execute(querry)
            conn.commit()
            cur.close()
        except Exception as err:
            print(f'error occurred: {err}')
            conn.rollback()
            cur.close()
    
    conn.close()


reviews = [
    "I had the most amazing cocktail at this bar. The flavors were so unique and well-balanced. Highly recommend!",
    "I have been to a lot of bars, but this one takes the cake for best cocktails. The bartenders are so talented and creative.",
    "I had the pleasure of trying several cocktails at this establishment and was blown away by the quality and presentation of each one.",
    "I love the atmosphere at this bar and the cocktails are out of this world. I'll definitely be back for more.",
    "I had the best cocktail of my life at this bar. I can't wait to come back and try more of their creations.",
    "The bartenders here know how to make a mean cocktail. I was impressed by their knowledge and skill.",
    "I had a great time at this bar, the drinks were delicious and the service was fantastic.",
    "I was pleasantly surprised by the cocktail menu at this bar. It was unique and well-executed.",
    "The drinks here are top notch. I highly recommend the signature cocktail.",
    "I enjoyed trying different cocktails at this bar. They were all expertly crafted and delicious.",
    "I was impressed by the variety of cocktails available at this bar. I will definitely be back to try more.",
    "I had a fantastic experience at this bar. The drinks were expertly made and the service was great.",
    "I loved the creative twists on classic cocktails at this bar. They were all delicious.",
    "I had a great time trying different cocktails at this bar. They were all expertly made and had unique flavors.",
    "I was impressed by the quality of the cocktails at this bar. They were all expertly made and delicious.",
    "I had a great experience at this bar. The drinks were expertly made and the service was great.",
    "The cocktails at this bar are out of this world. I highly recommend them.",
    "I was blown away by the quality of the cocktails at this bar. They were expertly made and delicious.",
    "I had a great experience at this bar. The drinks were expertly made and the service was great.",
    "I was impressed by the creativity and skill of the bartenders at this bar. The cocktails were all delicious."
]

reviews = [x.replace("'", ' ') for x in reviews]

def user_reviews():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()

    for review in reviews:

        ocena = round(random.uniform(3, 5), 2)
        review = str(review) + str(ocena) + str(round(random.uniform(3, 5), 2))
        querry_add_odpowiedz= 'INSERT INTO \"odpowiedz\" VALUES (\'{}\');'.format(review)
        cur.execute(querry_add_odpowiedz)
        conn.commit()

        querry_add_coctail = 'INSERT INTO \"odpowiedz_koktajl\" VALUES (\'{}\', \'{}\', \'{}\');'.format(review, coctail_name, ocena)
        cur.execute(querry_add_coctail)
        conn.commit()



    cur.close()
    conn.close()

testimonials = [
    "The bouquet of flavors in the signature cocktail was truly exceptional. The balance of sweetness, acidity, and complexity was unparalleled.",
    "I had the pleasure of trying several cocktails at this establishment and was thoroughly impressed by the attention to detail and precision in each one.",
    "The use of seasonal and locally sourced ingredients in the cocktails was a delightful surprise. The flavors were truly unique and elevated.",
    "I am a true connoisseur of cocktails, and I can confidently say that the creations at this bar are some of the finest I have ever had the pleasure of trying.",
    "The mixologist's ability to pair cocktails with food was truly impressive. Each drink complemented the flavors of the dish perfectly.",
    "I was impressed by the mixologist's use of unique and unexpected ingredients in the cocktails. It added depth and interest to each drink.",
    "The presentation of the cocktails was impeccable. The attention to detail and care taken in the garnishing was evident in every sip.",
    "I had the pleasure of trying a number of cocktails, each one was expertly crafted and had its own unique and distinct flavor profile.",
    "The mixologist's knowledge of spirits and mixers was evident in the balance and complexity of each cocktail.",
    "I highly recommend trying the signature cocktail, it was a true masterpiece of flavors and aromas.",
    "The atmosphere of the bar paired beautifully with the cocktails. It was a truly elevated experience.",
    "I was impressed by the mixologist's ability to create new and exciting twists on classic cocktails. It kept the menu fresh and exciting.",
    "The service was impeccable and the bartenders were able to make suggestions based on my personal preferences.",
    "I highly recommend visiting this bar, the cocktails are truly a work of art and not to be missed.",
    "I was impressed by the mixologist's use of different techniques, such as smoking and infusing, to add depth and complexity to the cocktails.",
    "I had the pleasure of trying a number of cocktails, each one was expertly crafted and had its own unique and distinct flavor profile.",
    "The use of house-made syrups and bitters added a level of depth and complexity to the cocktails that was truly impressive.",
    "I was impressed by the mixologist's ability to pair cocktails with the specific flavors of the food. It elevated the dining experience to a whole new level.",
    "I highly recommend trying the signature cocktail, it was a true masterpiece of flavors and aromas."
]
testimonials = [x.replace("'", ' ') for x in reviews]

pseudonyms = [
    "The Shadow",
    "The Phantom",
    "The Ghost",
    "The Masked Marvel",
    "The Enigma",
    "The Mysterion",
    "The Whisperer",
    "The Illusionist",
     "The Vintner of Shadows",
    "The Oenologist of Illusion",
    "The Cellar Master of Secrets",
    "The Connoisseur of Disguise",
    "The Winemaker of Whispers",
    "The Sommelier of Mysterion",
    "The Taster of Enigma",
    "The Bouquet Blender",
    "The Vintage Veil",
    "The Aromatist of Anonymity",
    "The Cuvée Crafter",
    "The Barrel Bearer of Secrets",
    "The Fermenter of Fictions",
    "The Cellar Keeper of Pseudonyms",
    "The Cork Dork of Deception",
    "The Blend Blender of Alias",
    "The Tincture Taster of Facades",
    "The Flavor Fabricator of Fictitious Identities",
    "The Sip Siphoner of Falsehoods",
    "The Nip Napper of Nom de plumes"]


def add_sommelier():
    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()

    try: 
        for pseudonym in pseudonyms:
            querry_add_user = 'INSERT INTO \"sommelier\" VALUES (\'{}\');'.format(pseudonym)
            cur.execute(querry_add_user)
            conn.commit()

    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()
    cur.close()
    conn.close()

def sommelier_reviews():

    conn = psycopg2.connect('postgresql://joramba:admin@localhost:5432/bazy_danych')
    cur = conn.cursor()
  
    try: 
        for testimonial in testimonials:
            som = random.choice(pseudonyms)
            ocena = random.randint(2, 5)
            querry_add_coctail = 'INSERT INTO \"koktajl_sommelier\" VALUES (\'{}\', \'{}\',\'{}\',\'{}\');'.format(coctail_name, som, testimonial, ocena)
            cur.execute(querry_add_coctail)
            conn.commit()
    except Exception as err:
        print(f'error occurred: {err}')
        conn.rollback()

    cur.close()
    conn.close()

def start(start_id,amount):
    for i in range(0,amount):
        start_id+=1
        parse_coctail(start_id)
        try:
            przepis()
            koktajl()
            skladnik()
            kategoria_koktajl()
            kategoria_koktajli_koktajl()
            skladnik_przepis()
            user_reviews()
            add_sommelier()
            sommelier_reviews()
            
        except Exception as err:
            print(f'error occurred: {err}')

start(11000,25)
# start(12560,30)


