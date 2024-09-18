from django.contrib import messages
from django.contrib.gis.geos import Polygon
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import PolygonForm
from .models import PolygonModel
from .serializers import PolygonModelSerializer


def polygon_view(request):
    if request.method == 'POST':
        form = PolygonForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Polygon saved successfully!')
                return redirect('polygon_form')
            except Exception as e:
                messages.error(request, f'Error saving polygon: {str(e)}')
        else:
            messages.error(request, 'Form is not valid. Please check the errors.')
    else:
        form = PolygonForm()

    return render(request, 'main/polygon_form.html', {'form': form})


def saved_polygons_view(request):
    polygons = PolygonModel.objects.all()

    processed_polygons = []
    for polygon in polygons:
        processed_polygons.append({
            'name': polygon.name,
            'coordinates': polygon.polygon.coords[0],
            'crosses_antimeridian': polygon.crosses_antimeridian,
        })

    return render(request, 'main/saved_polygons.html', {'polygons': processed_polygons})


class PolygonList(APIView):
    def post(self, request, format=None):
        serializer = PolygonModelSerializer(data=request.data)

        if serializer.is_valid():
            polygon_data = serializer.validated_data.get('polygon')

            coordinates = polygon_data['coordinates'][0]

            adjusted_coords, crosses_antimeridian = self.adjust_coordinates_for_antimeridian(
                coordinates)

            if adjusted_coords[0] != adjusted_coords[-1]:
                adjusted_coords.append(adjusted_coords[0])

            adjusted_polygon = Polygon(adjusted_coords)

            instance = serializer.save(polygon=adjusted_polygon,
                                       crosses_antimeridian=crosses_antimeridian)

            return Response(PolygonModelSerializer(instance).data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def adjust_coordinates_for_antimeridian(self, coordinates):
        adjusted_coords = []
        crosses_antimeridian = False

        for lon, lat in coordinates:
            if lon > 180:
                lon -= 360
                crosses_antimeridian = True
            elif lon < -180:
                lon += 360
                crosses_antimeridian = True
            adjusted_coords.append((lon, lat))

        return adjusted_coords, crosses_antimeridian
