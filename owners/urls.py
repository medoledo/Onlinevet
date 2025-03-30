from django.urls import path
from .views import add_owner

urlpatterns = [
    path("add/", add_owner, name="add_owner"),
]
