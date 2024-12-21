import os
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

from chat import process_chatbot_input, recommend_recipe
from recipes.get_recipies_from_file import parse_recipe_file

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('kitchen_buddy.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Add Ingredient Endpoint
@app.route('/ingredients', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    name = data['name']
    quantity = data['quantity']
    unit = data['unit']
    expiration_date = data.get('expiration_date')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Ingredients (name, quantity, unit, expiration_date)
        VALUES (?, ?, ?, ?)
    ''', (name, quantity, unit, expiration_date))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Ingredient added successfully"}), 201

# Update Ingredient Endpoint
@app.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    data = request.get_json()
    quantity = data.get('quantity')
    expiration_date = data.get('expiration_date')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Ingredients
        SET quantity = ?, expiration_date = ?, last_updated = ?
        WHERE ingredient_id = ?
    ''', (quantity, expiration_date, datetime.now(), ingredient_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Ingredient updated successfully"}), 200

# Get All Ingredients Endpoint
@app.route('/ingredients', methods=['GET'])
def get_all_ingredients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ingredients')
    ingredients = cursor.fetchall()
    conn.close()

    return jsonify([dict(ingredient) for ingredient in ingredients]), 200

# Add Recipe Endpoint
@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    name = data['name']
    ingredients = data['ingredients']  # Ingredients in JSON format
    instructions = data['instructions']
    tags = data.get('tags')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Recipes (name, ingredients, instructions, tags)
        VALUES (?, ?, ?, ?)
    ''', (name, str(ingredients), instructions, tags))
    conn.commit()
    conn.close()

    return jsonify({"message": "Recipe added successfully"}), 201


# Endpoint to upload and parse the recipe file
@app.route('/upload_recipes', methods=['POST'])
def upload_recipes():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Save the uploaded file temporarily
    filename = os.path.join(upload_folder, file.filename)
    file.save(filename)

    # Read and parse the file
    with open(filename, 'r') as f:
        file_content = f.read()
        recipes = parse_recipe_file(file_content)
    
    # Insert the parsed recipes into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for recipe in recipes:
        cursor.execute('''
            INSERT INTO Recipes (name, ingredients, instructions, tags)
            VALUES (?, ?, ?, ?)
        ''', (recipe['name'], str(recipe['ingredients']), "\n".join(recipe['instructions']), ", ".join(recipe['tags'])))
    
    conn.commit()
    conn.close()
    
    # Delete the temporary file
    os.remove(filename)

    return jsonify({"message": "Recipes uploaded and stored successfully"}), 200

@app.route('/recipes', methods=['GET'])
def get_all_reccipies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Recipes')
    recipes = cursor.fetchall()
    conn.close()

    return jsonify([dict(recipe) for recipe in recipes]), 200

@app.route('/chatbot', methods=['POST'])
def chatbot_interaction():
    user_input = request.json.get("user_input")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Based on the user's preference, recommend a recipe
    user_preference = process_chatbot_input(user_input)
    available_ingredients = request.json.get("available_ingredients", "")

    # If available ingredients are not provided, use an empty string
    recommended_recipe = recommend_recipe(available_ingredients)

    if recommended_recipe:
        recipe_response = {
            "recipe_name": recommended_recipe['name'],
            "ingredients": recommended_recipe['ingredients'],
            "instructions": recommended_recipe['instructions']
        }
    else:
        recipe_response = {"message": "Sorry, no matching recipe found based on your ingredients."}

    return jsonify({
        "chatbot_reply": chatbot_reply,
        "user_preference": user_preference,
        "recommended_recipe": recipe_response
    })


if __name__ == '__main__':
    app.run(debug=True)
