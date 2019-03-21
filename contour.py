import cv2
import numpy as np


#Path to the image (without the extension)
imagefile = "img\\2\\set2"

#For card recognition
lower_white = np.array([0, 0, 150])
upper_white = np.array([180, 75, 255])

#Returning black image
def black(image):
    blck = np.zeros(image.shape, np.uint8)
    return cv2.cvtColor(blck, cv2.COLOR_BGR2GRAY)

#Writing the image to the disk, with the given extension.
#Mainly used for debugging
def write(location, image):
    cv2.imwrite(imagefile + location + ".jpg", image)


#Loading the image into cv2
img = cv2.imread(imagefile + ".jpg", cv2.IMREAD_COLOR)
blur = cv2.medianBlur(img, 5)
blur_gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
threshold = cv2.adaptiveThreshold(blur_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 20)
write("_thresh", threshold)



_, thresh_cnt, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

trs_cnt = [contour for contour in thresh_cnt if  1000000 > cv2.contourArea(contour) > 100000]
print(len(trs_cnt))
firkanter = cv2.drawContours(img, trs_cnt, -1, (255, 0, 255), 5)
write("_firkant", firkanter)

maske = cv2.drawContours(black(img), trs_cnt, -1, (255), -1)
write("_sort", maske)


for i in trs_cnt:
    print(cv2.contourArea(i))

