# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_activation_email(self, user_id, context):
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.get(id=user_id)

        print(f"🎯 Задача send_activation_email запущена")
        print(f"👤 Пользователь: {user.email} (ID: {user.id})")
        print(f"📋 Контекст: {context}")

        subject = "Активация аккаунта BookNetwork"

        # Используйте URL из контекста
        activation_url = context.get("url", "")

        message = f"""
        Здравствуйте, {user.get_full_name() or user.username}!

        Для активации вашего аккаунта перейдите по ссылке:
        {activation_url}

        С уважением,
        Команда BookNetwork!
        """

        print(f"📤 Отправляем письмо на: {user.email}")
        print(f"📝 Тема: {subject}")
        print(f"🔗 Ссылка: {activation_url}")

        # Проверьте настройки email
        print(f"📧 FROM: {settings.DEFAULT_FROM_EMAIL}")
        print(f"�️ EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"🔌 EMAIL_PORT: {settings.EMAIL_PORT}")

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        print(f"✅ Письмо успешно отправлено на {user.email}")

    except Exception as e:
        print(f"❌ Ошибка при отправке письма: {e}")
        import traceback

        traceback.print_exc()
        raise self.retry(countdown=60)
