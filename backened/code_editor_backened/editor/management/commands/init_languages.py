from django.core.management.base import BaseCommand
from editor.services.language_handler import check_language_support, initialize_languages


class Command(BaseCommand):
    help = 'Initialize the database with default programming languages'

    def handle(self, *args, **options):
        self.stdout.write('Checking language support...')
        support = check_language_support()
        
        for language, supported in support.items():
            status = 'Available' if supported else 'Not available'
            self.stdout.write(f'  {language}: {status}')
        
        self.stdout.write('Initializing programming languages...')
        initialize_languages()
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized programming languages'))