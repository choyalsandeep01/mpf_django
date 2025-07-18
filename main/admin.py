from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'material', 'price', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'material', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'material']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active', 'price']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Technical Specifications', {
            'fields': ('material', 'size_range', 'pressure_rating', 'temperature_range', 'standards')
        }),
        ('Images', {
            'fields': ('image', 'gallery_image_1', 'gallery_image_2', 'gallery_image_3')
        }),
        ('Pricing & Status', {
            'fields': ('price', 'is_featured', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'phone', 'email']
    
    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company_name', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['client_name', 'company_name', 'testimonial']
    list_editable = ['is_active']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'company', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published', 'author', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at']

# Customize admin site
admin.site.site_header = "MPF - Stainless Steel Products"
admin.site.site_title = "MPF Admin"
admin.site.index_title = "Welcome to MPF Administration"