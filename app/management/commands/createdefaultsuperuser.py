from django.contrib.auth.management.commands import createsuperuser
from pathlib import Path
from django.conf import settings
import os, environ

# Load .env
env = environ.Env()
env.read_env('.env')

class Command(createsuperuser.Command):
    help = 'Create superuser by .env'

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        username = env('SUPERUSER_NAME')
        email = env('SUPERUSER_EMAIL')
        password = env('SUPERUSER_PASSWORD')
        database = options.get('database')

        superuser = {
            'username': username,
            'email': email,
            'password': password,
        }

        if not self.UserModel._default_manager.db_manager(database).filter(username=username).exists():
            self.UserModel._default_manager.db_manager(database).create_superuser(**superuser)
            