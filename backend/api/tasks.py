from django.core.mail import send_mail

from manufacture.settings import EMAIL_HOST_USER


def send_email(
        subject,
        recipient_list,
        from_email=EMAIL_HOST_USER,
        fail_silently=False,
        connection=None,
        html_message=None,
        message=None,
):

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        connection=connection,
        html_message=html_message,
    )
