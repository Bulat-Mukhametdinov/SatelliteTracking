import cv2
import datetime
from typing import Union
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pyorbital.orbital import Orbital
from visualization.utils import *
import time


def get_satellite_orb_img(satellites: Union[list[Orbital], Orbital]):
    """
    Renders satellites with traces to mercator projection of Earth
    """
    img = cv2.imread("visualization/earthmap.jpg")

    if type(satellites) == Orbital:
        satellites = [satellites]

    for satellite in satellites:
        trace_color, sat_color = getRandomColorPair()

        time = datetime.now(timezone.utc) - timedelta(seconds=3000)
        y_p, x_p = 0, 0
        for i in range(600):
            time += timedelta(seconds=10)
            lat, lon = getLatLon(satellite, time)
            x, y = spherical2mercator(lat, lon, img.shape[:2])
            img[y, x] = trace_color


        time = datetime.now(timezone.utc)
        lat, lon = getLatLon(satellite, time)
        x, y = spherical2mercator(lat, lon, img.shape[:2])

        cv2.circle(img=img, center=(x, y), radius=2, color=sat_color, thickness=-1)
        cv2.putText(img=img,
                    text=satellite.satellite_name,
                    org=(x+3, y+3),
                    fontFace=0, 
                    fontScale=0.5,
                    color=sat_color, 
                    thickness=2
                    )

    return img

# img = cv2.imread("earthmap.jpg")
# satellites = getSatellitesObjects()

# while True:
#     time = datetime.now(timezone.utc)
#     start = datetime.now()
#     img2show = img.copy()
#     for s in satellites:
#         lat, lon = getLatLon(s, time)
#         x, y = spherical2mercator(lat, lon, img.shape[:2])

#         img2show[y, x] = (0, 0, 255)

#     end = datetime.now()
#     cv2.putText(img2show, f"{round(1 / (end - start).total_seconds(), 2)} fps", (5, 30), 0, 0.8, (255, 0, 0), 2)
#     cv2.imshow(None, img2show)
#     if cv2.waitKey(1) == ord('q'):
#         break

#     cv2.imwrite("img.png", img2show)