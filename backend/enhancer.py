import re
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import logging
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取API密钥
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

def enhance_resume(resume_data, keywords):
    """
    Enhances the resume data using a generative AI model.
    Takes structured resume data (dict) and keywords (str) as input.
    Returns a dictionary with the enhanced resume data.
    """
    try:
        # Convert the resume data dictionary to a JSON string for the prompt
        resume_json_str = json.dumps(resume_data, indent=2)

        model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
        prompt = f"""Here is a resume in JSON format:

```json
{resume_json_str}
```

Here is a job description:

```text
{keywords}
```

Please rewrite the `summary`, `experience`, and `projects` sections of the resume to better align with the job description. 
For the `experience` and `projects` sections, focus on rephrasing the descriptions to highlight relevant skills and accomplishments. 

IMPORTANT: 
- Keep ALL existing fields and structure intact, including dates, names, titles, etc.
- For projects, preserve the "dates" field (not "date") if it exists - this is crucial for displaying project timelines
- Keep all sections including "publications", "education", "skills", "research", etc. exactly as they are
- Only enhance the content of summary, experience descriptions, and project descriptions

Return a complete JSON object with the same structure as the input, but with the enhanced content. Do not add any new keys or change the structure. The output must be a valid JSON object.
"""
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                max_output_tokens=8192,
                temperature=0.7,
            ),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )

        try:
            # The response should be a JSON string. We parse it into a Python dict.
            enhanced_data = json.loads(response.text)
            logging.info(f"Enhanced data: {json.dumps(enhanced_data, indent=2)}")
            
            # Force preserve critical fields that the AI might have dropped
            if 'projects' in resume_data and 'projects' in enhanced_data:
                for i, original_project in enumerate(resume_data['projects']):
                    if i < len(enhanced_data['projects']):
                        # Preserve dates field if it exists in original
                        if 'dates' in original_project:
                            enhanced_data['projects'][i]['dates'] = original_project['dates']
                        # Preserve name field
                        if 'name' in original_project:
                            enhanced_data['projects'][i]['name'] = original_project['name']
            
            # Force preserve publications section if it exists in original  
            if 'publications' in resume_data:
                enhanced_data['publications'] = resume_data['publications']
            
            # Merge research into experience if both exist
            if 'research' in resume_data and 'experience' in enhanced_data:
                # Convert research items to experience format
                for research_item in resume_data['research']:
                    experience_item = {
                        'title': research_item.get('title', ''),
                        'company': research_item.get('lab', research_item.get('institution', '')),  # Use lab or institution as company
                        'start_date': '',
                        'end_date': '',
                        'description': research_item.get('description_points', [research_item.get('description', '')])
                    }
                    
                    # Handle dates - split if it's a range (check both 'dates' and 'date' fields)
                    date_field = research_item.get('dates') or research_item.get('date', '')
                    if date_field:
                        if '–' in date_field or '-' in date_field:
                            date_parts = date_field.replace('–', '-').split('-')
                            if len(date_parts) >= 2:
                                experience_item['start_date'] = date_parts[0].strip()
                                experience_item['end_date'] = date_parts[1].strip()
                        else:
                            experience_item['end_date'] = date_field
                    
                    # Add to experience list
                    enhanced_data['experience'].append(experience_item)
                
                # Remove research section since it's now merged - don't preserve it separately
                if 'research' in enhanced_data:
                    del enhanced_data['research']
            
            # Debug: Print the projects data to see if dates are preserved
            if 'projects' in enhanced_data:
                logging.info(f"Projects data after preservation: {json.dumps(enhanced_data['projects'], indent=2)}")
            if 'research' in enhanced_data:
                logging.info(f"Research data after preservation: {json.dumps(enhanced_data['research'], indent=2)}")
                
            return enhanced_data
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON from LLM response: {e}")
            print(f"Raw response text: {response.text}")
            # Fallback or error handling
            return {"error": "Failed to parse enhanced resume from LLM."}
        except Exception as e:
            print(f"Error getting response text: {e}")
            print(f"Full response object: {response}")
            return {"error": f"Response was blocked. Details: {e}"}

    except ValueError as e:
        return {"error": f"Error enhancing resume: Response was blocked. Details: {e}"}
    except Exception as e:
        return {"error": f"Error enhancing resume: {e}"}