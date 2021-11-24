# Create your views here.
import datetime

from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView

from deals.models import Comment
from deals.models import Deal


class DealListView(ListView):
    model = Deal
    template_name = 'deals/deal_list.html'
    context_object_name = 'deals'
    paginate_by = 5
    ordering = ['-created_at']


class DealCreateView(CreateView):
    model = Deal
    template_name = 'deals/deal_create.html'
    fields = ['name', 'description', 'link', 'product_img',
              'current_price', 'historical_price', 'delivery_cost',
              # 'valid_till' commented for mocking purpose
              ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        today = datetime.date.today()
        form.instance.valid_till = today + datetime.timedelta(8)
        return super().form_valid(form)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-3', 'id': 'comment_id'}))


class NewDealDetailView(DetailView):
    model = Deal
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        context = super(NewDealDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        comments = Comment.objects.filter(deal=self.object.id).order_by('-created_at')[:10]
        context['comments'] = comments
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        form = CommentForm(self.request.POST)
        print(form)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.deal = self.object
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(**kwargs)
            context.update({'form': form})
            return self.render_to_response(context)


class DealDetailView(DetailView):
    model = Deal
    template_name = 'deals/deal_detail.html'
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(deal=self.object.id).order_by('-created_at')[:10]
        context['comments'] = comments
        return context


class DealDeleteView(DeleteView):
    model = Deal
    success_url = reverse_lazy("deals:list")
    template_name_suffix = "_delete"
