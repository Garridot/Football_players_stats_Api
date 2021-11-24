from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    def test_create_user_successful(self):
        email    = 'test@gmail.com'
        password = 'Tests123'
        user     = get_user_model().objects.create_user(
            email = email, password = password
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_email_normalized(self):
        email = 'test@gmail.com'
        password = 'Tests123'
        user     = get_user_model().objects.create_user(
            email = email, password = password
        )
        self.assertEqual(user.email,email.lower())

    def test_invalid_email(self):
        with self.assertRaises(ValueError):             
            email = None
            password = 'Tests123'
            user     = get_user_model().objects.create_user(
                email = email, password = password
            ) 
    def test_superuser(self):
        email = 'test@gmail.com'
        password = 'Tests123'
        user     = get_user_model().objects.create_superuser(
            email = email, password = password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        

             

