from django.core.management.base import BaseCommand
from cars_app.models import Car
from faker import Faker
import random

class Command(BaseCommand):
    help = 'توليد 100 سيارة عشوائية'

    def handle(self, *args, **kwargs):
        fake = Faker('ar_SA')
        colors = ['أحمر', 'أزرق', 'أبيض', 'أسود', 'فضي', 'رمادي']
        models = ['2020', '2021', '2022', '2023', '2024', '2025']

        for _ in range(100):
            Car.objects.create(
                name=fake.company(),
                model=random.choice(models),
                color=random.choice(colors),
                price=random.randint(20000, 100000)
            )

        self.stdout.write(self.style.SUCCESS('✅ تم إدخال 100 سيارة بنجاح.'))
