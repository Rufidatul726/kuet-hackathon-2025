import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('kitchen_buddy.db')
cursor = conn.cursor()

# Create Ingredients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    unit TEXT NOT NULL,
    expiration_date DATE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# Create Recipes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Recipes (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,  -- Store ingredients as a JSON string
    instructions TEXT NOT NULL,
    tags TEXT
);
''')

# Create Shopping History table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ShoppingHistory (
    shopping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    quantity TEXT NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients (ingredient_id)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")