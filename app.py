from flask import Flask, render_template, request
import google.generativeai as genai
import os  # Import the 'os' library to interact with the operating system
from dotenv import load_dotenv  # Import the tool from our new library

# --- SETUP ---
# This line reads the .env file and loads the variables into the environment
load_dotenv()


# --- AI ENGINE ---
def process_inquiry(text_to_summarize, scheduling_link):
    """
    Calls the Google Gemini API using a secure API key from the environment.
    """
    try:
        # --- SECURE KEY HANDLING ---
        # Get the API key from the environment variables.
        # os.getenv() is the standard way to read these.
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        # --- The hardcoded key is now GONE ---
        
        model = genai.GenerativeModel('gemini-2.0-flash-lite')

        # --- Prompts remain the same ---
        summary_prompt = f"Summarize the following client inquiry in one single sentence: {text_to_summarize}"
        summary_response = model.generate_content(summary_prompt)
        summary = summary_response.text

        draft_prompt = f"""
        You are a professional and efficient administrative assistant for a law firm.
        Your task is to draft a polite reply to the following client inquiry.
        The email should have three parts:
        1. Acknowledge the client's situation briefly.
        2. State that the next step is a complimentary 15-minute consultation to learn more.
        3. Provide this scheduling link for the client to use: {scheduling_link}
        Keep the tone professional and helpful. Do not give any legal advice.
        Do not use placeholders.
        Here is the client's email:
        ---
        {text_to_summarize}
        ---
        """
        draft_response = model.generate_content(draft_prompt)
        draft = draft_response.text

        return {'summary': summary, 'draft': draft}

    except Exception as e:
        print(f"---! An error occurred: {e} !---")
        # Return a more specific error if the key was the issue
        if "GOOGLE_API_KEY not found" in str(e):
             return {'summary': 'Configuration Error.', 'draft': 'The Google API key is missing. Please check server configuration.'}
        return {'summary': 'An error occurred.', 'draft': 'Could not generate draft due to an API error.'}

# --- FLASK APP (No changes below this line) ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text_from_form = request.form['client_email_text']
    link_from_form = request.form['scheduling_link']

    if not text_from_form.strip():
        error_message = "Please paste the client's email inquiry. The text box cannot be empty."
        return render_template('index.html', error=error_message)

    results = process_inquiry(text_from_form, link_from_form)
    return render_template('result.html', result_data=results)
