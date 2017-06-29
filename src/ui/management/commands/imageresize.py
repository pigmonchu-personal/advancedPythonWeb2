from django.core.management import BaseCommand


class Command(BaseCommand):

    help = "Resize image according our responsive design"

    def handle(self, *args, **options):
        self.stdout.write("Por aquí pasa")
