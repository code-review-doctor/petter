from django.urls import path

from deals.views import DealListView

urlpatterns = [
    path('', DealListView.as_view(), name='list')
]
