from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Product

User = get_user_model()

class Command(BaseCommand):
    help = "Create demo user and seed products"

    def handle(self, *args, **options):
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user("demo", password="password123", email="demo@example.com")
            self.stdout.write(self.style.SUCCESS("Created user demo / password123"))
        else:
            self.stdout.write("User demo exists")

        if Product.objects.count() == 0:
            Product.objects.create(name="Alpha", description="First product", price=10.0)
            Product.objects.create(name="Beta", description="Second product", price=20.0)
            Product.objects.create(name="Gamma", description="Third product", price=30.0)
            self.stdout.write(self.style.SUCCESS("Seeded 3 products"))
        else:
            self.stdout.write("Products already present")
