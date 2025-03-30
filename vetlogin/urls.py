from django.urls import path
from . import views
urlpatterns = [
    path('' , views.vetlogin , name='login' ),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),

]