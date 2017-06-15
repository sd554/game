import math


def polarToCartesian(angle, length):
    angle = math.radians(angle)
    dx = length * math.cos(angle)
    dy = length * -math.sin(angle)
    return dx, dy


def cartesianToPolarAngle(x, y):
    return math.degrees(math.atan2(-y, x))


def pointInPolygon(x, y, polygon):
    # original author: W. Randolph Franklin
    # source: http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
    inside = False
    length = len(polygon)
    i = 0
    j = length - 1
    while i < length:
        (vix, viy) = polygon[i]
        (vjx, vjy) = polygon[j]
        if (((viy > y) != (vjy > y)) and
                (x < (vjx - vix) * (y - viy) / float(vjy - viy) + vix)):
            inside = not inside
        j = i
        i += 1
    return inside
