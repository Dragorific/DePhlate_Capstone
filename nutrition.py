import json
with open(r"user_data/food_database.json", encoding="utf8") as file:
    fooddata = json.load(file)

def get_food_info(query):
    query = query.upper()
    serving_size = fooddata['Foods'][query]['servingSize']
    calories = fooddata['Foods'][query]['labelNutrients']['calories']['value']
    return(calories, serving_size)

def get_macro_info(query):
    query = query.upper()
    serving_size = fooddata['Foods'][query]['servingSize']
    try:
        sodium = fooddata['Foods'][query]['labelNutrients']['sodium']['value']
    except:
        sodium = 1
    try:
        carbs = fooddata['Foods'][query]['labelNutrients']['carbohydrates']['value']
    except:
        carbs = 1
    try:
        sugar = fooddata['Foods'][query]['labelNutrients']['sugars']['value']
    except:
        sugar = 1
    try:
        protein = fooddata['Foods'][query]['labelNutrients']['protein']['value']
    except:
        protein = 1
    
    return(serving_size,sodium/1000,carbs,sugar,protein)