from django.contrib.auth import get_user_model
from django.core.management import CommandError, BaseCommand
from user.hashers import make_password


class Command(BaseCommand):
    help = "Create an admin, and allow password to be provided"

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Admin's username")
        parser.add_argument("--email", help="Admin's email")
        parser.add_argument("--password", help="Admin's password")

    def handle(self, *args, **options):
        username = options.get("username")
        password = options.get("password")
        email = options.get("email")

        if password and not username:
            raise CommandError("--username is required if specifying --password")

        if password and not email:
            raise CommandError("--email is required if specifying --password")

        if password:
            User = get_user_model()
            user = User(
                username=username,
                email=email,
                is_active=True,
                role="admin",
                is_superuser=True,
                password=make_password(password),
            )
            user.save()
