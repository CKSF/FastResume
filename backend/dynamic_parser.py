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
    prompt = f"""Please parse the following resume text into a JSON object with the following structure: {{"personal_info": {{"name": "", "email": "", "phone": ""}}, "summary": "", "experience": [{{ "title": "", "company": "", "start_date": "", "end_date": "", "description": [] }}], "education": [{{ "university": "", "degree": "", "major": "", "year": "" }}], "projects": [{{ "name": "", "dates": "", "description": [] }}], "publications": [{{ "citation": "" }}], "skills": []}}. 

IMPORTANT: 
- For projects, always include the "dates" field to capture project timelines
- For projects description field, it should be an ARRAY of complete sentences/bullet points, NOT individual characters
- Each description item should be a complete meaningful sentence or bullet point
- For experience, include ALL work experience including research positions, internships, and jobs
- For experience, use "company" field for company name, lab name, or institution name
- For experience, description should be an ARRAY of bullet points, NOT a single long string
- Research positions should be treated as regular work experience entries
- For publications, include the full "citation" text
- Extract ALL sections present in the resume, do not omit any information
- DO NOT split text into individual characters - keep meaningful phrases together

Example of correct experience format (including research):
"experience": [{{
    "title": "Deep Learning Researcher",
    "company": "Melody Lab (Emory University)",
    "start_date": "Sep 2023",
    "end_date": "May 2025",
    "description": [
        "Collaborated with Emory Clinic on seizure forecasting using RNS data; led the development of a Transformer-based model (SeizureFormer) capable of predicting seizure risk 1–14 days in advance, achieving state-of-the-art performance",
        "Researched epidemic source detection and spread prediction with Hypergraph Neural Networks (EpiDHGNN), achieving up to 7–12% accuracy improvement and 30% faster convergence compared to baseline models"
    ]
}}, {{
    "title": "Frontend Developer Intern",
    "company": "Shen Tong Technology Group Co., Ltd (Ningbo, China)",
    "start_date": "Jun 2021",
    "end_date": "Aug 2021",
    "description": [
        "Led UI redesign for automotive cooling systems, conducting user studies and usability tests to inform wireframes and prototypes, resulting in a +30% usability gain",
        "Designed the subsidiary's logo and corporate branding, which was officially adopted and registered as a company trademark"
    ]
}}]

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