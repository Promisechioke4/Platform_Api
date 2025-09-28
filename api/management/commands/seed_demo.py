from django.core.management.base import BaseCommand
from api.models import Product


class Command(BaseCommand):
    help = "Seed database with sample products"

    def handle(self, *args, **kwargs):
        products = [
            {"name": "Laptop", "price": 250000, "description": "Core i7, 16GB RAM"},
            {"name": "Smartphone", "price": 120000, "description": "Android 13, 128GB"},
            {"name": "Headphones", "price": 15000, "description": "Noise cancelling"},
        ]

        for p in products:
            Product.objects.get_or_create(name=p["name"], defaults=p)

        self.stdout.write(self.style.SUCCESS("Products seeded successfully!"))
