from rest_framework_gis.serializers import GeoFeatureModelSerializer
from main.models import PolygonModel

class PolygonModelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PolygonModel
        fields = ('id', 'name', 'polygon', 'crosses_antimeridian')
        geo_field = 'polygon'