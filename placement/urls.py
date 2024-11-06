from django.urls import path
from .views import build_new_tree

urlpatterns = [
    path('', build_new_tree, name='build_new_tree'),
]
