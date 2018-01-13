from django.contrib import admin

# Register your models here.
from .models import FreshSheet, Farm, FoodItem

admin.site.register(FreshSheet)
admin.site.register(Farm)
admin.site.register(FoodItem)
