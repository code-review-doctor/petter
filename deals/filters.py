import django_filters
from django.db.models import Q

from deals.models import Deal


class DealFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='wider_filter', label="Search")

    class Meta:
        model = Deal
        fields = ['q']

    def wider_filter(self, queryset, name, value):
        return Deal.objects.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )
