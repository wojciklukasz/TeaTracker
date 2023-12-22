from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Store)
admin.site.register(models.Type)
admin.site.register(models.Cultivar)
admin.site.register(models.Country)
admin.site.register(models.Province)
admin.site.register(models.Region)
admin.site.register(models.Tea)
admin.site.register(models.Brew)
admin.site.register(models.Image)
