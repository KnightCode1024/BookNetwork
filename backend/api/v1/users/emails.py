from djoser import email
from django.conf import settings
from api.v1.users.tasks import send_activation_email, send_password_reset_email


class CustomActivationEmail(email.ActivationEmail):
    def send(self, to, *args, **kwargs):
        try:
            context = self.get_context_data()
            user = context.get("user")

            if user and user.id:
                activation_url = (
                    f"{settings.FRONTEND_URL}/activate/"
                    f"{context.get('uid')}/{context.get('token')}"
                )

                celery_context = {
                    "uid": context.get("uid"),
                    "token": context.get("token"),
                    "url": activation_url,
                    "domain": settings.FRONTEND_URL,
                    "site_name": "BookNetwork",
                }

                send_activation_email.delay(
                    user_id=user.id,
                    context=celery_context,
                )

            else:
                super().send(to, *args, **kwargs)

        except Exception as e:
            print(f"Ошибка в CustomActivationEmail: {e}")
            super().send(to, *args, **kwargs)


class CustomPasswordResetEmail(email.PasswordResetEmail):
    def send(self, to, *args, **kwargs):
        try:
            context = self.get_context_data()
            user = context.get("user")

            if user and user.id:
                reset_password_url = (
                    f"{settings.FRONTEND_URL}/password-reset-confirm/"
                    f"{context.get('uid')}/{context.get('token')}"
                )

                celery_context = {
                    "uid": context.get("uid"),
                    "token": context.get("token"),
                    "url": reset_password_url,
                    "domain": settings.FRONTEND_URL,
                    "site_name": "BookNetwork",
                }
                send_password_reset_email.delay(
                    user_id=user.id,
                    context=celery_context,
                )
            else:
                super().send(to, *args, **kwargs)

        except Exception as e:
            print(f"Ошибка в CustomPasswordResetEmail: {e}")
            super().send(to, *args, **kwargs)
