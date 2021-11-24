from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):    
    class Meta:               
        model  = User
        exclude = ('password','user_permissions','groups','is_active','is_staff','is_superuser','last_login')