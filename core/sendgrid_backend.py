"""
SendGrid API Email Backend for Django
Uses HTTP API instead of SMTP to bypass port 587 blocking on Render
"""
import os
import logging
from django.core.mail.backends.base import BaseEmailBackend
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


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
                raise ValueError("SENDGRID_API_KEY must be set in environment variables")

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number sent.
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
                logger.error(f"[SendGrid] Error sending to {message.recipients()}: {e}")
                if not self.fail_silently:
                    raise

        return num_sent

    def _send(self, email_message):
        """Send a single email message via SendGrid HTTP API"""
        recipients = email_message.recipients()
        if not recipients:
            return False

        try:
            from_email = email_message.from_email or self.from_email
            subject = email_message.subject
            body = email_message.body

            # Determine content type
            if hasattr(email_message, 'alternatives') and email_message.alternatives:
                # EmailMultiAlternatives (HTML email) — grab the HTML part
                html_body = None
                for content, mimetype in email_message.alternatives:
                    if mimetype == 'text/html':
                        html_body = content
                        break
                mail = Mail(
                    from_email=from_email,
                    to_emails=recipients,
                    subject=subject,
                    plain_text_content=body,
                    html_content=html_body or body,
                )
            else:
                # Plain text email
                mail = Mail(
                    from_email=from_email,
                    to_emails=recipients,
                    subject=subject,
                    plain_text_content=body,
                )

            sg = SendGridAPIClient(self.api_key)
            response = sg.send(mail)

            logger.info(f"[SendGrid] Sent to {recipients} — status {response.status_code}")
            return response.status_code in [200, 201, 202]

        except Exception as e:
            logger.error(f"[SendGrid] _send failed: {e}")
            if not self.fail_silently:
                raise
            return False
