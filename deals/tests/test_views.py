import datetime
from unittest import skip

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse
from django.utils import timezone

from deals.models import Deal
from deals.views import vote_view

User = get_user_model()


class DealViewTestCase(TestCase):
    DEAL_DETAIL = 'deals:detail'
    DEAL_VOTE = 'deals/vote/'

    def setUp(self):
        today = timezone.now()
        self.factory = RequestFactory()
        self.custom_user = User.objects.create_user(
            username='test',
            first_name='test name',
            email='test@test.test',
            password='password',
            is_active=True,
        )

        self.deal_1 = Deal.objects.create(
            name='Deal 1',
            description='{"delta":"{\\"ops\\":[{\\"insert\\":\\"this is a test!\\"},'
                        '{\\"insert\\":\\"\\\\n\\"}]}","html":"<p>this is a test!</p>"}',
            link='http://localhost:8000/link/',
            product_img='http://localhost:8000/link/avatar',

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

    def test_deal_detail_can_add_comment_view(self):
        login = self.client.login(username='test', password='password')
        self.assertTrue(login)
        response_post = self.client.post(reverse(self.DEAL_DETAIL, args=[self.deal_1.id]), {
            'comment': 'test comment'
        })
        self.assertEqual(response_post.status_code, 302)
        response_get = self.client.get(reverse(self.DEAL_DETAIL, args=[self.deal_1.id]))
        self.assertContains(response_get, 'test comment')

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

    @skip
    def test_deal_create_deal_view(self):
        login = self.client.login(username='test', password='password')
        self.assertTrue(login)
        response = self.client.post(reverse('deals:new'), {
            'name': 'Deal 2',
            'description': 'test123',
            'link': 'http://localhost:8000/link/',
            'product_img': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),

            'current_price_0': 20.00,
            'current_price_1': 'PLN',
            'historical_price_0': 100.00,
            'historical_price_1': 'PLN',
            'delivery_cost_0': 10.00,
            'delivery_cost_1': 'PLN',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Deal.objects.last().name, 'Deal 2')

    def test_deal_detail_view(self):
        response = self.client.get(reverse(self.DEAL_DETAIL, args=[self.deal_1.id]))
        self.assertEqual(response.status_code, 200)

    def test_guest_cant_vote_on_deal(self):
        response_post = self.client.post(self.DEAL_VOTE, {
            'action': 'vote',
            'deal_id': '1',
            'button': 'vote_up'
        })
        self.assertEqual(response_post.status_code, 404)

    def test_user_can_vote_on_deal_first_time(self):
        deal_vote_up_old = self.deal_1.vote_up
        request = self.factory.post(self.DEAL_VOTE, {
            'action': 'votes',
            'deal_id': self.deal_1.id,
            'button': 'vote_up',
        })
        request.user = self.custom_user
        response = vote_view(request)
        self.assertEqual(response.status_code, 200)
        self.deal_1.refresh_from_db()
        self.assertGreater(self.deal_1.vote_up, deal_vote_up_old)

    def test_user_cant_vote_up_twice_for_same_deal(self):
        deal_vote_up_old = self.deal_1.vote_up
        request = self.factory.post(self.DEAL_VOTE, {
            'action': 'votes',
            'deal_id': self.deal_1.id,
            'button': 'vote_up',
        })
        request.user = self.custom_user
        vote_view(request)
        vote_view(request)
        self.deal_1.refresh_from_db()
        self.assertEqual(deal_vote_up_old, self.deal_1.vote_up - 1)

    def test_user_can_delete_deal(self):
        self.client.login(username='test', password='password')
        response = self.client.post(reverse('deals:delete', kwargs={'pk': self.deal_1.id}))
        self.assertEqual(response.status_code, 302)
        null_response = self.client.get(reverse(self.DEAL_DETAIL, args=[self.deal_1.id]))
        self.assertEqual(null_response.status_code, 404)
