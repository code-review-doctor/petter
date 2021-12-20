from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from deals.models import Comment
from deals.models import Deal
from users.admin import CustomUser


class UserProfileView(DetailView):
    model: CustomUser = get_user_model()
    template_name = 'account/profile_detail.html'
    context_object_name = 'profile'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(author_id=user.uuid)
        context['deals'] = Deal.objects.filter(author_id=user.uuid)

        return context
