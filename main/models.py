from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['created_at']  # ✅ This shows older categories first

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    MATERIAL_CHOICES = [
        ('SS304', 'Stainless Steel 304'),
        ('SS316', 'Stainless Steel 316'),
        ('SS316L', 'Stainless Steel 316L'),
        ('SS321', 'Stainless Steel 321'),
        ('SS347', 'Stainless Steel 347'),
        ('SS904L', 'Stainless Steel 904L'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    material = models.CharField(max_length=10, choices=MATERIAL_CHOICES, default='SS304')
    size_range = models.CharField(max_length=200, help_text="e.g., 1/2 inch to 24 inch")
    pressure_rating = models.CharField(max_length=100, blank=True)
    temperature_range = models.CharField(max_length=100, blank=True)
    standards = models.CharField(max_length=200, blank=True, help_text="e.g., ASTM, ASME, DIN")
    image = models.ImageField(upload_to='products/')
    gallery_image_1 = models.ImageField(upload_to='products/gallery/', blank=True, null=True)
    gallery_image_2 = models.ImageField(upload_to='products/gallery/', blank=True, null=True)
    gallery_image_3 = models.ImageField(upload_to='products/gallery/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.short_description:
            self.short_description = self.description[:200] + "..." if len(self.description) > 200 else self.description
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name

class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=100, default="MPF")
    tagline = models.CharField(max_length=200, blank=True)
    about_us = models.TextField()
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    established_year = models.IntegerField(blank=True, null=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    favicon = models.ImageField(upload_to='company/', blank=True, null=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"
    
    def __str__(self):
        return self.company_name

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.company_name}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True)
    featured_image = models.ImageField(upload_to='blog/')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt:
            self.excerpt = self.content[:200] + "..." if len(self.content) > 200 else self.content
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title