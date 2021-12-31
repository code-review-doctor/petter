import django_filters

from products.models import Product


class ProductsFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(method='wider_filter', label="Search")

    class Meta:
        model = Product
        fields = ['brand']

    def wider_filter(self, queryset, name, value):
        return Product.objects.filter(brand=value)
