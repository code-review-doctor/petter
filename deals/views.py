# Create your views here.
import datetime

from django import forms
from django.db.models import F
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView

from deals.models import Comment
from deals.models import Deal
from deals.models import Vote


def votes(request):
    if request.POST.get('action') == 'votes':

        deal_id = int(request.POST.get('deal_id'))
        button = request.POST.get('button')
        deal_o = Deal.objects.get(id=deal_id)

        if deal_o.voter.filter(id=request.user.id).exists():

            # Get the users current vote (True/False)
            q = Vote.objects.get(Q(deal_id=deal_id) & Q(user_id=request.user.id))
            # q = Vote.objects.get(Q(deal_id=4) & Q(user_id=1))
            evote = q.vote

            if evote == True:

                # Now we need action based upon what button pressed

                if button == 'vote_up':
                    deal_o.vote_up = F('vote_up') - 1
                    deal_o.voter.remove(request.user)
                    deal_o.save()
                    deal_o.refresh_from_db()
                    up = deal_o.vote_up
                    down = deal_o.vote_down
                    total = deal_o.get_voting_count()
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none', 'total': total})

                if button == 'vote_down':
                    # Change vote in Post
                    deal_o.vote_up = F('vote_up') - 1
                    deal_o.vote_down = F('vote_down') + 1
                    deal_o.save()

                    # Update Vote

                    q.vote = False
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    deal_o.refresh_from_db()
                    up = deal_o.vote_up
                    down = deal_o.vote_down
                    total = deal_o.get_voting_count()

                    return JsonResponse({'up': up, 'down': down, 'total': total})

            pass

            if evote == False:

                if button == 'vote_up':
                    # Change vote in Post
                    deal_o.vote_up = F('vote_up') + 1
                    deal_o.vote_down = F('vote_down') - 1
                    deal_o.save()

                    # Update Vote

                    q.vote = True
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    deal_o.refresh_from_db()
                    up = deal_o.vote_up
                    down = deal_o.vote_down
                    total = deal_o.get_voting_count()
                    return JsonResponse({'up': up, 'down': down, 'total': total})

                if button == 'vote_down':
                    deal_o.vote_down = F('vote_down') - 1
                    deal_o.voter.remove(request.user)
                    deal_o.save()
                    deal_o.refresh_from_db()
                    up = deal_o.vote_up
                    down = deal_o.vote_down
                    total = deal_o.get_voting_count()
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none', 'total': total})

        else:  # New selection

            if button == 'vote_up':
                deal_o.vote_up = F('vote_up') + 1
                deal_o.voter.add(request.user)
                deal_o.save()
                # Add new vote
                new = Vote(deal_id=deal_id, user_id=request.user.id, vote=True)
                new.save()
            else:
                # Add vote down
                deal_o.vote_down = F('vote_down') + 1
                deal_o.voter.add(request.user)
                deal_o.save()
                # Add new vote
                new = Vote(deal_id=deal_id, user_id=request.user.id, vote=False)
                new.save()

            # Return updated votes
            deal_o.refresh_from_db()
            up = deal_o.vote_up
            down = deal_o.vote_down
            total = deal_o.get_voting_count()

            return JsonResponse({'up': up, 'down': down, 'total': total})

    pass


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
