from django.urls import path

from deals.views import DealCreateView
from deals.views import DealDetailView
from deals.views import DealListView

urlpatterns = [
    path('', DealListView.as_view(), name='list'),
    path('deal/<int:pk>/', DealDetailView.as_view(), name='detail'),
    path('deal/new/', DealCreateView.as_view(), name='new'),
]
