import cv2
import numpy as np
import constants as c
import solve as s
from sys import argv
from os import path as p
from os import mkdir


######################### BASIC FUNCTIONS ######################

def black(im):
    """Returns a black image, binary, in the same size as input image"""
    return np.zeros(im.shape[0:2], np.uint8)
 
#Writing the image to the disk, with the given extension.
#Mainly used for debugging, but also for writing image solutions
def write(location, extension , im):
    """Writes image to a location, with the given extension'"""
    root, ext = p.splitext(location)
    root = root + extension
    location = p.join(root + ext)

    cv2.imwrite(location, im)


def thresh(gray_im, val):
    """Thresholds gray image with the given value, returns the contours and threshold image"""
    _, thr = cv2.threshold(gray_im, val, 255, cv2.THRESH_BINARY)
    _, card_cnts, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return card_cnts



def crop(cnt, *images):
    """Crop images into smaller bits, making it easier on the CPU usage"""
    assert images is not None
    
    #Checking that all are in fact images
    if not all(isinstance(item, np.ndarray) for item in images):
        raise TypeError('"*images" must be nust be of type: "numpy.ndarray"')

    #Returning the cropped images

    reference_y, reference_x = images[0].shape[:2]

    x,y,w,h = cv2.boundingRect(cnt)

    #Ading offset of 2 pixels, so the contours still work properly
    #Making if else statements, to prevent errors in indexing
    y1 = y-2 if 2 < y else 0
    x1 = x-2 if 2 < x else 0
    y2 = y+h+2 if y+h+2 < reference_y else None
    x2 = x+w+2 if x+w+2 < reference_x else None

    return [img[y1:y2, x1:x2] for img in images]




################ FINDING THE CARDS AND RUNNING THE MAIN FUNCTIONS ###########



def find_cards(path):
    """Loops over the different threshold values, and then calls 'check_cards()', on the image in the given path
       Also checks for remaining contours, otherwise it breaks and returns the found contours"""

    if not p.isfile(path):
        raise OSError('Could not locate file: "{}", please make sure you spelled the path correctly'. format(f))


    #Loads the image
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    copy = img.copy()

    found = []
    #Iterating the different values for thresholds
    for val in range(80, 260, 20):

        cnt = thresh(gray, val)
        contours = [c for c in cnt if 800000 > cv2.contourArea(c) > 300000]
        too_big = len([c for c in cnt if cv2.contourArea(c) > 800000])

        #Checking to see if there are any contours left
        if len(contours) == 0 and too_big == 0 and len(found) != 0:
            break

        #Check if the found contours, actually are cards
        outlines = cv2.drawContours(black(img), contours, -1, (255), -1)
        cards = check_cards(contours, outlines, gray)
        found.extend(cards)

    #Printing card ID - for convenience
    for n, f in enumerate(found):
        rect = cv2.minAreaRect(f)
        mid_x = int(rect[0][0])
        mid_y = int(rect[0][1])
        cv2.putText(copy, str(n), (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 4, 0, 10)
    write(path, '_numbers', copy)


    #For your convinience :)
    print('Found {} cards on image: "{}"'.format(len(found), path))

    # atribs = find_atrs([found[6]], img)
    atribs = find_atrs(found, img)

    return found




def check_cards(contours, threshold_im, gray_im):
    """Checks if the givens contours are cards, then returns those who are"""

    real = []
    for nr, c in enumerate(contours):
        #Drawing boxes
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        #Variables for ratio
        x1, y1 = box[0,0], box[0,1]
        x2, y2 = box[1,0], box[1,1]
        x3, y3 = box[2,0], box[2,1]

        #Calculates the length of the hypothenus of a triangle
        s1 = np.hypot(x2-x1, y2-y1)
        s2 = np.hypot(x3-x2, y3-y2)

        #Parametres used to detemine card validation
        ratio = s1/s2 if s1 > s2 else s2/s1  # ~1.4..1.7
        extent = cv2.contourArea(c) / cv2.contourArea(box)  # ~0.93..1

        #If it looks like a card, append the conoutr to rerurn list
        if 1.4 < ratio < 1.75 and 0.93 < extent:
            gray = cv2.drawContours(gray_im, [c], 0, 0, -1)
            real.append(c)

    return real




###################### ATTRIBUTE RECOGNITION ######################




def find_atrs(card_contours, im):
    """Calls the functions to find specific characteristics of the attributes on every card.
       Returns a list containing the cards"""

    attributes = []

    for card_cnt in card_contours:
        copy = im.copy()
        card_mask = cv2.drawContours(black(im), [card_cnt], -1, (255), -1)

        #Make smaller image of the card
        copy, card_mask = crop(card_cnt, copy, card_mask)

        #Varieties of card 
        card = cv2.bitwise_and(copy, copy, mask=card_mask)
        card_gray = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
        card_hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)

        #First, finding the number of attributes
        atr_cnt, count = all_atrs(card_gray)

        #Making image of that specific attribute
        atr, atr_gray, atr_hsv = crop(atr_cnt, card, card_gray, card_hsv)

        #Finding last 3 paramters
        color = atr_color(atr_hsv)
        fill = atr_fill(atr_gray)
        shape = atr_shape(atr_cnt)

        #Appending to the list of current card
        game.addCard(s.card(count, color, fill, shape))
        # print(count, c.ATR_COLOR(color), c.ATR_FILL(fill), c.ATR_SHAPE(shape))


    return attributes


def all_atrs(card_im_gray):
    """Finds all contours on grayscaled card
       returns the first attribute contour and the total number of attributes"""

    #Adaptive threshold and some dialiation, the make the attributes stand out
    adaptive = cv2.adaptiveThreshold(card_im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 10)
    kernel = np.ones((3,3),np.uint8)
    adaptive = cv2.dilate(adaptive, kernel, iterations=1)

    #Finding contours of certain size and with children and whose solidity is greater than .3
    _, atr_contours, atr_hieracy = cv2.findContours(adaptive, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    atrs = [c for c, h in zip(atr_contours, atr_hieracy[0]) if 100000 > cv2.contourArea(c) > 10000 and h[2] != -1]
  
    #Returning the first attribute contour and the total amount of attributes
    return atrs[0], len(atrs)



def atr_color(atr_im_hsv):
    """Finds the color of the attribute based on hue"""

    #Save the hue values, with a saturation over 100
    hue = [col[0] for row in atr_im_hsv for col in row if col[1] > 100]

    #Create histogram of the hues
    hist, _ = np.histogram(hue, 18, (0,179))

    #If some green on image (hue == 120..180)
    if sum(hist[6:10]) > 1000:
        return c.ATR_COLOR_GREEN

    #If more magenta ish (hue == 260..360)
    elif sum(hist[12:17]) > 1000:
        return c.ATR_COLOR_PURPLE

    #Probably just red then
    else: 
        return c.ATR_COLOR_RED



def atr_fill(atr_im_gray):
    """Finds the fill of the attribute, based on color of grayscaled image """

    #Adaptive threshold, used to find stripes
    #Can't tell difference between empty and filled
    adaptive = cv2.adaptiveThreshold(atr_im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 10)

    #Hisogram of the colors (gray), ranging from 0..255
    hist, _ = np.histogram(atr_im_gray, 8, (0,255))


    #If fairly white (high number), then striped
    if np.average(adaptive) >= 45:
        return c.ATR_FILL_STRIPED

    #If a lot of dark pixels on gray image, then filled
    elif sum(hist[:4]) > 20000:
        return c.ATR_FILL_FULL

    #Else probably empty
    else:
        return c.ATR_FILL_EMPTY


 
def atr_shape(atr):
    """Finds the shape of the attribute, based on contour features"""

    #Basic area of the contour
    area = cv2.contourArea(atr)

    #Finding solodity based on convex hull
    hull = cv2.convexHull(atr)
    hull_area = cv2.contourArea(hull)
    solidity = area/hull_area

    #Finding extent of contour
    rect = cv2.minAreaRect(atr)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    area_rect = cv2.contourArea(box)
    extent = area/area_rect

    #If not so solid, then it's a peanut
    if solidity < 0.9:
        return c.ATR_SHAPE_PEANUT

    #If fairly extent, then it's a pill
    elif extent > 0.75:
        return c.ATR_SHAPE_PILL

    #Else probably a rhombus
    else:
        return c.ATR_SHAPE_RHOMBUS
        

############################# IMAGE SOLUTION ##############################


def image_solution(path, cards, ids):
    """Creates an image, for every solution found on current set"""
    img = cv2.imread(path)

    sol_path = p.splitext(path)[0] + "_solution"
    if not p.exists(sol_path):
        mkdir(sol_path)
    
    for nr, solutions in enumerate(ids):
        cp = img.copy()
        mask = black(img)

        for sol in solutions:
            mask = cv2.drawContours(mask, [cards[sol]], -1, (255), -1)
        
        the_set = cv2.bitwise_and(cp, cp, mask=mask)
        write(sol_path + '\\set.jpg', str(nr+1), the_set)




######################## INITIALIZING THE PROGRAM #########################



if __name__ == '__main__':
    filenames = argv[1:]

    #Iterating the files
    for f in filenames:
        try:
            game = s.game()
            cards = find_cards(f)
            ids = game.findSetsId()
            i = image_solution(f, cards, ids)
            print('―――――――――――――――――――――――――――――')
        except:
            continue


#$ python cards.py img\1.jpg img\2.jpg img\3.jpg img\4.jpg img\5.jpg img\6.jpg img\7.jpg

