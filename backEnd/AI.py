import google.generativeai as genai
import os
from PIL import Image
# from config import config
from rembg import remove


genai.configure(api_key=os.environ["googleApiKey"])
model = genai.GenerativeModel('gemini-pro')
# img_model = genai.GenerativeModel('gemini-pro-vision')

def ask(query) -> str:
    try:
        response = model.generate_content(query)
        print(response.text)
        return response.text
    except Exception as e:
        return e
    
def post_check(post) -> str:

    try:
        ans = ask(f'data : {post["data"]}, tag : {post["tag"]}, give me a score between 0 and 10, ONE NUMBER ONLY PLEASE, based on the following parameters: 1. is this text suitable to be on a disaster crowd sourcing website (if it is not suitable give a 0), 2. has this happened in the place provided in the tag(if not, give a 0),3. could this be an update to something that has recently happened in the area provided in the tag (if not, give a 0),4. how likely is it that this is a real event (if it is not likely, give a 0), 5.how much information is provided in the post (if there is no information, give a 0), 6. could this post be a plee for help (if yes, give a 10)')
    except Exception as e:
        print(e)
        return e
    return True, int(ans.title())


# ans = ask(f'data : volcano, tag : philipenes, give me a score between 0 and 10, ONE NUMBER ONLY PLEASE and a valid for all link related to this event from indianexpress, seperated by spaces, based on the following parameters: 1. is this text suitable to be on a disaster crowd sourcing website (if it is not suitable give a 0), 2. has this happened in the place provided in the tag(if not, give a 0),3. could this be an update to something that has recently happened in the area provided in the tag (if not, give a 0),4. how likely is it that this is a real event (if it is not likely, give a 0), 5.how much information is provided in the post (if there is no information, give a 0), 6. could this post be a plee for help (if yes, give a 10)')

# print([ob for ob in ans.split()])
