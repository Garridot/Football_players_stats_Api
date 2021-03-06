from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns=[
    path('create/',views.CreateUserView.as_view(),name='create'),
    path('token/',views.CreateTokenView.as_view(),name='token'),    
    path('login/',views.Login.as_view(),name='login'),
    path('register/',views.Register.as_view()),
    path('logout/',views.Logout.as_view()),
    path('my_account',views.MyAccount.as_view(),name='my_account')


]