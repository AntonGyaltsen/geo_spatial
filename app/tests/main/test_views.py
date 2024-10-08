import pytest
from django.contrib.gis.geos import Polygon
from django.test import Client
from django.urls import reverse

from main.models import PolygonModel


@pytest.mark.django_db
def test_polygon_view_add_record():
    client = Client()
    url = reverse("polygon_form")

    coordinates = "0.0 175.0, 0.0 185.0, 10.0 185.0, 10.0 175.0, 0.0 175.0"

    form_data = {
        "name": "Test Polygon",
        "coordinates": coordinates,
        "latitude": 10.0,
        "longitude": 20.0,
        "polygon": "POLYGON((0.0 175.0, 0.0 185.0, 10.0 185.0, 10.0 175.0, 0.0 175.0))",
    }

    response = client.post(url, data=form_data)

    assert response.status_code in [
        200,
        302,
    ], f"Unexpected status code: {response.status_code}"

    polygons = PolygonModel.objects.all()
    print(f"Number of PolygonModel objects: {polygons.count()}")
    for polygon in polygons:
        print(
            f"Polygon: {polygon.name}, {polygon.polygon}, Crosses Antimeridian: {polygon.crosses_antimeridian}"
        )

    assert PolygonModel.objects.count() == 1, "PolygonModel object was not created"
    polygon = PolygonModel.objects.first()
    assert polygon.name == "Test Polygon"
    expected_coords = (
        (175.0, 0.0),
        (-175.0, 0.0),
        (-175.0, 10.0),
        (175.0, 10.0),
        (175.0, 0.0),
    )
    assert polygon.polygon.coords[0] == expected_coords
    assert polygon.crosses_antimeridian


@pytest.mark.django_db
def test_polygon_api_add_record(client):
    polygons = PolygonModel.objects.all()
    assert len(polygons) == 0

    coordinates = [
        [174.19921875000003, 69.3493386397765],
        [204.96093750000003, 69.3493386397765],
        [205.48828125000003, 62.103882522897884],
        [173.67187500000003, 62.186013857194226],
        [174.19921875000003, 69.3493386397765],
    ]
    expected_coords = (
        (174.19921875000003, 69.3493386397765),
        (-155.03906249999997, 69.3493386397765),
        (-154.51171874999997, 62.103882522897884),
        (173.67187500000003, 62.186013857194226),
        (174.19921875000003, 69.3493386397765),
    )

    geojson_polygon = {"type": "Polygon", "coordinates": [coordinates]}

    resp = client.post(
        "/api/polygons/",
        {
            "name": "Test Polygon",
            "polygon": geojson_polygon,
        },
        content_type="application/json",
    )

    assert (
        resp.status_code == 201
    ), f"Expected status code 201, but got {resp.status_code}"

    polygons = PolygonModel.objects.all()
    assert len(polygons) == 1, "A polygon should have been created"

    polygon = polygons.first()
    assert (
        polygon.name == "Test Polygon"
    ), f"Expected polygon name 'Test Polygon', but got {polygon.name}"

    stored_coords = polygon.polygon.coords[0]
    assert (
        stored_coords == expected_coords
    ), f"Expected coordinates {expected_coords}, but got {stored_coords}"

    assert (
        polygon.crosses_antimeridian is True
    ), "The polygon should cross the antimeridian"


@pytest.mark.django_db
def test_get_polygon_by_id(client):
    coordinates = (
        (174.19921875000003, 69.3493386397765),
        (204.96093750000003, 69.3493386397765),
        (205.48828125000003, 62.103882522897884),
        (173.67187500000003, 62.186013857194226),
        (174.19921875000003, 69.3493386397765),
    )

    polygon = PolygonModel.objects.create(
        name="Test Polygon", polygon=Polygon(coordinates), crosses_antimeridian=True
    )

    url = reverse("polygon-detail", args=[polygon.id])
    response = client.get(url)

    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()
    print(f"Response data: {response_data}")

    assert (
        response_data["properties"]["name"] == "Test Polygon"
    ), f"Expected name 'Test Polygon', but got {response_data['properties']['name']}"

    geometry = response_data["geometry"]
    assert (
        "POLYGON" in geometry
    ), f"Expected geometry to be a POLYGON, but got {geometry}"

    stored_coords = polygon.polygon.coords[0]
    assert stored_coords == coordinates, (
        f"Expected coordinates" f" {coordinates}, but got" f" {stored_coords}"
    )

    assert (
        response_data["properties"]["crosses_antimeridian"] is True
    ), f"Expected crosses_antimeridian to be True, but got {response_data['properties']['crosses_antimeridian']}"


@pytest.mark.django_db
def test_delete_polygon(client):
    coordinates = (
        (174.19921875000003, 69.3493386397765),
        (204.96093750000003, 69.3493386397765),
        (205.48828125000003, 62.103882522897884),
        (173.67187500000003, 62.186013857194226),
        (174.19921875000003, 69.3493386397765),
    )

    polygon = PolygonModel.objects.create(
        name="Test Polygon", polygon=Polygon(coordinates), crosses_antimeridian=True
    )

    url = reverse("polygon-detail", args=[polygon.id])
    response = client.delete(url)

    assert (
        response.status_code == 204
    ), f"Expected status code 204, but got {response.status_code}"

    polygons = PolygonModel.objects.all()
    assert (
        len(polygons) == 0
    ), "The polygon should have been deleted, but it's still in the database"


@pytest.mark.django_db
def test_update_polygon(client):
    original_coordinates = (
        (174.19921875000003, 69.3493386397765),
        (204.96093750000003, 69.3493386397765),
        (205.48828125000003, 62.103882522897884),
        (173.67187500000003, 62.186013857194226),
        (174.19921875000003, 69.3493386397765),
    )

    updated_coordinates = (
        (150.19921875000003, 60.3493386397765),
        (160.96093750000003, 60.3493386397765),
        (160.48828125000003, 55.103882522897884),
        (150.67187500000003, 55.186013857194226),
        (150.19921875000003, 60.3493386397765),
    )

    polygon = PolygonModel.objects.create(
        name="Test Polygon",
        polygon=Polygon(original_coordinates),
        crosses_antimeridian=False,
    )

    updated_data = {
        "name": "Updated Polygon",
        "polygon": {"type": "Polygon", "coordinates": [updated_coordinates]},
        "crosses_antimeridian": False,
    }

    url = reverse("polygon-detail", args=[polygon.id])
    response = client.put(url, updated_data, content_type="application/json")

    assert (
        response.status_code == 200
    ), f"Expected status code 200, but got {response.status_code}"

    polygon.refresh_from_db()

    assert (
        polygon.name == "Updated Polygon"
    ), f"Expected name 'Updated Polygon', but got {polygon.name}"
    assert (
        polygon.polygon.coords[0] == updated_coordinates
    ), f"Expected coordinates {updated_coordinates}, but got {tuple(polygon.polygon.coords[0])}"
    assert (
        polygon.crosses_antimeridian is False
    ), f"Expected crosses_antimeridian to be False, but got {polygon.crosses_antimeridian}"
