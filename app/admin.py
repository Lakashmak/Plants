from django.contrib import admin
from app.models import Product, User, Order, OrderProduct

# Register your models here.


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    pass

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    pass

@admin.register(OrderProduct)
class AdminOrderProduct(admin.ModelAdmin):
    pass
