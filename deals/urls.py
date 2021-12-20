from django.urls import path

from deals import views
from deals.views import DealCreateView
from deals.views import DealDeleteView
from deals.views import DealListView
from deals.views import HotDealListView
from deals.views import NewDealDetailView
from deals.views import UserDealListView

urlpatterns = [
    path('', DealListView.as_view(), name='list'),
    path('deals/hot/', HotDealListView.as_view(), name='hot_list'),
    path('deals/user/<str:username>/', UserDealListView.as_view(), name='user_deals'),
    path('deals/<int:pk>/', NewDealDetailView.as_view(), name='detail'),
    path('deals/delete/<int:pk>/', DealDeleteView.as_view(), name='delete'),
    path('deals/new/', DealCreateView.as_view(), name='new'),
    path('deals/vote/', views.vote_view, name='vote'),
]
