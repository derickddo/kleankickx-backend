# services/admin.py
from django.contrib import admin
from .models import Service
from django import forms

class ServiceAdminForm(forms.ModelForm):
    """Custom form for the Service model in the admin interface."""
    image_file = forms.FileField(required=False, help_text="Upload an image (JPEG/PNG)")

    class Meta:
        model = Service
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            instance.image = image_file.read()  # Read file as bytes
        if commit:
            instance.save()
        return instance

class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = ['name', 'price', 'created_at']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'price', 'image_file']

admin.site.register(Service, ServiceAdmin)
