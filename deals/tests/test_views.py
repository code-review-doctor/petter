import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from deals.models import Deal

User = get_user_model()


class DealViewTestCase(TestCase):
    def setUp(self):
        today = timezone.now()

        self.custom_user = User.objects.create_user(
            username='test',
            first_name='test name',
            email='test@test.test',
            password='password',
            is_active=True,
        )

        self.deal_1 = Deal.objects.create(
            name='Deal 1',
            description='Description',
            link='http://localhost:8000/link/',
            product_img='http://localhost:8000/link/',

            current_price=20.00,
            historical_price=100.00,
            delivery_cost=10.00,
            author=self.custom_user,

            valid_till=today + datetime.timedelta(8),
            created_at=today,
            promo_code="promo_code",
            active=True,

            vote_up=200,
            vote_down=100,
        )

    def test_deal_list(self):
        response = self.client.get(reverse("deals:list"))
        self.assertEqual(response.status_code, 200)

    def test_deal_create_view_not_logged(self):
        response = self.client.get(reverse("deals:new"))
        self.assertEqual(response.status_code, 302)

    def test_deal_create_view_logged(self):
        login = self.client.login(username='test', password='password')
        self.assertTrue(login)
        response = self.client.get(reverse("deals:new"))
        self.assertEqual(response.status_code, 200)

    def test_deal_create_deal_view(self):
        login = self.client.login(username='test', password='password')
        self.assertTrue(login)
        response = self.client.post(reverse('deals:new'), {
            'name': 'Deal 2',
            'description': 'Description',
            'link': 'http://localhost:8000/link/',
            'product_img': 'http://localhost:8000/link/',

            'current_price': 20.00,
            'historical_price': 100.00,
            'delivery_cost': 10.00,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Deal.objects.last().name, 'Deal 2')
