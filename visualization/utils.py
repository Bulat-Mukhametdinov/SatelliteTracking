import math
import numpy as np
from pyorbital.orbital import Orbital
from datetime import datetime

pi = math.pi


def spherical2mercator(latitude:float, longitude:float, img_size:tuple[int, int]):
    """
    Translates latitude and longitude to mercator projection coordinates on image\n
    img_size = (img_height, img_width)
    """
 
    h, w = img_size

    latitude = min(latitude, 2 * math.atan(math.exp(pi)) - pi / 2)

    x = int(w * (pi + longitude) / (2 * pi)) % w
    y = min(int(h * (pi - math.log(math.tan(pi / 4 + latitude / 2))) / (2 * pi)), h - 1)
    return x, y


def getLatLon(satellite:Orbital, time:datetime) -> tuple[float, float]:
    """
    Returns latitude and longitude at radians of satellite
    """

    lon, lat, alt = satellite.get_lonlatalt(time)
    return np.deg2rad(np.array((lat, lon)))


def getSatellitesObjects(file_name="TLE_data.txt") -> list[Orbital]:
    """
    Prepares list of Orbital objects from file with tle data
    """

    satellites = list()

    with open(file_name) as f:
        data = f.readlines()

        title = None
        line1 = None
        line2 = None

        for row in data:
            row = row.replace('\n', '')
            if row[0] == '0':
                title = row[2:]
                line1 = None
                line2 = None
            elif row[0] == '1':
                line1 = row
                line2 = None
            elif row[0] == '2':
                line2 = row
                if title is None:
                    title = "UNK"
                s = Orbital(title, line1=line1, line2=line2)

                satellites.append(s)

                title = None
                line1 = None
                line2 = None

    return satellites

