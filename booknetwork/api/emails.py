from djoser import email
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from api.v1.users.tasks import send_activation_email


class CustomActivationEmail(email.ActivationEmail):
    """
    Кастомное письмо активации аккаунта через Celery
    """

    template_name = "email/activation.html"  # Укажите путь к вашему шаблону

    def send(self, to, *args, **kwargs):
        """
        Отправка письма через Celery вместо синхронной отправки
        """
        try:
            # Получаем контекст письма
            context = self.get_context_data()

            # Получаем пользователя
            user = context.get("user")

            if user and user.id:
                # Формируем полный URL для активации
                activation_url = f"{settings.FRONTEND_URL}/activate/{context.get('uid')}/{context.get('token')}/"

                celery_context = {
                    "uid": context.get("uid"),
                    "token": context.get("token"),
                    "url": activation_url,
                    "domain": settings.FRONTEND_URL or "127.0.0.1:8000",
                    "site_name": context.get("site_name", "BookNetwork"),
                }

                # Отправляем задачу в Celery
                send_activation_email.delay(
                    user_id=user.id,
                    context=celery_context,
                )

                print(
                    f"Задача отправки активационного письма поставлена в очередь для пользователя {user.email}"
                )
            else:
                print("Ошибка: пользователь не найден в контексте")
                # Fallback: отправляем синхронно
                super().send(to, *args, **kwargs)

        except Exception as e:
            print(f"Ошибка при постановке задачи отправки письма: {e}")
            # Fallback: отправляем синхронно
            super().send(to, *args, **kwargs)
