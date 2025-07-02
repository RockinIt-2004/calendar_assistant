from google.generativeai import list_models
import google.generativeai as genai

genai.configure(api_key="AIzaSyC5z9Vjc8X7JgGQ1R5ISc-tHJniKzowefo")

for model in list_models():
    print(model.name, "->", model.supported_generation_methods)
