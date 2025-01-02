import google.generativeai as genai
from PIL import Image

from config.config import Config

genai.configure(api_key = Config.API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def send_to_llm(image_path : str) -> tuple[str, str]:
    print("Sending to LLM...")
    try:
        image = Image.open(image_path)
        response = model.generate_content([Config.prompt_for_llm, image])
        
        print("LLM responded Successfully")
        return "Success", response.text
    
    except Exception as e:
        return "Failure", str(e)