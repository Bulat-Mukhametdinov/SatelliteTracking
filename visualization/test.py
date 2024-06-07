import math
import cv2
import datetime
import numpy as np
from pyorbital.orbital import Orbital

pi = math.pi

def spherical2mercator(latitude:float, longitude:float, img_size:tuple[int, int]):
    """
    Translates latitude and longitude to mercator projection coordinates on image\n
    img_size = (img_height, img_width)
    """
 
    h, w = img_size

    x = int(w * (pi + longitude) / (2 * pi)) % w
    y = int(h * (pi - math.log(math.tan(pi / 4 + latitude / 2))) / (2 * pi)) % h
    return x, y



s = '1 25544U 98067A   24158.57932675  .00018530  00000+0  32097-3 0  9994'
t = '2 25544  51.6405   7.8504 0005827 281.5011 168.8243 15.50938054456903'

orb = Orbital("ISS (ZARYA)", line1=s, line2=t)

bg = cv2.imread("earthmap.jpg")
sprite = np.ones((60, 60, 3)) * 255

d = datetime.datetime.now(datetime.timezone.utc)
while True:
    t = d
    t -= datetime.timedelta(seconds=3000)
    img = bg.copy()
    y_p, x_p = 0, 0
    for i in range(300):
        t += datetime.timedelta(seconds=20)
        lon, lat, alt = orb.get_lonlatalt(t)
        lat, lon = np.deg2rad(np.array((lat, lon)))
        x1, y1 = spherical2mercator(lat, lon, img.shape[:2])

        if (y_p, x_p) == (0, 0) or x1 - x_p < 0:
            y_p, x_p = y1, x1
            continue
        cv2.line(img, (x_p, y_p), (x1, y1), (200, 200, 200), 2)
        x_p, y_p = x1, y1

    # t = datetime.datetime.now(datetime.timezone.utc)
    d += datetime.timedelta(seconds=20)
    t = d
    lon, lat, alt = orb.get_lonlatalt(t)
    lat, lon = np.deg2rad(np.array((lat, lon)))
    x1, y1 = spherical2mercator(lat, lon, img.shape[:2])

    img2show = img.copy()
    # img2show = cv2.circle(img2show, (x1, y1), 2, (0, 0, 255), -1)
    for i in range(60):
        for j in range(60):
            if tuple(sprite[i, j]) != (255, 255, 255) and 0 <= y1 - i // 2 + 20 < img.shape[0] and 0 <= x1 - j // 2 < img.shape[1]:
                img2show[y1 - i // 2 + 20, x1 - j // 2] = sprite[i, j]
    cv2.putText(img2show, orb.satellite_name, (x1+ 3, y1 + 3), 0, 0.5, (0, 0, 255), 2)
    cv2.putText(img2show, f'Real time tracking {t}', (5, 20), 0, 0.5, (255, 0, 0), 2)

    cv2.imshow(None, img2show)
    if cv2.waitKey(1) == ord('q'):
        break
    cv2.imwrite("img.png", img2show)
