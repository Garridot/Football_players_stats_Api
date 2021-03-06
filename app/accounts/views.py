#rest_framework
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics,authentication,permissions
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response



from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

#Login
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate,get_user_model
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm   

# Create Account
from .forms import *
 

# Create your views here.



class Register(FormView):
    template_name  = 'register.html'
    form_class     = UserForm
    success_url    = reverse_lazy('accounts:my_account') 

    def form_valid(self, form):         
        form.save()
        user = authenticate(username = form.cleaned_data['email'], password = form.cleaned_data['password1'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, user)        
        return super(Register,self).form_valid(form)

class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('accounts:my_account') 

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    def form_valid(self,form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)            

class Logout(APIView):   
    def get(self,request,format=None):        
        logout(request)
        return Response(status=status.HTTP_200_OK)
        

class MyAccount(TemplateView):
    template_name = "my_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = Token.objects.get(user=self.request.user)
        return context
    

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
  
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer 
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES 

class ManagerUserView(generics.RetrieveAPIView):
    # Manage the authenticated user
    serializer_class = UserSerializer
    authentication_class = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user 