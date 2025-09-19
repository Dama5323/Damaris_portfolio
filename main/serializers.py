from rest_framework import serializers
from .models import AboutMe, Skill, Project, ContactMe, Certification

class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'category_display', 'description', 'icon', 'created', 'modified']
        # Removed 'level' field since it doesn't exist in the model

class ProjectSerializer(serializers.ModelSerializer):
    technologies_used = SkillSerializer(many=True, read_only=True)
    project_type_display = serializers.CharField(source='get_project_type_display', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'project_type', 'project_type_display', 
            'technologies_used', 'github_url', 'live_demo_url', 
            'architecture_diagram', 'featured', 'created', 'modified'
        ]

class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = [
            'id', 'full_name', 'title', 'location', 'email_public', 
            'phone_public', 'bio_md', 'resume_url', 'github_url', 
            'linkedin_url', 'photo', 'created', 'modified'
        ]

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class ContactMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMe
        fields = ['id', 'name', 'email', 'message', 'created', 'modified']