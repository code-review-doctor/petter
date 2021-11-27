from django.urls import path

from deals import views
from deals.views import DealCreateView
from deals.views import DealDeleteView
from deals.views import DealListView
from deals.views import NewDealDetailView

urlpatterns = [
    path('', DealListView.as_view(), name='list'),
    path('deal/<int:pk>/', NewDealDetailView.as_view(), name='detail'),
    path('deal/delete/<int:pk>/', DealDeleteView.as_view(), name='delete'),
    path('deal/new/', DealCreateView.as_view(), name='new'),
    path('deal/vote/', views.vote_view, name='vote')
]
