from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import CustomUser

User: CustomUser = get_user_model()


class TestsUser(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='tester',
            first_name='test',
            last_name='testowy',
            age=50,
            avatar='http://test.com/avatr.jpg',
            email='test@test.com',
            password='password'
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'tester')
        self.assertEqual(self.user.first_name, 'test')
        self.assertEqual(self.user.last_name, 'testowy')
        self.assertEqual(self.user.avatar, 'http://test.com/avatr.jpg')
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.age, 50)

    def test_delete_user(self):
        user = User.objects.get(username='tester')
        self.assertEqual(self.user.username, 'tester')
        user.delete()
        delete_user = User.objects.filter(username='tester')
        self.assertEqual(delete_user.count(), 0)

    def test_get_initials_has_first_and_last_name(self):
        initials = self.user.get_initials()
        self.assertEqual('TT', initials)

    def test_get_initials_has_not_first_and_last_name(self):
        self.user.first_name = ''
        self.user.last_name = ''
        self.user.save(update_fields=['first_name', 'last_name'])
        initials = self.user.get_initials()
        self.assertEqual('T', initials)
