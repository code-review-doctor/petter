import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from deals.models import Deal

User = get_user_model()


class TestDealSModel(TestCase):
    def setUp(self) -> None:
        self.current_day = timezone.now()
        self.custom_user = User.objects.create(
            username='test',
            password='password',
            first_name='test name',
            email='test@test.test',
        )
        self.deal1 = Deal.objects.create(
            name='Deal 1',
            description='Description',
            link='http://localhost:8000/link/',
            product_img='http://localhost:8000/link/',

            current_price=20.00,
            historical_price=100.00,
            delivery_cost=10.00,
            author=self.custom_user,

            valid_till=self.current_day + datetime.timedelta(8),
            created_at=self.current_day,
            promo_code="promo_code",
            active=True,

            vote_up=200,
            vote_down=100,
        )

    def test_computing_price_percentage(self):
        self.assertEqual(self.deal1.price_percentage(), 80.0)
