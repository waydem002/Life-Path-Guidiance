import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_blueprint_pdf(name: str, dob: str, text_content: str) -> str:
    """
    Compiles raw string content into an elegantly formatted PDF document blueprint.
    Returns the absolute path to the generated file.
    """
    # Create a temporary directory for generated exports
    export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    # Establish file naming structure safely
    filename = f"Life_Path_Blueprint_{name.replace(' ', '_')}.pdf"
    file_path = os.path.join(export_dir, filename)
    
    # Initialize the Document Flow layout
    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Define clean, modern text styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=14,
        textColor='#555555',
        spaceAfter=24
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        spaceAfter=12
    )
    
    # Construct Document Structure Header
    story.append(Paragraph(f"Strategic Life Path Blueprint", title_style))
    story.append(Paragraph(f"Prepared for: {name.title()} || Date of Birth: {dob}", meta_style))
    story.append(Spacer(1, 12))
    
    # Split incoming string blocks cleanly into individual paragraphs
    paragraphs = text_content.split("\n\n")
    for para in paragraphs:
        cleaned_para = para.strip().replace("\n", " ")
        if cleaned_para:
            story.append(Paragraph(cleaned_para, body_style))
            
    # Build document
    doc.build(story)
    return file_path