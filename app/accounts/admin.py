from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display  = ('id','email','is_active','is_staff',)    
    search_fields = ('email',)
    list_filter   = ('is_active','is_staff')

admin.site.register(User,UserAdmin)    