from django.contrib.messages import api
from django.urls import path

from .views import PolygonDetailView, PolygonList, polygon_view, saved_polygons_view

namespace = "main"

urlpatterns = [
    path("add-polygon/", polygon_view, name="polygon_form"),
    path("saved-polygons/", saved_polygons_view, name="saved_polygons"),
    path("api/polygons/", PolygonList.as_view(), name="api_add"),
    path("api/polygon/<int:pk>/", PolygonDetailView.as_view(), name="polygon-detail"),
]
