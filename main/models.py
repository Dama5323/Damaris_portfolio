from django.db import models
from django.utils.text import slugify
from django.utils import timezone  
from cloudinary.models import CloudinaryField 

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AboutMe(TimeStampedModel):
    full_name = models.CharField(max_length=120)
    title = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=120, blank=True)
    email_public = models.EmailField(blank=True)
    phone_public = models.CharField(max_length=50, blank=True)
    bio_md = models.TextField(help_text="Markdown supported", blank=True)
    resume_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    photo = CloudinaryField('image', folder="profile", blank=True, null=True)

    class Meta:
        verbose_name_plural = "About me"
        constraints = [
            models.UniqueConstraint(fields=['full_name'], name='unique_about_me')
        ]

    def __str__(self):
        return self.full_name


class Skill(TimeStampedModel):
    class Category(models.TextChoices):
        PROGRAMMING_LANGUAGE = "Programming Language", "Programming Language"
        FRAMEWORK = "Framework", "Framework"
        API_ARCHITECTURE = "API & Architecture", "API & Architecture"
        DEVOPS_DEPLOYMENT = "DevOps & Deployment", "DevOps & Deployment"
        SECURITY_AUTH = "Authentication & Security", "Authentication & Security"
        CLOUD = "Cloud", "Cloud"
        DATABASE = "Database", "Database"
        TOOLS = "Tools", "Tools"
        SOFT_SKILLS = "Soft Skills", "Soft Skills"

    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=32, choices=Category.choices)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=50, blank=True, 
                           help_text="Icon class name (e.g., from Font Awesome)")

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"

class Project(TimeStampedModel):
    PROJECT_TYPES = (
        ('Backend', 'Backend'),
        ('Cloud', 'Cloud Architecture'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField(
        help_text="Use '-' at the beginning of a line for bullet points. Example:\n- First item\n- Second item\n- Third item"
    )
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    technologies_used = models.ManyToManyField(Skill, blank=True, related_name='projects') 
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    architecture_diagram = CloudinaryField('image', folder="architecture_diagrams", blank=True, null=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-featured', '-created']

    def __str__(self):
        return self.title
    
class Certification(TimeStampedModel):
    class Category(models.TextChoices):
        AWS = "aws", "AWS"
        ALX = "Alx", "Alx"
        OTHER = "other", "other"

    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    image = CloudinaryField('image', folder="certification", blank=True, null=True)


    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.name} ({self.issuer})"

    def is_expired(self):
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        return False
    
class ContactMe(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    