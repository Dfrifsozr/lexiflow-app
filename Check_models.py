# check_models.py
# This script will list the AI models available for your API key.

import google.generativeai as genai

# --- IMPORTANT ---
# Paste your Google API key here
GOOGLE_API_KEY = "AIzaSyDsXEFJegJje339LqlYn8bs1XzUJMdWrD4"

try:
    genai.configure(api_key=GOOGLE_API_KEY)

    print("--- Finding available models for your API key... ---")
    
    found_models = False
    for model in genai.list_models():
      # We only care about models that support the 'generateContent' method
      if 'generateContent' in model.supported_generation_methods:
        print(f"Model found: {model.name}")
        found_models = True

    if not found_models:
        print("\n--- No models supporting 'generateContent' were found for this API key. ---")
        print("This could be an issue with the key or account permissions.")

except Exception as e:
    print(f"\n---! An error occurred while trying to list models: {e} !---")
    print("Please double-check that your API key is correct and valid.")