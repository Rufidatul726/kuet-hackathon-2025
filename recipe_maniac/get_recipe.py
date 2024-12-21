from ingredients.models import Recipe, Ingredient, RecipeIngredient

def load_recipes_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split recipes by separator
    recipes = content.split('---')

    for recipe_data in recipes:
        if recipe_data.strip():
            lines = recipe_data.strip().split('\n')
            title = lines[0].split('Title: ')[1]
            description = lines[1].split('Description: ')[1]

            # Parse ingredients
            ingredients = {}
            ingredients_section = lines[3:-2]  # Skip title, description, and instructions
            for line in ingredients_section:
                if line.startswith('- '):
                    item = line[2:].split(':')
                    ingredient_name = item[0].strip()
                    quantity_unit = item[1].strip().split(' ')
                    quantity = float(quantity_unit[0])
                    unit = ' '.join(quantity_unit[1:])
                    ingredients[ingredient_name] = (quantity, unit)

            # Parse instructions
            instructions = '\n'.join(lines[-2:])

            # Create Recipe
            recipe = Recipe.objects.create(
                title=title,
                description=description,
                instructions=instructions
            )

            # Add ingredients
            for ingredient_name, (quantity, unit) in ingredients.items():
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity,
                    unit=unit
                )

# Provide the path to the text file
file_path = 'recipe_maniac\pancake.txt'
load_recipes_from_file(file_path)