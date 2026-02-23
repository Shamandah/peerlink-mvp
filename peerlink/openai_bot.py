import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("OPENAI_API_KEY")) # It will use your AIza... key

def generate_ai_reply(question: str) -> str:
    try:
        # Set up the model with a soft persona
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "You are a compassionate MKU peer mentor. Provide a soft dialogue. "
                "Use warm, gentle, and validating language. Acknowledge feelings first. "
                "Keep responses human, concise, and supportive. Avoid robotic lists."
            )
        )

        # Generate response
        response = model.generate_content(question)
        
        return response.text

    except Exception as e:
        # A soft error message for the user
        return f"I'm so sorry, I'm having a little trouble connecting right now. Let's try again in a moment."