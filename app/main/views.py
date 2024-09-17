from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PolygonForm


def polygon_view(request):
    if request.method == 'POST':
        form = PolygonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Polygon saved successfully!')
            return redirect('polygon_form')
    else:
        form = PolygonForm()

    return render(request, 'main/polygon_form.html', {'form': form})