from django.urls import path
from .views import MainCreateView, MainListView, my_python_function  # Example: Adding a list view too

urlpatterns = [
    path('add/', MainCreateView.as_view(), name='add_main'),
    path('', MainListView.as_view(), name='main_list'),
    path('sendfile/', my_python_function, name='sendfile'),
]
