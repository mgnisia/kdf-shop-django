from django.contrib import admin

from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)