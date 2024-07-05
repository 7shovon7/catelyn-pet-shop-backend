from django.core.management.base import BaseCommand
from product.models import Category, Product
from core.utils import optimize_image_in_upload_model

class Command(BaseCommand):
    help = 'Optimize images for existing Category and Product objects'

    def handle(self, *args, **kwargs):
        self.stdout.write("Optimizing Category images...")
        for category in Category.objects.all():
            if category.image:
                self.stdout.write(f"Optimizing image for Category: {category.title}")
                optimized_image = optimize_image_in_upload_model(category.image, desired_height=300)
                category.image = optimized_image
                category.save()
        
        self.stdout.write("Optimizing Product images...")
        for product in Product.objects.all():
            if product.image:
                self.stdout.write(f"Optimizing image for Product: {product.title}")
                optimized_image = optimize_image_in_upload_model(product.image, desired_height=600)
                product.image = optimized_image
                product.save()
        
        self.stdout.write(self.style.SUCCESS("Optimization complete!"))
