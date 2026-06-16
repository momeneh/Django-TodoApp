from django.core.management.base import BaseCommand
from faker import Faker
import random

from accounts.models import User
from todo.models import Task


class Command(BaseCommand):
    help = "inserting some data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        # return super().handle(*args, **options)
        user = User.objects.create_user(email=self.faker.email(), password="1234!@#$")

        for _ in range(5):
            Task.objects.create(
                title=self.faker.paragraph(nb_sentences=1),
                user=user,
                done=random.choice([True, False]),
            )
