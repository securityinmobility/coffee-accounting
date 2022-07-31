import numpy as np
import cv2
from dt_apriltags import Detector

APRILTAG_AREA_WIDTH = 2710
APRILTAG_AREA_HEIGHT = 1360
TABLE_OFFSET_X = 40
TABLE_OFFSET_Y = 680
TABLE_WIDTH = 2000
TABLE_HEIGHT = 1240
TABLE_ROWS = 13
TABLE_COLS = 25
BLACKWHITE_THRESH = 127
BOX_FILL_THRESH = 240

def find_border(box, dx):
    h, w = box.shape
    startX = 0 if dx > 0 else w - 1

    borderSum = 0
    borderCount = 0
    for y in range(h):
        x = startX
        while x < w and x >= 0 and box[y][x] == 0:
            x += dx

        if x > 0 and x < w:
            borderSum += x
            borderCount += 1

    if borderCount == 0:
        # fallback
        return startX + dx * (w // 4)
    else:
        return borderSum // borderCount


def analyze_image(img):
    thresed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresed_img = cv2.threshold(thresed_img, BLACKWHITE_THRESH, 255, cv2.THRESH_BINARY)

    at_detector = Detector(families='tag36h11',
                        nthreads=1,
                        quad_decimate=1.0,
                        quad_sigma=0.0,
                        refine_edges=1,
                        decode_sharpening=0.25,
                        debug=0)

    tags = at_detector.detect(thresed_img)
    tag_corners = [tag.corners for tag in sorted(tags, key=lambda x: x.tag_id)]

    # we use tag ids 3, 42, 93 and 154 (picked at random) 
    # order of them in the pdf is upperleft, upperright, lowerleft, lowerright
    # tag_corners is counterclockwise
    points = np.float32([
        tag_corners[0][0],
        tag_corners[1][1],
        tag_corners[3][2],
        tag_corners[2][3],
    ])

    new_size = np.float32([
        [0, 0],
        [APRILTAG_AREA_WIDTH, 0],
        [APRILTAG_AREA_WIDTH, APRILTAG_AREA_HEIGHT],
        [0, APRILTAG_AREA_HEIGHT],
    ])
    M = cv2.getPerspectiveTransform(points, new_size)
    img = cv2.warpPerspective(img, M, (APRILTAG_AREA_WIDTH, APRILTAG_AREA_HEIGHT))

    img = img[
        TABLE_OFFSET_X : TABLE_OFFSET_X + TABLE_HEIGHT,
        TABLE_OFFSET_Y : TABLE_OFFSET_Y + TABLE_WIDTH
    ]

    thresed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresed_img = cv2.threshold(thresed_img, BLACKWHITE_THRESH, 255, cv2.THRESH_BINARY)

    dx = TABLE_WIDTH // TABLE_COLS
    dy = TABLE_HEIGHT // TABLE_ROWS
    result = []
    for y in range(0, TABLE_HEIGHT, dy):
        curr = []
        x = 0
        while x < TABLE_WIDTH:
            box = thresed_img[y : y + dy, x : x + dx]
            x1 = x + find_border(box, 1) + 3
            x2 = x + find_border(box, -1) - 3
            y1 = y + find_border(np.transpose(box), 1) + 3
            y2 = y + find_border(np.transpose(box), -1) - 3
            cv2.rectangle(img, (x, y), (x + dx, y + dy), (255, 0, 0), 3)
            if x2 - x1 < 10 or y2 - y1 < 10:
                x += dx
                continue

            avg = np.average(thresed_img[y1 : y2, x1 : x2])
            color = (0, 255, 0) if avg > BOX_FILL_THRESH else (0, 0, 255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

            curr.append(avg <= BOX_FILL_THRESH)
            x = x2 + (TABLE_WIDTH // TABLE_COLS // 6)

        result.append(curr)

    return img, result

if __name__ == "__main__":
    img = cv2.imread("example-input.jpg")
    img, ret = analyze_image(img)
    cv2.imwrite("example-output.jpg", img)
    print(ret)
