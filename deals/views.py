import datetime

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView

from deals.filters import DealFilter
from deals.models import Comment
from deals.models import Deal
from deals.models import Vote


@require_http_methods(["POST"])
def vote_view(request):
    if request.POST.get('action') == 'votes':
        deal_id = int(request.POST.get('deal_id'))
        user_vote = Vote.objects.filter(Q(user_id=request.user.uuid) & Q(deal_id=deal_id))
        button = request.POST.get('button')
        success_vote = None

        if not user_vote and button == 'vote_up':
            Vote.objects.create(deal_id=deal_id,
                                user_id=request.user.uuid,
                                vote_value=Vote.VoteChoice.PLUS)
            success_vote = button
        if not user_vote and button == 'vote_down':
            Vote.objects.create(deal_id=deal_id,
                                user_id=request.user.uuid,
                                vote_value=Vote.VoteChoice.MINUS)
            success_vote = button
        deal_o = Deal.objects.get(id=deal_id)
        return JsonResponse({'total': deal_o.get_voting_count(),
                             "vote": success_vote})
    else:
        return HttpResponse(status=422)


class DealList(ListView):
    queryset = Deal.objects.select_related('author', 'category').prefetch_related(
        Prefetch('comment_set', queryset=Comment.objects.all()))
    template_name = 'deals/deal_list.html'
    context_object_name = 'deals'
    ordering = ['-created_at', '-vote_up', '-vote_down']
    search_message = ''

    def get_context_data(self, **kwargs):
        context = super(DealList, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['filter'] = DealFilter(self.request.GET, queryset=self.get_queryset())

        return context


class HotDealListView(DealList):
    def get_context_data(self, **kwargs):
        context = super(HotDealListView, self).get_context_data(**kwargs)
        context['deals'] = Deal.deal_mgr.get_hot_deal(
            200,
        )
        return context


class DealListView(DealList):
    ...


class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    template_name = 'deals/deal_create.html'
    fields = ['name', 'description', 'link', 'product_img',
              'current_price', 'historical_price', 'delivery_cost',
              # 'valid_till' commented for mocking purpose
              ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        today = timezone.now()
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

    def get_queryset(self):
        qs = Deal.objects.all() \
            .select_related('author', 'category') \
            .prefetch_related(Prefetch('comment_set', queryset=Comment.objects.all().select_related('author'))) \
            .prefetch_related('vote_set')
        return qs

    def get_context_data(self, **kwargs):
        context = super(NewDealDetailView, self).get_context_data(**kwargs)
        comment_limit: int = self.request.GET.get('comment_limit', 20)
        page: int = self.request.GET.get('page', 1)

        context['form'] = CommentForm()

        comments = context['deal'].comment_set.all().order_by('-created_at')
        p = Paginator(comments, comment_limit)
        context['comments'] = p.get_page(page)
        votes = context['deal'].vote_set.filter(deal_id=self.object.id)
        context['votes'] = votes
        if not self.request.user.is_anonymous:
            have_voted = votes.filter(user_id=self.request.user.uuid).exists()
            if have_voted:
                have_voted = votes.get(user_id=self.request.user.uuid)
            context['have_voted'] = have_voted

        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        form = CommentForm(self.request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.deal = self.object
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            context = self.get_context_data(**kwargs)
            context.update({'form': form})
            return self.render_to_response(context)


class DealDeleteView(DeleteView):
    model = Deal
    success_url = reverse_lazy("deals:list")
    template_name_suffix = "_delete"


class UserDealListView(LoginRequiredMixin, DealList):

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.queryset = self.model.objects.filter(author__username=username)
        return super(UserDealListView, self).get_queryset()
