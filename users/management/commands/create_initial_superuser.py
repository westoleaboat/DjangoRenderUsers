from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create the initial superuser if it does not exist.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', '', '123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "admin" already exists.'))
