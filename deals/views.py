# Create your views here.
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from deals.models import Comment
from deals.models import Deal


class DealListView(ListView):
    model = Deal
    template_name = 'deals/deal_list.html'
    context_object_name = 'deals'


class DealCreateView(CreateView):
    model = Deal
    template_name = 'deals/deal_create.html'
    fields = [
        'name',
        'description', 'link',
        'current_price', 'historical_price', 'delivery_cost',
        'valid_till'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DealDetailView(DetailView):
    model = Deal
    template_name = 'deals/deal_detail.html'
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(deal=self.object.id).order_by('-created_at')[:10]
        context['comments'] = comments
        return context
