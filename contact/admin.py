from django.contrib import admin
from .models import Contact

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'mail_address', 'content', 'created_at']

admin.site.register(Contact, ContactAdmin)
