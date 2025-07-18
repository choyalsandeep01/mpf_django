from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import ContactForm, NewsletterForm

def get_company_info():
    try:
        return CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        return None

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    recent_blogs = BlogPost.objects.filter(is_published=True)[:3]
    company_info = get_company_info()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'testimonials': testimonials,
        'recent_blogs': recent_blogs,
        'company_info': company_info,
    }
    return render(request, 'index.html', context)

def products(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    material = request.GET.get('material')
    
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(material__icontains=search_query)
        )
    
    if material:
        products = products.filter(material=material)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    materials = Product.MATERIAL_CHOICES
    company_info = get_company_info()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'materials': materials,
        'current_category': category_slug,
        'search_query': search_query,
        'current_material': material,
        'company_info': company_info,
    }
    return render(request, 'products.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    company_info = get_company_info()
    
    context = {
        'product': product,
        'related_products': related_products,
        'company_info': company_info,
    }
    return render(request, 'product_detail.html', context)

def about(request):
    company_info = get_company_info()
    testimonials = Testimonial.objects.filter(is_active=True)[:8]
    
    context = {
        'company_info': company_info,
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            try:
                send_mail(
                    f'New Contact Form Submission: {contact.subject}',
                    f'''
                    Name: {contact.name}
                    Email: {contact.email}
                    Phone: {contact.phone}
                    Company: {contact.company}
                    
                    Message:
                    {contact.message}
                    ''',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    company_info = get_company_info()
    
    context = {
        'form': form,
        'company_info': company_info,
    }
    return render(request, 'contact.html', context)

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect('home')