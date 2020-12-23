from django.contrib import admin
from .models import Cv, Update, Notes

# Register your models here.
admin.site.register(Notes)
admin.site.register(Update)
admin.site.register(Cv)