from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pdfplumber
import re
from .models import Resume  # Optional if using the model

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        if not file.name.endswith('.pdf'):
            return JsonResponse({"error": "Invalid file format"}, status=400)

        data = extract_resume_data(file)
        # Optional: Save to database
        # Resume.objects.create(**data)

        return JsonResponse(data)

    return JsonResponse({"error": "No file uploaded"}, status=400)
from pdfminer.high_level import extract_text
import io
def extract_resume_data(file):

    data = {
        "name": "",
        "phone": "",
        "email": "",
        "education": "",
        "work_experience": "",
        "technologies": ""
    }

    file_content = io.BytesIO(file.read())
    text = extract_text(file_content)

    def extract_skills_from_resume(text, skills_list):
        skills = []

        for skill in skills_list:
            pattern = r"\b{}\b".format(re.escape(skill))
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                skills.append(skill)

        return skills

    name_pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    phone_pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    education_pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    experience_pattern =  ['[A-Z][a-z]* [A-Z][a-z]* Private Limited','[A-Z][a-z]* [A-Z][a-z]* Pvt. Ltd.','[A-Z][a-z]* [A-Z][a-z]* Inc.', '[A-Z][a-z]* LLC',
                ]
    pattern = '({})'.format('|'.join(experience_pattern))
    skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau']

    data["name"] = re.search(name_pattern, text).group(0).strip() if re.search(name_pattern, text) else ""
    data["phone"] = re.findall(phone_pattern, text)
    data["email"] = re.findall(email_pattern, text)
    data["education"] = re.findall(education_pattern, text)
    data["work_experience"] = re.findall(pattern, text)
    data["technologies"] = extract_skills_from_resume(text, skills_list)

    return data

def home(request):
    return render(request, 'parser/index.html')