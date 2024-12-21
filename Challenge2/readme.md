# Kitchen Buddy

Kitchen Buddy is a backend system powered by a Large Language Model (LLM) designed to help users manage their ingredients and suggest recipes based on the ingredients they have at home. Users can interact with a chatbot that understands their preferences (e.g., "I want something sweet today") and recommends recipes accordingly.

## Features:
- **Recipe Upload**: Upload recipe files and store the recipes in a database.
- **Chatbot Interaction**: A conversational chatbot to interact with users and recommend recipes based on their preferences and available ingredients.
- **Recipe Recommendations**: The system suggests recipes based on the ingredients available at home.

## Requirements:
- Python 3.6+
- Flask
- Transformers (for LLM)
- Torch
- SQLite

## Installation:

### Step 1: Install Dependencies
To install the necessary libraries, run the following command:

```bash
pip install transformers torch flask sqlite3
```

### Step 2: Set Up the Database
Before using the application, you need to create the database. Use the following Python script to create the SQLite database and tables:

```python
import sqlite3

conn = sqlite3.connect('kitchen_buddy.db')
c = conn.cursor()

# Create Recipes table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS Recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                ingredients TEXT,
                instructions TEXT)''')

conn.commit()
conn.close()
```

### Step 3: Run the Application

Run the Flask application using the following command:

```bash
python index.py
```

The app will start a development server on `http://127.0.0.1:5000`.

## API Endpoints:

### 1. **Upload Recipes**

- **Endpoint**: `/upload_recipes`
- **Method**: `POST`
- **Description**: Upload a `.txt` recipe file containing recipes to be stored in the database.
- **Request Body**:
  - A file upload with a `.txt` recipe file.
- **Response**:
  - `200 OK`: If the recipe file is uploaded and stored successfully.
  - `400 Bad Request`: If no file is uploaded or the file format is incorrect.
- **Example**:
  ```bash
  curl -X POST -F "file=@my_fav_recipes.txt" http://127.0.0.1:5000/upload_recipes
  ```

---

### 2. **Chatbot Interaction and Recipe Recommendation**

- **Endpoint**: `/chatbot`
- **Method**: `POST`
- **Description**: Interact with the chatbot to get recommendations based on user preferences (e.g., "I want something sweet today") and available ingredients.
- **Request Body**:
  - `user_input`: The user's text input to interact with the chatbot (e.g., "I want something sweet today").
  - `available_ingredients`: A comma-separated list of ingredients the user has at home (e.g., "sugar, cocoa powder, eggs, butter").
- **Response**:
  - `200 OK` with a JSON response containing:
    - `chatbot_reply`: The chatbot’s response based on the user input.
    - `user_preference`: The detected user preference (e.g., "sweet", "spicy", etc.).
    - `recommended_recipe`: A recommended recipe based on the ingredients the user has at home.
  
  Example Response:
  ```json
  {
    "chatbot_reply": "What kind of sweet dish would you like to make today?",
    "user_preference": "sweet",
    "recommended_recipe": {
      "recipe_name": "Chocolate Cake",
      "ingredients": "sugar, cocoa powder, eggs, flour, butter",
      "instructions": "Mix all ingredients and bake at 350°F for 30 minutes."
    }
  }
  ```

- **Example**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{
    "user_input": "I want something sweet today",
    "available_ingredients": "sugar, cocoa powder, eggs, flour, butter"
  }' http://127.0.0.1:5000/chatbot
  ```

---

## How it Works:

### 1. **Recipe Upload**:
   - When a user uploads a `.txt` file via the `/upload_recipes` endpoint, the file is read and parsed to extract the ingredients and instructions. The recipe is then stored in the `Recipes` table in the database.
   
### 2. **Chatbot Interaction**:
   - The chatbot listens to the user's input (e.g., "I want something sweet today") and identifies their preference (e.g., "sweet", "spicy", etc.). 
   - It then uses the `recommend_recipe()` function to filter and recommend recipes that match the user's available ingredients.
   - The system returns a recipe based on the available ingredients, or a message indicating no match is found.

### 3. **Recipe Recommendations**:
   - The system searches the database for recipes that match the available ingredients, and if a match is found, it returns a recipe from the database.
   - The system can handle different user preferences like "sweet", "spicy", or "salty" and recommend appropriate recipes.

## Example Usage:

1. **Uploading a Recipe**:

   You can upload a recipe in a `.txt` file format, which could look like this:

   ```
   Recipe Name: Chocolate Cake
   Ingredients: sugar, cocoa powder, eggs, flour, butter
   Instructions: Mix all ingredients and bake at 350°F for 30 minutes.
   ```

2. **Interacting with the Chatbot**:

   Send a request to the `/chatbot` endpoint with the user's preference and available ingredients:

   ```json
   {
     "user_input": "I want something sweet today",
     "available_ingredients": "sugar, cocoa powder, eggs, flour, butter"
   }
   ```

   The chatbot will process the input and respond with the most appropriate recipe based on the user's ingredients.

## Notes:
- The system uses the **t5-base** model from Hugging Face for chatbot functionality.
- It is important to have a `.txt` recipe file formatted correctly for parsing and storing in the database.
- Recipes are recommended based on the ingredients available at home.
