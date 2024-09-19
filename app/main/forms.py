from django import forms
from django.contrib.gis.geos import Point, Polygon

from main.models import PolygonModel


class PolygonForm(forms.ModelForm):
    coordinates = forms.CharField(
        widget=forms.Textarea(attrs={"readonly": "readonly"}), required=False
    )

    class Meta:
        model = PolygonModel
        fields = ["name", "polygon"]

    def clean(self):
        cleaned_data = super().clean()
        coordinates = cleaned_data.get("coordinates")

        if coordinates:
            try:
                points = [
                    Point(float(lon), float(lat))
                    for lat, lon in (coord.split() for coord in coordinates.split(","))
                ]

                if len(points) < 3:
                    raise forms.ValidationError("A polygon must have at least 3 points")

                if points[0] != points[-1]:
                    points.append(points[0])

                crosses_antimeridian = False
                adjusted_points = []
                for point in points:
                    lon, lat = point.x, point.y
                    if lon > 180:
                        lon -= 360
                        crosses_antimeridian = True
                    elif lon < -180:
                        lon += 360
                        crosses_antimeridian = True
                    adjusted_points.append(Point(lon, lat))

                cleaned_data["polygon"] = Polygon(adjusted_points)

                self.instance.crosses_antimeridian = crosses_antimeridian

            except ValueError as e:
                raise forms.ValidationError(f"Invalid coordinates: {str(e)}")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
