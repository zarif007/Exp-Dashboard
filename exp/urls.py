from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_expenses', views.add_expenses, name='add_expenses'),
]
