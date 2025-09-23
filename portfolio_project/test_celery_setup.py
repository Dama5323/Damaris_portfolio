# test_celery_setup.py
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from main.tasks import send_contact_notification, send_auto_response

# Test data matching your ContactMe model
test_contact_data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'message': 'This is a test message to verify Celery and RabbitMQ are working!',
    'timestamp': '2024-01-15 10:00:00',
    'db_id': 1
}

print("Testing Celery tasks...")

# Test the notification task
try:
    result = send_contact_notification.delay(test_contact_data)
    print(f"✅ Notification task submitted. Task ID: {result.id}")
except Exception as e:
    print(f"❌ Error submitting notification task: {e}")

# Test the auto-response task
try:
    result = send_auto_response.delay(test_contact_data)
    print(f"✅ Auto-response task submitted. Task ID: {result.id}")
except Exception as e:
    print(f"❌ Error submitting auto-response task: {e}")

print("Check your Celery worker terminal to see if tasks are being processed.")