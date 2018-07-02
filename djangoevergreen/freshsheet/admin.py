from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import FreshSheet, Farm, FoodItem, User, Order, OrderItem, AccountRequest

admin.site.register(FreshSheet)
admin.site.register(Farm)
admin.site.register(FoodItem)
admin.site.register(OrderItem)
admin.site.register(User, UserAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2


class OrderAdmin(admin.ModelAdmin):
    fields = ['status']
    inlines = [OrderItemInline]




admin.site.register(Order, OrderAdmin)

admin.site.register(AccountRequest)