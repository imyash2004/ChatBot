import spacy
import PyPDF2
import json

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')


def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    extracted_text = ""

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()

    return extracted_text


def extract_details(text):
    doc = nlp(text)
    details = {
        'Name': '',
        'Contact': '',
        'LinkedIn': '',
        'Github': '',
        'Leetcode': '',
        'Education': [],
        'Experience': [],
        'Projects': [],
        'Skills': [],
        'Achievements': [],
        'Prizes': [],
        'Certifications': [],
        'Companies': []
    }

    # Extract contact information
    contact_keywords = ['linkedin', 'github', 'leetcode', 'email']
    for ent in doc.ents:
        if 'yash agarwal' in ent.text.lower():
            details['Name'] = ent.text
        elif any(keyword in ent.text.lower() for keyword in contact_keywords):
            if 'linkedin' in ent.text.lower():
                details['LinkedIn'] = ent.text
            elif 'github' in ent.text.lower():
                details['Github'] = ent.text
            elif 'leetcode' in ent.text.lower():
                details['Leetcode'] = ent.text
            elif 'email' in ent.text.lower() or '@' in ent.text:
                details['Contact'] = ent.text

    # Define keywords for different sections
    experience_keywords = ['experience', 'work experience', 'employment history']
    projects_keywords = ['projects']
    skills_keywords = ['skills', 'technical skills']
    achievements_keywords = ['achievements', 'awards', 'positions held']
    prizes_keywords = ['prizes', 'awards']
    certifications_keywords = ['certifications']
    education_keywords = ['education', 'academic background']
    companies_keywords = ['company', 'organization']

    # Extract information based on keywords
    for ent in doc.ents:
        if any(keyword in ent.text.lower() for keyword in experience_keywords):
            details['Experience'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in projects_keywords):
            details['Projects'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in skills_keywords):
            details['Skills'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in achievements_keywords):
            details['Achievements'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in prizes_keywords):
            details['Prizes'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in certifications_keywords):
            details['Certifications'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in education_keywords):
            details['Education'].append(ent.text)
        elif any(keyword in ent.text.lower() for keyword in companies_keywords) or ent.label_ == 'ORG':
            details['Companies'].append(ent.text)

    # Remove duplicates
    for key in details:
        if isinstance(details[key], list):
            details[key] = list(set(details[key]))

    return details


# Specify the path to your PDF resume
pdf_path = 'RESUME_YASH_AGARWAL (9).pdf'

# Extract text from the PDF
text = extract_text_from_pdf(pdf_path)

# Extract details from the resume text
details = extract_details(text)
print(details)
# Save the extracted details to a JSON file
# output_json_path = 'resume_details.json'
# with open(output_json_path, 'w') as json_file:
#     json.dump(details, json_file, indent=4)
#
# print(f"Details extracted and saved to {output_json_path}")
