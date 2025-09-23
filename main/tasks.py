# main/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_contact_notification(self, contact_data):
    """
    Send email notification to YOU when someone contacts you
    """
    try:
        name = contact_data.get('name', 'Unknown')
        email = contact_data.get('email', 'No email provided')
        message = contact_data.get('message', 'No message provided')
        
        # Email to YOU (the portfolio owner)
        email_subject = f'🔥 Portfolio Contact: Message from {name}'
        
        email_body = f"""
        🚀 NEW PORTFOLIO CONTACT FORM SUBMISSION!

        You have received a new message from your portfolio website:

        📧 Contact Details:
        • Name: {name}
        • Email: {email}
        • Timestamp: {contact_data.get('timestamp', 'Unknown')}

        💬 Message:
        {message}

        ⚡ Action Required:
        Please respond to this inquiry as soon as possible.

        ---
        This email was sent automatically from your portfolio contact form.
        """

        # Send email to yourself
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # Your email address
            fail_silently=False,
        )
        
        logger.info(f"✅ Contact notification email sent successfully for {email}")
        return f"✅ Email sent successfully for {email}"
        
    except Exception as e:
        logger.error(f"❌ Failed to send contact notification email: {str(e)}")
        # Retry after 60 seconds if failed
        raise self.retry(countdown=60, exc=e)

@shared_task
def send_auto_response(contact_data):
    """
    Send automatic response to the person who contacted you
    """
    try:
        name = contact_data.get('name', 'There')
        email = contact_data.get('email')
        
        if not email:
            return "❌ No email provided for auto-response"
        
        auto_response_subject = 'Thank you for contacting me! - Damaris'
        
        auto_response_body = f"""
        Hi {name},

        Thank you for reaching out to me through my portfolio website! 
        I have received your message and will review it carefully.

        🔄 What happens next?
        • I'll get back to you within 24-48 hours
        • We can schedule a call to discuss your project
        • I'll provide any additional information you need

        💼 In the meantime, you can:
        • Check out my projects: [Your Portfolio URL]/projects
        • Learn more about my skills: [Your Portfolio URL]/about
        • Connect with me on LinkedIn

        Looking forward to speaking with you!

        Best regards,
        Damaris
        """

        send_mail(
            auto_response_subject,
            auto_response_body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        logger.info(f"✅ Auto-response sent to {email}")
        return f"✅ Auto-response sent to {email}"
        
    except Exception as e:
        logger.error(f"❌ Failed to send auto-response: {str(e)}")
        return f"❌ Failed to send auto-response: {str(e)}"