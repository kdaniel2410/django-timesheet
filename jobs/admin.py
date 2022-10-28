from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Job)
admin.site.register(models.Period)
admin.site.register(models.Shift)
