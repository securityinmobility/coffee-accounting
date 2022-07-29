import numpy as np
import cv2
from dt_apriltags import Detector

APRILTAG_AREA_WIDTH = 2710
APRILTAG_AREA_HEIGHT = 1360
TABLE_WIDTH = 2000
TABLE_HEIGHT = 1240

img = cv2.imread("test-data-real.JPG")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

def array2tuple(p):
    return (int(p[0]), int(p[1]))

def draw_poly(img, points):
    points = list(map(array2tuple, points))
    for i, p in enumerate(points):
        cv2.line(img, points[i], points[(i + 1) % len(points)], (0, 0, 255), 10)

tags = at_detector.detect(img)
tag_corners = [tag.corners for tag in sorted(tags, key=lambda x: x.tag_id)]

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for c in tag_corners:
    draw_poly(img, c)

# we use tag ids 3, 42, 93 and 154 (picked at random) 
# order of them in the pdf is upperleft, upperright, lowerleft, lowerright
# tag_corners is counterclockwise
points = np.float32([
    tag_corners[0][0],
    tag_corners[1][1],
    tag_corners[3][2],
    tag_corners[2][3],
])

#draw_poly(img, points)
new_size = np.float32([
    [0, 0],
    [APRILTAG_AREA_WIDTH, 0],
    [APRILTAG_AREA_WIDTH, APRILTAG_AREA_HEIGHT],
    [0, APRILTAG_AREA_HEIGHT],
])
print(new_size)
M = cv2.getPerspectiveTransform(points, new_size)
img = cv2.warpPerspective(img, M, (APRILTAG_AREA_WIDTH, APRILTAG_AREA_HEIGHT))

img = img[40 : 40 + TABLE_HEIGHT, 680 : 680 + TABLE_WIDTH]

dx = TABLE_WIDTH // 25
dy = TABLE_HEIGHT // 13
for y in range(0, TABLE_HEIGHT, dy):
    for x in range(0, TABLE_WIDTH, dx):
        x1 = x + dx // 3
        x2 = x + dx - dx // 3
        y1 = y + dy // 3
        y2 = y + dy - dy // 3

        if x1 > img.shape[1] or y1 > img.shape[0]:
            continue

        avg = np.average(img[y1 : y2, x1 : x2])
        print(x // dx, y // dy, avg)

        color = (0, 255, 0) if avg > 230 else (0, 0, 255)
        #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.circle(img, (x + dx - 30, y + dy - 30), 12, color, -1)

cv2.imwrite('output.jpg', img)
