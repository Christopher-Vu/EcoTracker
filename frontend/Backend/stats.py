import sqlite3
from flask import render_template_string

def generate_stats(email):
    stat_string = ""

    conn = sqlite3.connect('frontend/Backend/userdata.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {email}")
    results = cursor.fetchall()

    for row in results:
        stat_string = stat_string + f'→ {row[0]} (Data was taken over a {row[1]} day period):\nTotal Carbon Footprint: {row[2]} Tons.\nTheorertical Yearly Foorprint: {row[3]} Tons.\nThis Theoretical Footprint is {row[4]} {row[5]}.\n\n'

    cursor.close()
    conn.close()

    return render_template_string(stat_string)

def problem_area(goods, food, water, energy, transport):
    area = max([goods, food, water, energy, transport])

    if goods == area: return "goods", """Your biggest problem area is purchased goods. One of the best ways to reduce the 
    carbon footprint of purchased goods is to reduce the amount of waste that you produce. This can be achieved by purchasing 
    products with minimal packaging or by choosing products that can be recycled. Additionally, buying locally produced goods 
    can help to reduce the carbon footprint associated with transportation, as well as support local businesses."""
    if food == area: return "food", """Your biggest problem area is food. One of the easiest ways to reduce the carbon footprint 
    of your food consumption is to eat a plant-based diet, even if only for 1-2 days a week. Animal agriculture is a significant 
    contributor to greenhouse gas emissions, so reducing or eliminating meat and dairy products from your diet can have a significant 
    impact. Choosing organic and locally produced foods can also help to reduce the carbon footprint associated with food 
    production and transportation."""
    if water == area: return "water", """Your biggest problem area is water. Conserving water can help to reduce the energy needed 
    for pumping and treating water, as well as reduce the carbon footprint associated with water treatment. Simple actions like 
    fixing leaky faucets, taking shorter showers, and using a low-flow toilet can all help to conserve water. Additionally, 
    installing water-efficient appliances, such as a dishwasher or washing machine, can also help to reduce water consumption 
    and the associated carbon footprint."""
    if energy == area: return "energy", """Your biggest problem area is energy. Reducing energy consumption can have a significant 
    impact on reducing carbon emissions. One of the easiest ways to reduce energy consumption is to switch to energy-efficient 
    lighting, such as LED bulbs. Installing a programmable thermostat can also help to reduce energy consumption by automatically 
    adjusting the temperature when you are not at home. Additionally, investing in renewable energy sources, such as solar panels 
    or wind turbines, can help to reduce your reliance on fossil fuels and further reduce your carbon footprint."""
    return "transport", """Your biggest problem area is transport. Reducing the amount of driving you do can have a significant 
    impact on your carbon footprint. Walking, cycling, or taking public transportation are all more sustainable options than driving 
    alone. If driving is necessary, choosing a fuel-efficient vehicle or carpooling with others can help to reduce the carbon 
    emissions associated with transportation. Additionally, choosing a destination closer to home for vacations or leisure activities 
    can also help to reduce the carbon footprint associated with travel."""
