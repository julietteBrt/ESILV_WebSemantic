from math import sin, cos, sqrt, atan2, radians


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
