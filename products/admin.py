from django.contrib import admin

# Register your models here.
from products.models import Brand
from products.models import Price
from products.models import Product


class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand', 'slug', 'website']


admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Brand, BrandAdmin)
