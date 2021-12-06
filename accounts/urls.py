from django.urls import path

from accounts.views import UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile')
]
