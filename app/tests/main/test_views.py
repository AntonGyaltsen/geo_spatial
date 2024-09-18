import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.gis.geos import Polygon
from main.models import PolygonModel


@pytest.mark.django_db
def test_polygon_view_add_record():
    client = Client()
    url = reverse('polygon_form')
    
    coordinates = "0.0 175.0, 0.0 185.0, 10.0 185.0, 10.0 175.0, 0.0 175.0"

    form_data = {
        'name': 'Test Polygon',
        'coordinates': coordinates,
        'latitude': 10.0,
        'longitude': 20.0,
        'polygon': 'POLYGON((0.0 175.0, 0.0 185.0, 10.0 185.0, 10.0 175.0, 0.0 175.0))',
    }
    
    response = client.post(url, data=form_data)

    assert response.status_code in [200, 302], f"Unexpected status code: {response.status_code}"
    
    polygons = PolygonModel.objects.all()
    print(f"Number of PolygonModel objects: {polygons.count()}")
    for polygon in polygons:
        print(f"Polygon: {polygon.name}, {polygon.polygon}, Crosses Antimeridian: {polygon.crosses_antimeridian}")
    
    assert PolygonModel.objects.count() == 1, "PolygonModel object was not created"
    polygon = PolygonModel.objects.first()
    assert polygon.name == 'Test Polygon'
    expected_coords = ((175.0, 0.0), (-175.0, 0.0), (-175.0, 10.0), (175.0, 10.0), (175.0, 0.0))
    assert polygon.polygon.coords[0] == expected_coords
    assert polygon.crosses_antimeridian
