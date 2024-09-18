def adjust_coordinates_for_antimeridian(coordinates):
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