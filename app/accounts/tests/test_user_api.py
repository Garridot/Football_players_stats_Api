


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('accounts:create')
TOKEN_URL       = reverse('accounts:token')
MY_ACCOUNT_URL  = reverse('accounts:my_account')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {'email':'test@gmail.com','password':'Tests123'}
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)    
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data) 

    def  test_if_user_exists(self): 
        payload = {'email':'test@gmail.com','password':'Tests123'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST) 

    def test_password_too_short(self):
        payload = {'email':'test@gmail.com','password':'Ts'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST) 

    def test_token_user_create(self): 
        payload = {'email':'test@gmail.com','password':'Tests123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)  

    def test_token_invalid_credentials(self):
        create_user(email='test@gmail.com',password='Tests123')
        payload = {'email':'test@gmail.com','password':'Wrong123'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_crete_token_no_user(self):
        payload = {'email':'test@gmail.com','password':'Tests123'}
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST) 

    def test_token_missing_field(self):        
        res = self.client.post(TOKEN_URL,{'email':'test','password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    # def test_user_unauthorized(self):
    #     res = self.client.get(MY_ACCOUNT_URL)
    #     self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)




class PrivateUserApiTest(TestCase):
    def setUp(self):
        self.user = create_user(email='test@gmail.com',password='Tests123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_account_success(self):
        res = self.client.get(MY_ACCOUNT_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'email':self.user.email
        })
        
    def test_post_me_not_allowed(self):
        res = self.client.post(MY_ACCOUNT_URL,{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    # def test_update_account(self):
    #     payload = {'email':'newtest@gmail.com','password':'newtests123'}

    #     res = self.client.patch(MY_ACCOUNT_URL,payload)
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.email,payload['email']) 
    #     self.assertTrue(self.user.check_password(payload['password']))
    #     self.assertEqual(res.status_code,status.HTTP_200_OK)   





        
