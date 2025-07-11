import google.generativeai as genai

# --- CONFIGURATION ---
# IMPORTANT: Replace with your actual Google API key.
GOOGLE_API_KEY = "AIzaSyDsXEFJegJje339LqlYn8bs1XzUJMdWrD4"

# Configure the genai library
genai.configure(api_key=GOOGLE_API_KEY)


# --- THE AI FUNCTION ---
def get_ai_summary(text_to_summarize):
    """
    Calls the Google Gemini API to summarize text.
    """
    try:
        # This is the correct, working model name for your key.
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"Summarize the following client inquiry in one single sentence: {text_to_summarize}"
        
        print("...Processing with Google AI...")
        response = model.generate_content(prompt)
        
        return response.text

    except Exception as e:
        print(f"---! An error occurred while calling the API: {e} !---")
        return "An error occurred while contacting the AI."


# --- THE MAIN PART OF THE PROGRAM ---
print("Welcome to LexiFlow v0.1!")
print("Please paste the client email and press Enter twice.")

user_input_lines = []
while True:
    try:
        line = input()
    except EOFError:
        break
    if not line:
        break
    user_input_lines.append(line)

client_email = "\n".join(user_input_lines)

if client_email:
    summary = get_ai_summary(client_email)
    
    print("\n--- FINAL AI Summary ---")
    print(summary)
else:
    print("No input received. Exiting.")