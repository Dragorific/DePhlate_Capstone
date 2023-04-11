import matplotlib.pyplot as plt
import numpy as np
import json
from nutrition import get_macro_info

#Function for converting pie chart percents into gram values to put in the chart
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:,}g'.format(v=val)
    return my_format

def gen_plots():
    breakfast_cals = 0
    lunch_cals = 0
    dinner_cals = 0
    sodium_total = 0
    carbs_total = 0
    sugar_total = 0
    protein_total = 0

    #reading food items stored in json
    with open('user_data/breakfast.json') as infile:
        breakfast = json.load(infile)
    with open('user_data/lunch.json') as infile:
        lunch = json.load(infile)
    with open('user_data/dinner.json') as infile:
        dinner = json.load(infile)

    #calculating macros and total calories in each meal
    for food in breakfast:
        breakfast_cals += breakfast[food]
        serving_size, sodium, carbs, sugar, protein = get_macro_info(food)
        weight = breakfast[food]
        sodium_total += sodium*(weight/serving_size)
        carbs_total += carbs*(weight/serving_size)
        sugar_total += sugar*(weight/serving_size)
        protein_total += protein*(weight/serving_size)
    for food in lunch:
        lunch_cals += lunch[food]
        serving_size, sodium, carbs, sugar, protein = get_macro_info(food)
        weight = lunch[food]
        sodium_total += sodium*(weight/serving_size)
        carbs_total += carbs*(weight/serving_size)
        sugar_total += sugar*(weight/serving_size)
        protein_total += protein*(weight/serving_size)
    for food in dinner:
        dinner_cals += dinner[food]
        serving_size, sodium, carbs, sugar, protein = get_macro_info(food)
        weight = dinner[food]
        sodium_total += sodium*(weight/serving_size)
        carbs_total += carbs*(weight/serving_size)
        sugar_total += sugar*(weight/serving_size)
        protein_total += protein*(weight/serving_size)
    calories = np.array([0,breakfast_cals,breakfast_cals + lunch_cals,breakfast_cals + lunch_cals + dinner_cals])
    calories_each = np.array([breakfast_cals,lunch_cals,dinner_cals])

    time = np.array([0, 1, 2, 3])
    timetext = [1,2,3]
    timelabels = ['Breakfast','Lunch','Dinner']

    #line graph for total calorie consumption throughout the die
    plt.plot(time,calories,color='y')
    plt.axhline(y = 2000, color = 'r', linestyle = '-')
    plt.ylabel('Calories')

    #plot formatting
    ax = plt.gca()
    ax.grid(axis='y')
    ax.spines[['right', 'top']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    #bar graph for each individual meal
    ax.bar(timetext,calories_each)
    plt.xticks(timetext,timelabels)

    plt.savefig('user_data/calories.png', transparent=True)
    plt.clf()

    #pie chart of macros
    label = ['sodium', 'carbs', 'sugar', 'protein']
    data = [sodium_total,carbs_total,sugar_total,protein_total]
    patches, texts, autotexts = plt.pie(data, labels = label, autopct = autopct_format(data))
    for i, patch in enumerate(patches):
        texts[i].set_color('white')
    plt.savefig('user_data/macros.png', transparent=True)
