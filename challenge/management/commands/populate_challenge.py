import json
import os
from django.core.management.base import BaseCommand, CommandError
from challenge.models import Challenge
from django.db import IntegrityError
from django.conf import settings

class Command(BaseCommand):
    help = "Populates the database with some test data"

    def handle(self, *args, **options):
        try:
            filename = os.path.join(settings.BASE_DIR, "challenge", "challenge.json")
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise CommandError("File not found: {}".format(filename))
        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format in file: {}".format(filename))
            
        duplicates = 0
        created = 0
        for challenge in data:
            try:
                Challenge.objects.create(**challenge)
                created += 1
            except IntegrityError:
                duplicates += 1
                self.stdout.write(self.style.WARNING(
                    "Duplicate entry skipped: {}".format(challenge.get("name"))
                ))
                
        self.stdout.write(self.style.SUCCESS("Database populated successfully."))
        