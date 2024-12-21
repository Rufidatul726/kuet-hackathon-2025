from transformers import pipeline

text_generator = pipeline("text-generation", model="t5-base", tokenizer="t5-base")

def process_recipe_with_llm(file_content):
    # Call OpenAI GPT model to parse and extract ingredients and instructions
    response = text_generator(
        model="gpt-3.5-turbo",  # Use GPT-3.5 or GPT-4 depending on your API access
        prompt=f"Extract ingredients and instructions from the following recipe text and return them separately. \n\n{file_content}",
        max_tokens=1500,
        temperature=0.5
    )

    # Extracted text from the response
    processed_text = response['choices'][0]['text'].strip()
    return processed_text


# Function to parse the recipe file
def parse_recipe_file(file_content):
    recipes = []

    response = process_recipe_with_llm(file_content)

    
    print(response)

    return recipes
