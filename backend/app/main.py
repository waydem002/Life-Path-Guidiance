from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import traceback
from dotenv import load_dotenv
from groq import Groq

# Import application services
from app.numerology import generate_full_profile
from app.rag_service import load_rag_guidelines
from app.database import (
    init_db, 
    get_cached_profile, 
    save_profile_to_cache, 
    fetch_profiles_history
)
from app.pdf_service import generate_blueprint_pdf

load_dotenv()

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Request Schemas
class ProfileRequest(BaseModel):
    name: Optional[str] = "Anonymous / Unspecified"
    dob: Optional[str] = None
    birth_time: Optional[str] = None
    birth_location: Optional[str] = None
    age: Optional[str] = None
    focus_area: Optional[str] = "General Life Path & Guidance"
    language: Optional[str] = "English"

class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "English"
    context: Optional[str] = ""

@app.post("/api/generate-profile")
@app.post("/api/energy-profile")
async def generate_energy_profile(request: ProfileRequest):
    try:
        clean_name = (request.name or "").strip() or "Anonymous User"
        clean_dob = (request.dob or "").strip()
        clean_time = (request.birth_time or "").strip() or "Unspecified"
        clean_loc = (request.birth_location or "").strip() or "Unspecified"
        clean_age = (request.age or "").strip() or "Unspecified"
        clean_focus = (request.focus_area or "").strip() or "General Life Path & Guidance"
        target_lang = (request.language or "").strip() or "English"

        # 1. Cache Check
        if clean_dob:
            cached_interpretation = get_cached_profile(clean_name, clean_dob, target_lang, clean_focus)
            if cached_interpretation:
                print(f"[CACHE HIT] Serving existing profile reading for '{clean_name}' (Focus: {clean_focus})")
                return {"interpretation": cached_interpretation}

        print(f"[CACHE MISS] Generating new reading for '{clean_name}' - Focus: {clean_focus}")

        # 2. Numerology Calculation
        numbers = None
        if clean_dob:
            try:
                numbers = generate_full_profile(clean_name, clean_dob)
            except Exception as num_err:
                print(f"[NUMEROLOGY NOTICE] Calculation skipped/failed: {num_err}")

        systemic_guidelines = load_rag_guidelines()

        # 3. Dynamic Lens Prompt
        system_prompt = (
            f"You are an expert systemic life path and energy profile guide.\n\n"
            f"PRIMARY CORE LENS / FOCUS AREA: *** {clean_focus.upper()} ***\n"
            f"USER METRICS: Name: {clean_name}, DOB: {clean_dob or 'N/A'}, Time: {clean_time}, Location: {clean_loc}, Age: {clean_age}.\n"
            f"CALCULATED METRICS: {numbers if numbers else 'N/A'}\n\n"
            f"STRICT CONTENT FOCUS MANDATE:\n"
            f"You MUST interpret ALL life path metrics, soul urge numbers, and expression details STRICTLY through the lens of '{clean_focus}'.\n"
            f"- If Focus Area is 'Love & Relationships': Discuss romantic dynamics, partner communication, emotional triggers, and relational patterns.\n"
            f"- If Focus Area is 'Personal Growth & Spiritual Path': Focus exclusively on soul lessons, spiritual evolution, inner blockages, and higher purpose.\n"
            f"- If Focus Area is 'Career & Life Purpose': Focus on leadership skills, professional trajectory, business execution, and wealth generation.\n"
            f"- If Focus Area is 'Health & Energy Alignment': Focus on physical vigor, stress management, energy balance, and wellness rituals.\n\n"
            f"CRITICAL SYSTEM KNOWLEDGE REFERENCE:\n{systemic_guidelines}\n\n"
            f"Language: Write natively in {target_lang}. Do NOT output generic boilerplate introductory text."
        )

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user", 
                    "content": request.message
                }
            ],
            temperature=0.7
        )

        interpretation_text = completion.choices[0].message.content

        # 4. Save Cache Result
        if clean_dob:
            save_profile_to_cache(clean_name, clean_dob, target_lang, clean_focus, interpretation_text)

        return {"interpretation": interpretation_text, "numbers": numbers}

    except Exception as e:
        print("\n=== SERVER ERROR TRACEBACK ===")
        traceback.print_exc()
        print("==============================\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download-blueprint")
async def download_blueprint(name: str, dob: str, language: str, focus_area: Optional[str] = "General Life Path & Guidance"):
    try:
        clean_name = name.strip() if name else "Anonymous User"
        clean_dob = dob.strip() if dob else ""
        target_lang = language.strip() if language else "English"
        clean_focus = focus_area.strip() if focus_area else "General Life Path & Guidance"

        text_content = get_cached_profile(clean_name, clean_dob, target_lang, clean_focus)
        if not text_content:
            raise HTTPException(
                status_code=404, 
                detail="Profile report text not found. Please generate a profile reading first."
            )

        pdf_file_path = generate_blueprint_pdf(clean_name, clean_dob or "N/A", text_content)

        return FileResponse(
            path=pdf_file_path,
            media_type="application/pdf",
            filename=os.path.basename(pdf_file_path)
        )
    except Exception as e:
        if isinstance(e, HTTPException): 
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat-sandbox")
async def chat_sandbox(request: ChatRequest):
    try:
        target_lang = (request.language or "").strip() or "English"
        systemic_guidelines = load_rag_guidelines()

        system_prompt = (
            f"You are an expert life path guide and interactive conversational chatbot.\n\n"
            f"SYSTEMIC KNOWLEDGE REFERENCE:\n{systemic_guidelines}\n\n"
            f"CONVERSATIONAL EXTRACTION RULE:\n"
            f"Check if you have the user's Birth Date, Time, Location, Age, and Focus Area in context: {request.context or 'None'}.\n"
            f"If any key parameters are missing and relevant to their query, answer their question with current findings first, then politely invite them to share the missing fields to refine their calculation.\n"
            f"Target Language: Write strictly in {target_lang}."
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profiles-history")
def get_profiles_history():
    return fetch_profiles_history()