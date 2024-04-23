from django.core import management
from django.core.management.base import BaseCommand
from portmap.core.articles import get_content_files

class Command(BaseCommand):
    help = "Populates the articles into the db"

    def handle(self, *args, **options):
        get_content_files()
        self.stdout.write(self.style.SUCCESS("Articles populated!"))
