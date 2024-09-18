from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PolygonForm


def polygon_view(request):
    if request.method == 'POST':
        form = PolygonForm(request.POST)
        print(f"Submitted data: {request.POST}")
        if form.is_valid():
            try:
                polygon = form.save(commit=False)
                
                coordinates = polygon.polygon.coords[0]
                crosses_antimeridian = False
                adjusted_coordinates = []

                for lon, lat in coordinates:
                    if lon > 180:
                        lon -= 360
                        crosses_antimeridian = True
                    elif lon < -180:
                        lon += 360
                        crosses_antimeridian = True
                    adjusted_coordinates.append((lon, lat))

                polygon.polygon = type(polygon.polygon)(adjusted_coordinates)
                polygon.crosses_antimeridian = crosses_antimeridian
                polygon.save()

                print(f"Polygon created: {polygon}")
                messages.success(request, 'Polygon saved successfully!')
                return redirect('polygon_form')
            except Exception as e:
                print(f"Error saving polygon: {str(e)}")
                messages.error(request, f'Error saving polygon: {str(e)}')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = PolygonForm()

    return render(request, 'main/polygon_form.html', {'form': form})