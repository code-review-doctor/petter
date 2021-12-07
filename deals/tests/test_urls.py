from unittest import TestCase

from django.urls import resolve
from django.urls import reverse

from deals.views import DealCreateView
from deals.views import DealDeleteView
from deals.views import DealListView
from deals.views import HotDealListView
from deals.views import UserDealListView
from deals.views import vote_view


class TestUrls(TestCase):

    def test_deal_list_url_resolves(self):
        url = reverse('deals:list')
        self.assertEqual(resolve(url).func.view_class, DealListView)

    def test_deal_hot_list_url_resolves(self):
        url = reverse('deals:hot_list')
        self.assertEqual(resolve(url).func.view_class, HotDealListView)

    def test_deal_user_url_resolves(self):
        url = reverse('deals:user_deals', args=['1'])
        self.assertEqual(resolve(url).func.view_class, UserDealListView)

    def test_deal_delete_url_resolves(self):
        url = reverse('deals:delete', args=['1'])
        self.assertEqual(resolve(url).func.view_class, DealDeleteView)

    def test_deal_create_url_resolves(self):
        url = reverse('deals:new')
        self.assertEqual(resolve(url).func.view_class, DealCreateView)

    def test_deal_vote_url_resolves(self):
        url = reverse('deals:vote')
        self.assertEqual(resolve(url).func, vote_view)
