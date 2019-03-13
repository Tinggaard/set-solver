import cv2
import numpy as np
import solve


game = solve.game()

alias = {"purple": 0, "green": 1, "red": 2,
        "striped": 0, "empty": 1, "full": 2,
        "peanut": 0, "pill": 1, "rhombus": 2}


#################################
#################################
####### IMAGE RECOGNITION #######
#################################
#################################

#Path to the image (without the ending)
imagefile = "images\\set4"


#Loading the image into cv2
img = cv2.imread(imagefile + ".jpg", cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 10)


#Converting the image to HSV colorspace (max = 180, 255, 255)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


#Returning black image
def black(image):
    blck = np.zeros(image.shape, np.uint8)
    return cv2.cvtColor(blck, cv2.COLOR_BGR2GRAY)

#Writing the image to the disk, with the given extension.
#Mainly used for debugging
def write(location, image):
    cv2.imwrite(imagefile + location + ".jpg", image)


write("_thresh", threshold)
######################## FINDING CARDS ##########################
#Declaring highest and lowest values for color-recognition
lower_white = np.array([0, 0, 150])
upper_white = np.array([180, 75, 255])

#Creating a mask to find the shapes in the given color spectrum
white_mask = cv2.inRange(img_hsv, lower_white, upper_white)
#Finding the cards by contours
_, card_cnts, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
card_cnts = [contour for contour in card_cnts if cv2.contourArea(contour) > 10000]

#Drawing it as a mask
all_cards = cv2.drawContours(black(img), card_cnts, -1, (255), -1)
erosion = cv2.erode(all_cards, np.ones((5, 5), np.uint8), iterations=20)
_, card_cnts, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

card_ct = card_cnts[5]


rect = cv2.minAreaRect(card_ct)
box = cv2.boxPoints(rect)
box = np.int0(box)

single = cv2.drawContours(img, [box], -1, (255, 0, 255), 5)
write("_single", single)


write("_all", all_cards)

print("Found {} cards".format(len(card_cnts)))

################ FINDING ATTRIBUTES - FUNCTIONS ###################
colors = [[[120, 50, 50], [150, 255, 255], "purple"],
          [[50, 50, 50], [80, 255, 255], "green"]]



# Iterating over the cards

"""
for card_nr, card_cnt in enumerate(card_cnts):
    #Creating mask of the card
    card_mask = cv2.drawContours(black(img), [card_cnt], -1, (255), -1)
    card = cv2.bitwise_and(img, img, mask=card_mask)
    card_hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)


    ######################### NUMBER OF ATTRIBUTES #####################
    #Declaring highest and lowest values for attribute-recognition
    lower_white = np.array([0, 60, 0])
    upper_white = np.array([180, 255, 255])

    #Creating a mask to find the shapes in the given spectrum
    atrs_mask = cv2.inRange(card_hsv, lower_white, upper_white)


    #Finding the cotours - The attributes
    _, atrs, _ = cv2.findContours(atrs_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    atrs = [at for at in atrs if cv2.contourArea(at) > 25000]
    atr_count = len(atrs)

    #Creating list for checking all attributes return same values
    diff = [[] for i in range(len(atrs))]

    #Iterating over the attributes
    for atr_nr, atr in enumerate(atrs):
        #Mask of the single attribute
        single_atr_mask = cv2.drawContours(black(img), [atr], -1, (255), -1)
        single_atr = cv2.bitwise_and(img_hsv, img_hsv, mask=single_atr_mask)


        ##################### COLOR ON ATTRIBUTES #######################
        for color in colors:
            #Upper and lower color
            lower_color = np.array(color[0])
            upper_color = np.array(color[1])
            color_mask = cv2.inRange(single_atr, lower_color, upper_color)

            #Finding the contours (if any)
            _, color_contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            color_contours = [cnt for cnt in color_contours if cv2.contourArea(cnt) > 1000]

            if len(color_contours) != 0:
                diff[atr_nr].append(color[2])
                break

        if len(diff[atr_nr]) == 0:
            diff[atr_nr].append("red")
        
   
        ######################## FILL OF ATTRIBUTE ######################
        #Getting the mean color of b/w image of the attribute from 2 different methods
        mean_color_range = cv2.mean(atrs_mask, mask=single_atr_mask)
        mean_color_range = mean_color_range[0]

        mean_color_thresh = cv2.mean(threshold, mask=single_atr_mask)
        mean_color_thresh = mean_color_thresh[0]



        if 180 > mean_color_thresh > 75:
            diff[atr_nr].append("striped")

        elif mean_color_range < 75:
            diff[atr_nr].append("empty")

        else:
            diff[atr_nr].append("full")


        ####################### FORM OF ATTRIBUTE ######################
        area = cv2.contourArea(atr)

        hull = cv2.convexHull(atr)
        hull_area = cv2.contourArea(hull)
        solidity = area/hull_area

        rect = cv2.minAreaRect(atr)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        area_rect = cv2.contourArea(box)
        extent = area/area_rect

        if solidity < 0.9:
            diff[atr_nr].append("peanut")

        elif extent > 0.75:
            diff[atr_nr].append("pill")

        else:
            diff[atr_nr].append("rhombus")




    ################# CHEKCING FOR DIFFERENCES ##################
    if not all([diff[i]==diff[i+1] for i in range(atr_count-1)]):
        raise Exception("Could not identify attributes on card " + str(card_nr))

    #Adding the card to game class
    atr_color = alias[diff[0][0]]
    atr_fill = alias[diff[0][1]]
    atr_shape = alias[diff[0][2]]
    game.addCard(solve.card(atr_count-1, atr_color, atr_fill, atr_shape))

    #Drawing card-ID on image for refference
    # x, y, w, h = cv2.boundingRect(card_cnt)
    # cv2.putText(img, str(card_nr), (x+100, y+100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 255), 10)



    print("Processed card {} of {}".format(card_nr+1, len(card_cnts)))

#Card ID's on image
# write("_text", img)
print("Successfully processed all cards!")





print("\nFound {} sets".format(len(game.findSets())))



for num, cards in enumerate(game.findSetsId()):
    set_contours = [card_cnts[i] for i in cards]

    mask = black(img)
    for cnt in set_contours:
        mask = cv2.drawContours(mask, [cnt], -1, (255), -1)

    the_set = cv2.bitwise_and(img, img, mask=mask)

    cv2.imwrite(imagefile + "_set" + str(num+1) + ".jpg", the_set)
"""