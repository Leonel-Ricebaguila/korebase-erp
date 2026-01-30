"""
SendGrid API Email Backend for Django
Uses HTTP API instead of SMTP to bypass port 587 blocking on Render
"""
import os
from django.core.mail.backends.base import BaseEmailBackend
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


class SendGridBackend(BaseEmailBackend):
    """
    Email backend that uses SendGrid's HTTP API instead of SMTP.
    This bypasses Render's port 587 blocking.
    """
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = os.getenv('SENDGRID_API_KEY') or os.getenv('EMAIL_HOST_PASSWORD')
        self.from_email = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@korebase.com')
        
        if not self.api_key:
            if not self.fail_silently:
                raise ValueError("SENDGRID_API_KEY or EMAIL_HOST_PASSWORD must be set")
    
    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return 0
        
        num_sent = 0
        for message in email_messages:
            try:
                sent = self._send(message)
                if sent:
                    num_sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        
        return num_sent
    
    def _send(self, email_message):
        """Send a single email message via SendGrid API"""
        if not email_message.recipients():
            return False
        
        try:
            # Build SendGrid message
            from_email = Email(email_message.from_email or self.from_email)
            to_emails = [To(email) for email in email_message.recipients()]
            subject = email_message.subject
            
            # Handle both plain text and HTML content
            if email_message.content_subtype == 'html':
                content = Content("text/html", email_message.body)
            else:
                content = Content("text/plain", email_message.body)
            
            # Create mail object
            mail = Mail(
                from_email=from_email,
                to_emails=to_emails[0] if len(to_emails) == 1 else to_emails,
                subject=subject,
                plain_text_content=content if email_message.content_subtype != 'html' else None,
                html_content=content if email_message.content_subtype == 'html' else None
            )
            
            # Send via API
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(mail)
            
            # SendGrid returns 202 for successful queuing
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            if not self.fail_silently:
                raise e
            return False
