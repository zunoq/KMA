from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                return user
            return None
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
