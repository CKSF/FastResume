import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

def parse_dynamic_resume(enhanced_resume_text, email=None, phone=None):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    prompt = f"""Please parse the following resume text into a JSON object with the following structure: {{"personal_info": {{"name": "", "email": "", "phone": ""}}, "summary": "", "experience": [{{ "title": "", "company": "", "start_date": "", "end_date": "", "description": [] }}], "education": [{{ "university": "", "degree": "", "major": "", "year": "" }}], "projects": [{{ "name": "", "dates": "", "description": [] }}], "research": [{{ "title": "", "lab": "", "institution": "", "date": "", "description": "" }}], "publications": [{{ "citation": "" }}], "skills": []}}. 

IMPORTANT: 
- For projects, always include the "dates" field to capture project timelines
- For research, include "title", "lab" (laboratory/research group name), "institution" (university/organization), "date", and "description" fields
- For publications, include the full "citation" text
- Extract ALL sections present in the resume, do not omit any information

Here is the resume text:\n\n{enhanced_resume_text}"""
    
    response = model.generate_content(prompt,
    generation_config=genai.types.GenerationConfig(
        max_output_tokens=8192,
        temperature=0.2,
    ),
    safety_settings=[
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
    ]
    )
    
    try:
        # Extract the JSON string from the response
        json_string = response.text.strip(' `json\n')
        parsed_data = json.loads(json_string)

        # Overwrite with correct PII if provided
        if email:
            parsed_data.setdefault('personal_info', {})['email'] = email
        if phone:
            parsed_data.setdefault('personal_info', {})['phone'] = phone

        return parsed_data
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing JSON from response: {e}")
        print(f"Raw response text: {response.text}")
        return None