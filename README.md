## Problem2: APP for Recipe
### Testing the API
The API using tools like Postman can be used to test by visiting:  

- for ingredients: http://127.0.0.1:8000/api/ingredients/
- for recipes: http://127.0.0.1:8000/api/recipe/ 
- for recipe-ingredient relationships http://127.0.0.1:8000/api/recipeingredient/

### Features:
The Django app has the features to:
- Add, Remove and Update an ingredient
- Add, Remove and Update a recipe
- Retrieve the recipe from a file and update the database
- Creating relation between the recipe and available ingredients based on the ingredients

### API GET response for ingredinets:
```
[
    {
        "id": 1,
        "name": "Sugar",
        "quantity": "5.00",
        "unit": "kg",
        "expiration_date": "2024-12-25",
        "cost": null,
        "tags": null
    }]
```
### API GET response for recipe:
```
  {
        "id": 3,
        "ingredients": [
            {
                "id": 1,
                "quantity": "200.00",
                "unit": "grams",
                "recipe": 3,
                "ingredient": 4
            },
            {
                "id": 2,
                "quantity": "2.00",
                "unit": "units",
                "recipe": 3,
                "ingredient": 5
            },
            {
                "id": 3,
                "quantity": "300.00",
                "unit": "ml",
                "recipe": 3,
                "ingredient": 6
            }
```
