from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Contact, Newsletter

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name *'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email *'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject *'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message *'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-3'),
                Column('email', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-3'),
                Column('company', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'subject',
            'message',
            Submit('submit', 'Send Message', css_class='btn btn-primary')
        )

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        }