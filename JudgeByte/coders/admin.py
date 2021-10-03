from django.contrib import admin
from coders.models import UserProfile, Faqs
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Faqs)
