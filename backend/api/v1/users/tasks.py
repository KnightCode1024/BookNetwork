from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


@shared_task(bind=True, max_retries=3)
def send_activation_email(user_id, context):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)

        subject = "Активация аккаунта в сервисе Переплёт"

        activation_url = context.get("url", "")

        message = f"""
        Здравствуйте, {user.get_full_name() or user.username}!

        Для активации вашего аккаунта перейдите по ссылке:
        {activation_url}

        С уважением,
        Команда Переплёта!
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    except Exception as e:
        raise e


@shared_task(bind=True, max_retries=3)
def send_password_reset_email(user_id, context):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)

        subject = "Сброс пароля в сервисе Переплёт"
        reset_password_url = context.get("url", "")

        message = f"""
        Здравствуйте, {user.get_full_name() or user.username}!

        Для сброса пароля перейдите по ссылке:
        {reset_password_url}

        С уважением,
        Команда Переплёта!
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    except Exception as e:
        raise e
