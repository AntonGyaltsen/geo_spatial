from django.contrib.messages import api
from django.urls import path
from .views import polygon_view, saved_polygons_view, PolygonList

namespace = 'main'

urlpatterns = [
    path('add-polygon/', polygon_view, name='polygon_form'),
    path('saved-polygons/', saved_polygons_view, name='saved_polygons'),
    path('api/add/', PolygonList.as_view(), name='api_add'),
]