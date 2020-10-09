from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from time import sleep


class Command(BaseCommand):
    """This command waits until the database can be reached"""

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database...")
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default'].cursor()
            except OperationalError:
                self.stdout.write(
                    "Database unavailable, waiting for 1 second..."
                )
                sleep(1)

        self.stdout.write(self.style.SUCCESS("Database connected!"))
