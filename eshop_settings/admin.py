from django.contrib import admin
from .models import SiteSetting, SocialMedia

# Register your models here.

admin.site.register(SiteSetting)
admin.site.register(SocialMedia)
