import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Using Llama 3.3 70B for deep, high-quality, nuanced interpretation
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_profile_interpretation(profile_data: dict, language: str = "English") -> str:
    """
    Weaves calculated numbers into a fluid, holistic life roadmap.
    Ensures the response matches the user's preferred language.
    """
    
    system_prompt = (
        f"You are an expert, empathetic spiritual guide and master numerologist. "
        f"Your job is to weave five distinct numerological data points into a cohesive, "
        f"deeply personalized profile narrative. Avoid generic platitudes.\n\n"
        f"CRITICAL: You must write the entire analysis entirely in the requested language: {language}.\n\n"
        f"Focus on the tensions, conflicts, and harmonies between their numbers "
        f"(e.g., how a reserved Life Path interacts with an expressive Expression number). "
        f"Keep the tone grounded, self-reflective, psychological, and inspiring. "
        f"Do not predict the future; offer archetypal insight for self-discovery."
    )
    
    user_payload = f"""
    Please generate a custom reading for a profile with these parameters:
    - Life Path Number: {profile_data['life_path']}
    - Expression Number: {profile_data['expression']}
    - Soul Urge Number: {profile_data['soul_urge']}
    - Personality Number: {profile_data['personality']}
    - Birthday Number: {profile_data['birthday_number']}
    
    Structure the response layout with:
    1. A comprehensive 3-paragraph synthesis blending these forces together.
    2. Three distinct Strengths.
    3. Three hidden Blind Spots/Challenges.
    4. One focal Core Advice takeaway for their current chapter.
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating interpretation: {str(e)}"