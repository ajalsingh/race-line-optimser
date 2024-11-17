import geojson
from shapely.geometry import shape


def load_geojson(file_path):
    """
    Load a GeoJSON file and extract its geometry.
    """
    with open(file_path.as_posix(), "r") as file:
        data = geojson.load(file)
    geometries = []
    for feature in data.get("features", []):
        if "geometry" in feature and feature["geometry"]["type"] in [
            "LineString",
            "MultiLineString",
        ]:
            geom = shape(feature["geometry"])
            geometries.append(geom)
    return geometries
