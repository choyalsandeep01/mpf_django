import os
import json
from django.core.management.base import BaseCommand
from main.models import Category, Product
from django.utils.text import slugify
from django.conf import settings
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = 'Import categories and products from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before importing',
        )

    def handle(self, *args, **kwargs):
        if kwargs['clear']:
            self.stdout.write("Clearing existing data...")
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write("Existing data cleared.")

        # Step 1: Import categories
        self.stdout.write("Importing categories...")
        categories_file = os.path.join(settings.BASE_DIR, 'categories.json')
        
        if os.path.exists(categories_file):
            with open(categories_file, encoding='utf-8') as f:
                categories = json.load(f)
                category_count = 0
                for entry in categories:
                    fields = entry['fields']
                    obj, created = Category.objects.update_or_create(
                        pk=entry['pk'],
                        defaults={
                            'name': fields['name'],
                            'slug': fields.get('slug') or slugify(fields['name']),
                            'description': fields.get('description', ''),
                            'is_active': fields.get('is_active', True),
                            'created_at': parse_datetime(fields.get('created_at')) if fields.get('created_at') else None,
                        }
                    )
                    category_count += 1
                    if created:
                        self.stdout.write(f"Created category: {obj.name}")
                    else:
                        self.stdout.write(f"Updated category: {obj.name}")
                        
            self.stdout.write(f"Categories imported successfully. Total: {category_count}")
        else:
            self.stdout.write("categories.json not found, skipping categories import.")

        # Step 2: Import products from products_json/
        self.stdout.write("Importing products...")
        product_folder = os.path.join(settings.BASE_DIR, 'products_json')
        
        if not os.path.exists(product_folder):
            self.stdout.write(f"Error: {product_folder} directory not found!")
            return
            
        product_files = [f for f in os.listdir(product_folder) if f.endswith('.json')]
        
        if not product_files:
            self.stdout.write("No JSON files found in products_json directory!")
            return
            
        self.stdout.write(f"Found {len(product_files)} JSON files: {product_files}")
        
        total_products = 0
        
        for file in product_files:
            file_path = os.path.join(product_folder, file)
            self.stdout.write(f"Processing file: {file}")
            
            try:
                with open(file_path, encoding='utf-8') as f:
                    products = json.load(f)
                    file_product_count = 0
                    
                    for entry in products:
                        fields = entry['fields']
                        
                        # Check if category exists
                        try:
                            category = Category.objects.get(pk=fields['category'])
                        except Category.DoesNotExist:
                            self.stdout.write(f"Warning: Category with ID {fields['category']} not found for product {fields['name']}. Skipping.")
                            continue
                        
                        # Handle price conversion
                        price = None
                        if fields.get('price'):
                            try:
                                price = float(fields['price'])
                            except (ValueError, TypeError):
                                price = None
                        
                        
                        # Create unique slug based on name and material for better uniqueness
                        base_name = fields['name']
                        material = fields.get('material', 'SS304')
                        base_slug = slugify(f"{base_name}-{material}")
                        if not base_slug:
                            base_slug = fields.get('slug') or slugify(fields['name'])
                        
                        slug = base_slug
                        counter = 1
                        while Product.objects.filter(slug=slug).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1
                        
                        # Don't use pk from JSON, let Django auto-assign
                        # Check if product already exists by name and category
                        existing_product = Product.objects.filter(
                            name=fields['name'],
                            category=category
                        ).first()
                        
                        if existing_product:
                            # Update existing product
                            obj = existing_product
                            created = False
                            # Update fields
                            obj.slug = slug
                            obj.description = fields.get('description', '')
                            obj.short_description = fields.get('short_description', '')
                            obj.material = fields.get('material', 'SS304')
                            obj.size_range = fields.get('size_range', '')
                            obj.pressure_rating = fields.get('pressure_rating', '')
                            obj.temperature_range = fields.get('temperature_range', '')
                            obj.standards = fields.get('standards', '')
                            obj.image = fields.get('image', '')
                            obj.gallery_image_1 = fields.get('gallery_image_1') or None
                            obj.gallery_image_2 = fields.get('gallery_image_2') or None
                            obj.gallery_image_3 = fields.get('gallery_image_3') or None
                            obj.price = price
                            obj.is_featured = fields.get('is_featured', False)
                            obj.is_active = fields.get('is_active', True)
                            obj.meta_title = fields.get('meta_title', '')
                            obj.meta_description = fields.get('meta_description', '')
                            if fields.get('created_at'):
                                obj.created_at = parse_datetime(fields.get('created_at'))
                            if fields.get('updated_at'):
                                obj.updated_at = parse_datetime(fields.get('updated_at'))
                            obj.save()
                        else:
                            # Create new product
                            obj = Product.objects.create(
                                name=fields['name'],
                                slug=slug,
                                category=category,
                                description=fields.get('description', ''),
                                short_description=fields.get('short_description', ''),
                                material=fields.get('material', 'SS304'),
                                size_range=fields.get('size_range', ''),
                                pressure_rating=fields.get('pressure_rating', ''),
                                temperature_range=fields.get('temperature_range', ''),
                                standards=fields.get('standards', ''),
                                image=fields.get('image', ''),
                                gallery_image_1=fields.get('gallery_image_1') or None,
                                gallery_image_2=fields.get('gallery_image_2') or None,
                                gallery_image_3=fields.get('gallery_image_3') or None,
                                price=price,
                                is_featured=fields.get('is_featured', False),
                                is_active=fields.get('is_active', True),
                                meta_title=fields.get('meta_title', ''),
                                meta_description=fields.get('meta_description', ''),
                                created_at=parse_datetime(fields.get('created_at')) if fields.get('created_at') else None,
                                updated_at=parse_datetime(fields.get('updated_at')) if fields.get('updated_at') else None,
                            )
                            created = True
                        
                        file_product_count += 1
                        total_products += 1
                        
                        if created:
                            self.stdout.write(f"  Created product: {obj.name} - {obj.material} (ID: {obj.pk})")
                        else:
                            self.stdout.write(f"  Updated product: {obj.name} - {obj.material} (ID: {obj.pk})")
                    
                    self.stdout.write(f"Processed {file_product_count} products from {file}")
                    
            except json.JSONDecodeError as e:
                self.stdout.write(f"Error parsing JSON file {file}: {e}")
            except Exception as e:
                self.stdout.write(f"Error processing file {file}: {e}")
        
        self.stdout.write(f"Products imported successfully. Total products processed: {total_products}")
        
        # Final verification
        final_product_count = Product.objects.count()
        final_category_count = Category.objects.count()
        self.stdout.write(f"Final database counts - Categories: {final_category_count}, Products: {final_product_count}")