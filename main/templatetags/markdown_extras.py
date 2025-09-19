from django.shortcuts import render
from django.utils.safestring import mark_safe
from markdown import markdown

# ✅ Import your models
from main.models import AboutMe, Certification, Skill  

def about_view(request):
    about_me = AboutMe.objects.first()
    certifications = Certification.objects.all().order_by('-issue_date')
    skills = Skill.objects.all()  

    # Convert bio text (Markdown) to safe HTML
    formatted_bio = None
    if about_me and about_me.bio:
        formatted_bio = mark_safe(markdown(about_me.bio))

    # Group skills by category
    skill_categories = {}
    for skill in skills:
        skill_categories.setdefault(skill.category, []).append(skill)

    context = {
        'about_me': about_me,
        'formatted_bio': formatted_bio,
        'skills': skills,
        'skill_categories': skill_categories,
        'certifications': certifications,
    }
    return render(request, 'main/about.html', context)
