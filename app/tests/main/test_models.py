import pytest
from django.contrib.gis.geos import Polygon

from main.models import PolygonModel


@pytest.mark.django_db
def test_polygon_model():
    polygon_geom = Polygon(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)))

    polygon = PolygonModel(name="test_1", polygon=polygon_geom)
    polygon.save()

    assert polygon.name == "test_1"
    assert str(polygon) == polygon.name
