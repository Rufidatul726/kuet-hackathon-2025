import random
from flask import jsonify, request
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

from index import get_db_connection

tokenizer = AutoTokenizer.from_pretrained("t5-base")
model = AutoModelForCausalLM.from_pretrained("t5-base")
chatbot = pipeline("conversational", model=model, tokenizer=tokenizer)

def recommend_recipe(available_ingredients):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Search for recipes that match available ingredients
    query = f"SELECT name, ingredients, instructions FROM Recipes"
    cursor.execute(query)
    recipes = cursor.fetchall()

    recommended_recipes = []

    for recipe in recipes:
        ingredients = recipe['ingredients'].lower().split(",")
        available_ingredients_set = set(available_ingredients.lower().split(","))
        if set(ingredients).intersection(available_ingredients_set):
            recommended_recipes.append({
                'name': recipe['name'],
                'ingredients': recipe['ingredients'],
                'instructions': recipe['instructions']
            })

    conn.close()

    if recommended_recipes:
        return random.choice(recommended_recipes)  # Recommend a random recipe from the match
    else:
        return None

# Function to process chatbot input and understand user preferences
def process_chatbot_input(user_input):
    # Process the chatbot input for preferences like "I want something sweet today"
    user_input = user_input.lower()

    if "sweet" in user_input or "dessert" in user_input:
        return "sweet"
    elif "spicy" in user_input:
        return "spicy"
    elif "salty" in user_input:
        return "salty"
    else:
        return "any"
    
# Function to interact with the chatbot
def chatbot_interaction(user_input):
    chat_history = chatbot(user_input)
    chatbot_reply = chat_history[0]['generated_text']

    if not chatbot_reply:
        return jsonify({"error": "Chatbot failed to reply"}), 500
    
    return jsonify({"chatbot_reply": chatbot_reply}), 200
