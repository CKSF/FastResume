from weasyprint import HTML
from flask import render_template
import os

def generate_pdf_from_template(resume_data, template_name, output_path=None):
    """
    Generate PDF from template using structured resume data
    
    Args:
        resume_data: Dictionary containing structured resume data
        template_name: Name of the template (e.g., 'default')
        output_path: Path to save PDF (optional, for preview mode)
    
    Returns:
        For file generation: True/False
        For preview mode: BytesIO object
    """
    try:
        # Determine template file path
        template_file = f"{template_name}.html"
        css_file = f"{template_name}.css"
        
        # Get the absolute path to the templates directory
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        css_path = os.path.join(template_dir, css_file)
        
        # Read CSS content
        css_content = ""
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
        
        # Render HTML using Jinja2 template
        html_content = render_template(template_file, 
                                     personal_info=resume_data.get('personal_info', {}),
                                     summary=resume_data.get('summary', ''),
                                     experience=resume_data.get('experience', []),
                                     projects=resume_data.get('projects', []),
                                     research=resume_data.get('research', []),
                                     education=resume_data.get('education', []),
                                     skills=resume_data.get('skills', []),
                                     publications=resume_data.get('publications', []),
                                     section_order=resume_data.get('section_order', ['summary', 'experience', 'projects', 'education', 'skills', 'publications']),
                                     css_content=css_content)
        
        # Debug: Save HTML to file for inspection
        if output_path:
            debug_html_path = output_path.replace('.pdf', '_debug.html')
            with open(debug_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Debug HTML saved to: {debug_html_path}")
        
        # Generate PDF
        if output_path:
            # File mode: save to disk
            HTML(string=html_content).write_pdf(output_path)
            return True
        else:
            # Preview mode: return BytesIO
            from io import BytesIO
            pdf_buffer = BytesIO()
            HTML(string=html_content).write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            return pdf_buffer
            
    except Exception as e:
        print(f"Error generating PDF: {e}")
        if output_path:
            return False
        else:
            return None

# Legacy function for backward compatibility
def generate_pdf_from_html_string(html_content, template_name, output_path):
    """
    Legacy function that accepts HTML string directly
    This is kept for backward compatibility but should be deprecated
    """
    try:
        debug_html_path = output_path.replace('.pdf', '_debug.html')
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Debug HTML saved to: {debug_html_path}")
        
        HTML(string=html_content).write_pdf(output_path)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False