from django.core.management.base import BaseCommand, CommandError

from LearnModels.models import Post


class Command(BaseCommand):
    help = '123'
    #missing_args_message = 'Args is none'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you want to delete all posts? yes/no')
        answer = input()

        if answer == 'yes':
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Success'))
            return

        self.stdout.write(self.style.ERROR('Error'))