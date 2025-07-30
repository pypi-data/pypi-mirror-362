from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Find a model class in your Django project'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model class to find')

    def handle(self, *args, **options):
        model_name = options['model_name']
        found_model = None

        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                if model.__name__ == model_name:
                    found_model = model
                    break

        if found_model:
            self.stdout.write(self.style.SUCCESS(f"Found the model class '{model_name}' in app '{found_model._meta.app_label}'."))
        else:
            self.stdout.write(self.style.ERROR(f"Model class '{model_name}' not found."))
