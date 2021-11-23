# Create your views here.
from django.views.generic import ListView

from deals.models import Deal


class DealListView(ListView):
    model = Deal
    template_name = 'deal/deal_list.html'
    context_object_name = 'deals'

