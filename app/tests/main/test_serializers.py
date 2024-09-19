from collections import OrderedDict

import pytest
from django.contrib.gis.geos import Polygon

from main.models import PolygonModel
from main.serializers import PolygonModelSerializer


@pytest.mark.django_db
def test_polygon_model_serializer():
    polygon_geom = Polygon(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)))
    polygon_instance = PolygonModel.objects.create(
        name="Test Polygon", polygon=polygon_geom, crosses_antimeridian=False
    )

    serializer = PolygonModelSerializer(polygon_instance)

    expected_data = {
        "id": 2,
        "type": "Feature",
        "geometry": "SRID=4326;POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))",
        "properties": OrderedDict(
            {"name": "Test Polygon", "crosses_antimeridian": False}
        ),
    }

    assert serializer.data == expected_data
