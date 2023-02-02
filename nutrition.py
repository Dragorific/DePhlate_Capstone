import json
with open(r"food_database.json", encoding="utf8") as file:
    fooddata = json.load(file)

def get_food_info(query):
    serving_size = fooddata['Foods'][query]['servingSize']
    sodium = fooddata['Foods'][query]['labelNutrients']['sodium']['value']
    carbs = fooddata['Foods'][query]['labelNutrients']['carbohydrates']['value']
    sugar = fooddata['Foods'][query]['labelNutrients']['sugars']['value']
    protein = fooddata['Foods'][query]['labelNutrients']['protein']['value']
    calories = fooddata['Foods'][query]['labelNutrients']['calories']['value']

    print("The nutritional breakdown for ",query," is: Sodium: ",sodium,"mg, Carbohydrates: ",carbs,"g, Sugar: ",sugar,"g, Protein: ",protein,"g, Calories: ",calories," per a single serving of ",serving_size,"g sourced from the USDA FoodData database")

query = "APPLE"
get_food_info(query)