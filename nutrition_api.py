import json
import requests

# This function returns the fdc Id
def get_fdc_id(api, parameters):
    response = requests.get(f"{api}", params=parameters)
    if response.status_code == 200:
        print("successfully fetched the fdc ID with parameters provided")
        return(response.json()['foods'][0]['fdcId'])
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")

# This function prints the item info based on the fdc Id
def get_food_info(api, parameters):
    response = requests.get(f"{api}", params=parameters)
    if response.status_code == 200:
        print("sucessfully fetched the food info with parameters provided")
        json_body = response.json()
        
        name = json_body['description']
        calories = json_body['labelNutrients']['calories']['value']
        print("The total calories for", name, "are", calories, "sourced from the USDA FoodData database.")
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")

# Make the first request to obtain the fdc Id of a string query item
api_id = "https://api.nal.usda.gov/fdc/v1/foods/search"
params = {
    "api_key":"DEMO_KEY",
    "query":"pretzel"      # This needs to change to support what our detection API gets
}

fdcId = get_fdc_id(api_id, params)

# Make a new request with the fdc Id to get caloric information
api_food = "https://api.nal.usda.gov/fdc/v1/food/"+str(fdcId)    # This can be changed to something nicer
params = {
    "api_key":"DEMO_KEY"    
}

get_food_info(api_food, params)
