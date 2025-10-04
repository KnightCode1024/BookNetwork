from djoser import email
from django.conf import settings

from api.v1.users.tasks import send_activation_email


class CustomActivationEmail(email.ActivationEmail):
    def send(self, to, *args, **kwargs):
        try:
            context = self.get_context_data()

            user = context.get("user")

            if user and user.id:
                activation_url = (
                    f"{settings.FRONTEND_URL}/activate/"
                    f"{context.get('uid')}/{context.get('token')}/"
                )

                celery_context = {
                    "uid": context.get("uid"),
                    "token": context.get("token"),
                    "url": activation_url,
                    "domain": settings.FRONTEND_URL or "127.0.0.1:8000",
                    "site_name": context.get("site_name", "BookNetwork"),
                }

                send_activation_email.delay(
                    user_id=user.id,
                    context=celery_context,
                )

                print(
                    (
                        "Задача отправки активационного письма поставлена"
                        f"в очередь для пользователя {user.email}"
                    )
                )
            else:
                print("Ошибка: пользователь не найден в контексте")
                super().send(to, *args, **kwargs)

        except Exception as e:
            print(f"Ошибка при постановке задачи отправки письма: {e}")
            super().send(to, *args, **kwargs)
