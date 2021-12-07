# Create your tests here.
# import datetime
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase
#
# from deals.models import Deal
#
# User = get_user_model()
#
#
# class DealTestCase(TestCase):
#     def setUp(self):
#         today = datetime.date.today()
#         custom_user = User.objects.create(
#             username='test',
#             password='password',
#             first_name='test name',
#             email='test@test.test',
#         )
#         Deal.objects.create(
#             name='Deal 1',
#             description='Description',
#             link='http://localhost:8000/link/',
#             product_img='http://localhost:8000/link/',
#
#             current_price=20.00,
#             historical_price=100.00,
#             delivery_cost=10.00,
#             author=custom_user,
#
#             valid_till=today + datetime.timedelta(8),
#             created_at=today,
#             promo_code="promo_code",
#             active=True,
#
#             vote_up=200,
#             vote_down=100,
#         )
#
#     def test_user_created_deal(self):
#         user = User.objects.get(username='test')
#         deal = Deal.objects.get(name='Deal 1')
#         self.assertEqual(deal.author.id, user.id)
