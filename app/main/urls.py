from django.urls import path
from .views import polygon_view

namespace = 'main'

urlpatterns = [
    path('add-polygon/', polygon_view, name='polygon_form'),
]