from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_activation_email(self, user_id, context):
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()

        user = User.objects.get(id=user_id)

        subject = "Активация аккаунта"
        message = f"""
        Здравствуйте, {user.get_full_name() or user.username}!
        
        Для активации вашего аккаунта перейдите по ссылке:
        {context.get('uid')}/{context.get('token')}/
        
        С уважением,
        ИП Обнал Кидалов!
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        print(f"Активационное письмо отправлено на {user.email}")

    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        raise self.retry(countdown=60)
