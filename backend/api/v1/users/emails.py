from djoser import email
from django.conf import settings
from api.v1.users.tasks import send_activation_email


class CustomActivationEmail(email.ActivationEmail):
    def send(self, to, *args, **kwargs):
        try:
            context = self.get_context_data()
            user = context.get("user")

            print(f"🎯 CustomActivationEmail.send() вызван")
            print(f"📧 Получатель: {to}")
            print(f"👤 Пользователь: {user}")

            if user and user.id:
                # Уберите слеш в конце URL
                activation_url = f"{settings.FRONTEND_URL}/activate/{context.get('uid')}/{context.get('token')}"

                celery_context = {
                    "uid": context.get("uid"),
                    "token": context.get("token"),
                    "url": activation_url,
                    "domain": settings.FRONTEND_URL,
                    "site_name": "BookNetwork",
                }

                print(f"✅ Ставим задачу в Celery для пользователя {user.email}")
                print(f"🔗 Ссылка активации: {activation_url}")

                # Поставьте задачу в очередь
                send_activation_email.delay(
                    user_id=user.id,
                    context=celery_context,
                )

                print(f"✅ Задача отправлена в очередь для {user.email}")

            else:
                print("❌ Ошибка: пользователь не найден в контексте")
                super().send(to, *args, **kwargs)

        except Exception as e:
            print(f"❌ Ошибка в CustomActivationEmail: {e}")
            import traceback

            traceback.print_exc()
            super().send(to, *args, **kwargs)
