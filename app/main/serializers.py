from django.contrib.gis.geos import Polygon
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from main import utils
from main.models import PolygonModel

class PolygonModelSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PolygonModel
        fields = ('id', 'name', 'polygon', 'crosses_antimeridian')
        geo_field = 'polygon'
        read_only_fields = ('crosses_antimeridian',)

    def update(self, instance, validated_data):
        if 'polygon' in validated_data:
            polygon_data = validated_data.pop('polygon')

            coordinates = polygon_data['coordinates'][0]
            adjusted_coords, crosses_antimeridian = (
                utils.adjust_coordinates_for_antimeridian(
                coordinates))

            if adjusted_coords[0] != adjusted_coords[-1]:
                adjusted_coords.append(adjusted_coords[0])

            adjusted_polygon = Polygon(adjusted_coords)

            instance.polygon = adjusted_polygon
            instance.crosses_antimeridian = crosses_antimeridian

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
