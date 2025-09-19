from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import AboutMe, Skill, Project, ContactMe, Certification
from .serializers import AboutMeSerializer, SkillSerializer, ProjectSerializer, ContactMeSerializer, CertificationSerializer
from .forms import ContactForm

# ===== TEMPLATE VIEWS =====
def home_view(request):
    """Home page view - aggregates data from multiple models"""
    about_me = AboutMe.objects.first()
    featured_projects = Project.objects.filter(featured=True)[:3]
    key_skills = Skill.objects.all()[:30]
    latest_certifications = Certification.objects.all().order_by('-issue_date')[:5]
    
    # Group skills by category for home page
    skill_categories = {}
    for skill in key_skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill)
    
    context = {
        'about_me': about_me,
        'featured_projects': featured_projects,
        'key_skills': key_skills,
        'skill_categories': skill_categories,  
        'latest_certifications': latest_certifications,
    }
    return render(request, 'main/home.html', context)

def about_view(request):
    """About page view"""
    about_me = AboutMe.objects.first()
    certifications = Certification.objects.all().order_by('-issue_date')
    skills = Skill.objects.all()  
    
    # Group skills by category
    skill_categories = {}
    for skill in skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill)

    
    context = {
        'about_me': about_me,
        'skills': skills, 
        'skill_categories': skill_categories, 
        'certifications': certifications,
    }
    return render(request, 'main/about.html', context)

def projects_view(request):
    """Projects page view"""
    projects = Project.objects.all().order_by('-featured', '-created')
    context = {'projects': projects}
    return render(request, 'main/projects.html', context)

def project_detail_view(request, pk):
    """Individual project detail view"""
    project = get_object_or_404(Project, pk=pk) 
    context = {'project': project}
    return render(request, 'main/project_detail.html', context)

def certifications_view(request):  
    """Certifications page view"""
    certifications = Certification.objects.all().order_by('-issue_date')
    context = {'certifications': certifications}
    return render(request, 'main/certifications.html', context)

def certification_detail_view(request, pk): 
    """Individual certification detail view"""
    certification = get_object_or_404(Certification, pk=pk)
    context = {'certification': certification}
    return render(request, 'main/certification_detail.html', context)

def contact_view(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email notification (optional)
            try:
                send_mail(
                    f'Portfolio Contact from {contact_message.name}',
                    f'Name: {contact_message.name}\nEmail: {contact_message.email}\n\nMessage:\n{contact_message.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],  
                    fail_silently=True,
                )
            except:
                pass  
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'main/contact.html', context)

# ===== API VIEWS =====
class AboutMeListAPIView(generics.ListAPIView):
    """API endpoint for About Me data"""
    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer
    permission_classes = [AllowAny]

class SkillListAPIView(generics.ListAPIView):
    """API endpoint for Skills"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]

class ProjectListAPIView(generics.ListAPIView):
    """API endpoint for Projects"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProjectDetailAPIView(generics.RetrieveAPIView):
    """API endpoint for single Project detail"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class CertificationListAPIView(generics.ListAPIView):  
    """API endpoint for Certifications"""
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]

class CertificationDetailAPIView(generics.RetrieveAPIView):  
    """API endpoint for single Certification detail"""
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Your name'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Your message'),
        },
        required=['name', 'email', 'message']
    ),
    responses={
        201: openapi.Response('Contact message created successfully', ContactMeSerializer),
        400: openapi.Response('Bad Request - Invalid data'),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def contact_api_view(request):
    """API endpoint for contact form submissions"""
    serializer = ContactMeSerializer(data=request.data)
    if serializer.is_valid():
        contact_message = serializer.save()
        
        # Send email notification (optional)
        try:
            send_mail(
                f'Portfolio Contact from {contact_message.name}',
                f'Name: {contact_message.name}\nEmail: {contact_message.email}\n\nMessage:\n{contact_message.message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  
                fail_silently=True,
            )
        except:
            pass
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)