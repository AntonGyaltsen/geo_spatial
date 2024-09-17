from django import forms
from django.contrib.gis.geos import Polygon, Point
from main.models import PolygonModel


class PolygonForm(forms.Form):
    name = forms.CharField(max_length=255)
    latitude = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Latitude'}))
    longitude = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Longitude'}))
    coordinates = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}))

    def save(self):
        name = self.cleaned_data['name']
        coordinates = self.cleaned_data['coordinates']

        try:
            points = [
                Point(float(lat), float(lon)) for lat, lon in [coord.split() for coord in coordinates.split(',')]
            ]

            if len(points) < 3:
                raise ValueError("A polygon must have at least 3 points")

            if points[0] != points[-1]:
                points.append(points[0])

            polygon = Polygon(points)
            return PolygonModel.objects.create(name=name, polygon=polygon)
        except ValueError as e:
            raise forms.ValidationError(f"Invalid coordinates: {str(e)}")