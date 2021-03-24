from math import sin, cos, sqrt, atan2, radians
import geopy


# source: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def get_distance(point1, point2):
    point1 = list(point1)
    point2 = list(point2)
    R = 6373.0
    for i in (0, 1):
        point1[i] = radians(point1[i])
        point2[i] = radians(point2[i])
    dlat = point2[0] - point1[0]
    dlon = point2[1] - point1[1]
    a = sin(dlat / 2)**2 + cos(point1[0]) * cos(point2[0]) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000


def get_bounds(points):
    lats = [p[0] for p in points]
    longs = [p[1] for p in points]
    bound_sw = (min(lats), min(longs))
    bound_ne = (max(lats), max(longs))
    return (bound_sw, bound_ne)


def find_point(address):
    geolocator = geopy.Nominatim(user_agent='ESILV_WebSemantic')
    location = geolocator.geocode(address)
    if location is None:
        return
    return (location.latitude, location.longitude)
