from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import FreshSheet, Farm, FoodItem, User, Order, OrderItem

admin.site.register(FreshSheet)
admin.site.register(Farm)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User, UserAdmin)
