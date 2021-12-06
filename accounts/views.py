from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from deals.models import Comment
from deals.models import Deal
from users.admin import CustomUser


class UserProfileView(DetailView):
    model: CustomUser = get_user_model()
    template_name = 'account/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        if not self.kwargs.get(self.pk_url_kwarg):
            self.kwargs.setdefault('pk', self.request.user.id)
        return super(UserProfileView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(author_id=user.id)
        context['deals'] = Deal.objects.filter(author_id=user.id)

        return context
