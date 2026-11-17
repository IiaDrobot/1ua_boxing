
from django.contrib import admin
from django.urls import path
from main.views import home, training_signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', training_signup, name='training_signup'),
]

