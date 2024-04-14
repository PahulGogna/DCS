import google.generativeai as genai
import os
from PIL import Image
# from config import config
from rembg import remove

genai.configure(api_key=os.environ["googleApiKey"])
model = genai.GenerativeModel('gemini-pro')
img_model = genai.GenerativeModel('gemini-pro-vision')

def ask(query) -> str:
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return e

def rate_img(img):
    try:
        result = img_model.generate_content([
        "give a score out of 10, how good is this image for an ecommerce website? :", img])
        return result.text
    except Exception as e:
        return e

def remove_background(img):
    return remove(img)  #image object