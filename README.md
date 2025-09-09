# Damaris Portfolio Website

A modern, responsive Django portfolio website showcasing skills, projects, certifications, and providing a contact form. Built with Django 5.2.5 and styled with TailwindCSS.

## Features

- **Modern Design**: Clean, professional interface with purple/blue gradient theme
- **Responsive Layout**: Mobile-first design that works on all screen sizes
- **Smooth Animations**: AOS (Animate On Scroll) library for engaging user experience
- **Dual Interface**: Both web templates and REST API endpoints
- **Project Showcase**: Featured projects with technology stacks and GitHub integration
- **Skills Display**: Categorized technical skills with progress visualization
- **Certifications**: Professional certifications with status tracking and verification
- **Contact Form**: Django-powered contact form with email functionality
- **Admin Panel**: Django admin interface for content management

## Technology Stack

- **Backend**: Django 5.2.5, Django REST Framework
- **Frontend**: HTML5, TailwindCSS, JavaScript (ES6+)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Animations**: AOS (Animate On Scroll)
- **Email**: Django email with Gmail SMTP support
- **Media**: Pillow for image processing
- **Development**: Python virtual environment

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Damaris_portfolio
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv portfolio_env
   # On Windows
   portfolio_env\Scripts\activate
   # On macOS/Linux
   source portfolio_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DEFAULT_FROM_EMAIL=your-email@example.com
   CONTACT_EMAIL=contact@example.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
Damaris_portfolio/
├── portfolio_project/          # Main project settings
│   ├── settings.py            # Django settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
├── main/                     # Main portfolio app
│   ├── models.py            # Database models
│   ├── views.py             # Views (templates + API)
│   ├── urls.py              # App URL patterns
│   ├── serializers.py       # DRF serializers
│   └── templates/main/      # HTML templates
├── media/                   # User uploads
│   ├── profile/            # Profile photos
│   ├── architecture_diagrams/ # Project diagrams
│   └── certification/      # Certification images
├── db.sqlite3              # SQLite database
├── requirements.txt        # Python dependencies
└── .env                   # Environment variables
```

## Database Models

- **AboutMe**: Personal information and social links
- **Skill**: Technical skills with categories and icons
- **Project**: Portfolio projects with GitHub links and technology stacks
- **Certification**: Professional certifications with expiration tracking
- **ContactMe**: Contact form submissions

## API Endpoints

All endpoints return JSON responses:

- `GET /about/` - Personal information
- `GET /skills/` - All skills grouped by category
- `GET /projects/` - All projects with details
- `GET /projects/<id>/` - Individual project details
- `GET /certifications/` - All certifications
- `GET /certifications/<id>/` - Individual certification details
- `POST /contact/` - Submit contact form

## Development Commands

### Database Management
```bash
# Apply migrations
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Reset database (development only)
python manage.py flush
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test main
```

## Email Configuration

The application supports two email backends:

1. **Gmail SMTP** (production): Set `EMAIL_HOST_PASSWORD` in `.env`
2. **Console Backend** (development): Emails printed to console when no password is set

## Deployment

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_EMAIL=contact@yourdomain.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### Static Files
Configure your web server to serve static files from the `staticfiles/` directory after running `collectstatic`.

### Database
For production, consider using PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfolio_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Damaris Chege - [Your Contact Information]

Project Link: [https://github.com/Dama5323/Damaris_portfolio](https://github.com/Dama5323/Damaris_portfolio)