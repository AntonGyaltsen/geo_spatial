from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PolygonForm
from .models import PolygonModel


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
