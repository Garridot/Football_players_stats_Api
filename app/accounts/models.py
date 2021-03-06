from os import pipe
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):    
    def create_user(self,email,password=None,**extra_field):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email),**extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)

        return user            

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email' 
