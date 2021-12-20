import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from deals.models import Deal
from deals.models import Vote

User = get_user_model()


class TestDealsModel(TestCase):
    DEAL_1 = 'Deal 1'

    def setUp(self) -> None:
        self.current_day = timezone.now()
        self.custom_user = User.objects.create(
            username='test',
            password='password',
            first_name='test name',
            email='test@test.test',
        )
        self.deal1 = Deal.objects.create(
            name=self.DEAL_1,
            description='{"delta":"{\\"ops\\":[{\\"insert\\":\\"this is a test!\\"},'
                        '{\\"insert\\":\\"\\\\n\\"}]}","html":"<p>this is a test!</p>"}',
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

    def test_computing_vote_count(self):
        self.assertEqual(self.deal1.get_voting_count(), 100)

    def test_user_cant_vote(self):
        self.assertFalse(self.deal1.can_vote(user_id=self.custom_user.uuid), False)

    def test_user_can_vote(self):
        Vote.objects.create(
            deal=self.deal1,
            user=self.custom_user,
            vote_value=Vote.VoteChoice.PLUS,
        )
        self.assertTrue(self.deal1.can_vote(user_id=self.custom_user.uuid), True)

    def test_vote_plus_increase_deal_vote_counter(self):
        deal = Deal.objects.get(name=self.DEAL_1)
        deal.vote_up = 400
        deal.save(update_fields=['vote_up'])

        Vote.objects.create(
            deal=deal,
            user=self.custom_user,
            vote_value=Vote.VoteChoice.PLUS,
        )
        deal.refresh_from_db()
        self.assertEqual(deal.vote_up, 401)

    def test_vote_minus_decrease_deal_vote_counter(self):
        deal = Deal.objects.get(name=self.DEAL_1)
        deal.vote_down = 100
        deal.save(update_fields=['vote_down'])

        Vote.objects.create(
            deal=deal,
            user=self.custom_user,
            vote_value=Vote.VoteChoice.MINUS,
        )
        deal.refresh_from_db()
        self.assertEqual(deal.vote_down, 101)

    def test_deleting_vote_decrease_deal_vote_counter(self):
        deal = Deal.objects.get(name=self.DEAL_1)
        deal.vote_down = 10
        deal.save(update_fields=['vote_down'])

        vote = Vote.objects.create(
            deal=deal,
            user=self.custom_user,
            vote_value=Vote.VoteChoice.MINUS,
        )
        deal.refresh_from_db()
        self.assertEqual(deal.vote_down, 11)
        vote.delete()
        deal.refresh_from_db()
        self.assertEqual(deal.vote_down, 10)

    def test_deal_vote_down_counter_cant_be_lower_than_zero(self):
        deal = Deal.objects.get(name=self.DEAL_1)
        deal.vote_down = -50
        deal.save()
        self.assertEqual(deal.vote_down, 0)

    def test_deal_vote_up_counter_cant_be_lower_than_zero(self):
        deal = Deal.objects.get(name=self.DEAL_1)
        deal.vote_up = -10
        deal.save()
        self.assertEqual(deal.vote_up, 0)
