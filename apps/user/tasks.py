from AudioBook.celery import app
from django.conf import settings
from django.core.mail import send_mail


@app.task(bind=True)
def send_email(self, email, code, redirect_url, **kwargs):
    subject = 'Verify your email'
    message = f"Verify your code: {code} Url: {redirect_url}"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email]
    )
