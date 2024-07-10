import os
import openai
import config
import requests
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO

def extract_and_parse_menu_items(input_source):
    openai.api_key = config.OPENAI_API_KEY
    images = []

    if input_source.lower().endswith('.pdf'):
        images = convert_from_path(input_source)
    elif input_source.lower().endswith(('.jpg', '.jpeg', '.png')):
        images.append(Image.open(input_source))

    # use a openbrowser instead of downloading as pdf     
    elif input_source.startswith('http'):
        response = requests.get(input_source)
        if response.headers['Content-Type'] == 'application/pdf':
            pdf_path = 'temp_menu.pdf'
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            images = convert_from_path(pdf_path)
            os.remove(pdf_path)
        else:
            images.append(Image.open(BytesIO(response.content)))
    else:
        print("Unsupported file format")
        return []

    try:
        text = ""
        for image in images:
            response = openai.Image.create(
                model="gpt-4o",
                file=image.tobytes(),
                purpose="answers"
            )
            text += response['data']['text'] + "\n"

        prompt = f"Extract the menu items and their prices from the following text:\n\n{text}\n\nFormat the output as 'Item Name - Price'."
        completion_response = openai.Completion.create(
            engine="gpt-3.5-turbo-0125",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.0001,
        )
        return completion_response.choices[0].text.strip().split('\n')
    except Exception as e:
        print(f"Error using GPT-3.5 for OCR and parsing: {e}")
        return []
