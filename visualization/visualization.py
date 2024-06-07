import cv2
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pyorbital.orbital import Orbital
from visualization.utils import *
import time


def get_satellite_orb_img(satellite: Orbital):
    # s = '1 25544U 98067A   24158.57932675  .00018530  00000+0  32097-3 0  9994'
    # t = '2 25544  51.6405   7.8504 0005827 281.5011 168.8243 15.50938054456903'

    # satellite = Orbital("ISS (ZARYA)", line1=s, line2=t)


    
    img = cv2.imread("visualization/earthmap.jpg")

    time = datetime.now(timezone.utc) - timedelta(seconds=3000)
    y_p, x_p = 0, 0
    for i in range(600):
        time += timedelta(seconds=10)
        lat, lon = getLatLon(satellite, time)
        x, y = spherical2mercator(lat, lon, img.shape[:2])
        img[y, x] = (0, 255, 0)
        # if (y_p, x_p) == (0, 0) or x - x_p < 0:
        #     y_p, x_p = y, x
        #     continue
        # cv2.line(img=img, pt1=(x_p, y_p), pt2=(x, y), color=(200, 200, 200), thickness=2)
        # x_p, y_p = x, y

    time = datetime.now(timezone.utc)
    lat, lon = getLatLon(satellite, time)
    x, y = spherical2mercator(lat, lon, img.shape[:2])

    cv2.circle(img=img, center=(x, y), radius=2, color=(0, 0, 255), thickness=-1)
    cv2.putText(img=img, text=satellite.satellite_name, org=(x+3, y+3), fontFace=0, fontScale=0.5, color=(0, 0, 255), thickness=2)

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