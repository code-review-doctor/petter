# Create your views here.
from django.db.models import Prefetch
from django.views.generic import DetailView
from django.views.generic import ListView

from products.filters import ProductsFilter
from products.models import Brand
from products.models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        query = self.request.GET.get('deal')
        if query:
            context['filter'] = ProductsFilter(self.request.GET, queryset=self.get_queryset())

        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'


class BrandListView(ListView):
    queryset = Brand.objects.prefetch_related(Prefetch('product_set', queryset=Product.objects.all()))
    context_object_name = 'brands'
    template_name = 'brands/brand_list.html'
    paginate_by = 20


class BrandDetailView(DetailView):
    model = Brand
    context_object_name = 'brand'
    template_name = 'brands/brand_detail.html'
