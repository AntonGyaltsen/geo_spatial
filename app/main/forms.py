from django import forms
from django.contrib.gis.geos import Polygon, Point
from main.models import PolygonModel


class PolygonForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Latitude'}), required=False)
    longitude = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Longitude'}), required=False)
    coordinates = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}), required=False)

    class Meta:
        model = PolygonModel
        fields = ['name', 'polygon']

    def clean(self):
        cleaned_data = super().clean()
        coordinates = cleaned_data.get('coordinates')
        
        if coordinates:
            try:
                points = [
                    Point(float(lon), float(lat))
                    for lat, lon in (coord.split() for coord in coordinates.split(','))
                ]

                if len(points) < 3:
                    raise forms.ValidationError("A polygon must have at least 3 points")

                if points[0] != points[-1]:
                    points.append(points[0])

                cleaned_data['polygon'] = Polygon(points)
            except ValueError as e:
                raise forms.ValidationError(f"Invalid coordinates: {str(e)}")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
