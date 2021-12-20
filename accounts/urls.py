from django.urls import path

from accounts.views import UserProfileView

urlpatterns = [
    path('<slug:username>', UserProfileView.as_view(), name='profile')
]
