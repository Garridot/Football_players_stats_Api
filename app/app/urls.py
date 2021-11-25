from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player_stats/api/',include('api.urls')),
    path('player_stats/',include('accounts.urls'))
]
