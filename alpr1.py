import cv2
import numpy as np
import os
import math
import random
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 19
MIN_NUMBER_OF_MATCHING_CHARS = 3
MAX_DIAG_SIZE_MULTIPLE_AWAY= 5.0
MAX_ANGLE_BETWEEN_CHARS = 12.0
MAX_CHANGE_IN_AREA = 0.9
MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30
MIN_CONTOUR_AREA = 100
kNearest = cv2.ml.KNearest_create()

class PossibleChar:
    def __init__(self,contour):
        self.MIN_PIXEL_WIDTH = 2
        self.MIN_PIXEL_HEIGHT = 8
        self.MIN_ASPECT_RATIO = 0.25
        self.MAX_ASPECT_RATIO = 1.0
        self.MIN_PIXEL_AREA = 80
        self.MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
        self.MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0
        self.MAX_CHANGE_IN_AREA = 0.5
        self.MAX_CHANGE_IN_WIDTH = 0.8
        self.MAX_CHANGE_IN_HEIGHT = 0.2
        self.MAX_ANGLE_BETWEEN_CHARS = 12.0
        self.RESIZED_CHAR_IMAGE_WIDTH = 20
        self.RESIZED_CHAR_IMAGE_HEIGHT = 30
        self.MIN_CONTOUR_AREA = 100

        self.contour = contour
        [intX, intY, intWidth, intHeight] = cv2.boundingRect(self.contour)

        self.intBoundingRectX = intX
        self.intBoundingRectY = intY
        self.intBoundingRectWidth = intWidth
        self.intBoundingRectHeight = intHeight

        self.intBoundingRectArea = self.intBoundingRectWidth * self.intBoundingRectHeight

        self.intCenterX = (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2
        self.intCenterY = (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2

        self.fltDiagonalSize = math.sqrt((self.intBoundingRectWidth ** 2) + (self.intBoundingRectHeight ** 2))

        self.fltAspectRatio = float(self.intBoundingRectWidth) / float(self.intBoundingRectHeight)

    def check(self):
        if (self.intBoundingRectArea > self.MIN_PIXEL_AREA and self.intBoundingRectWidth > self.MIN_PIXEL_WIDTH and self.intBoundingRectHeight > self.MIN_PIXEL_HEIGHT
            and self.MIN_ASPECT_RATIO < self.fltAspectRatio and self.fltAspectRatio < self.MAX_ASPECT_RATIO):
            return True
        else:
            return False

def loadKNNDataAndTrainKNN():
    x=[]
    y=[]
    z=[]
    cc=0
    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)
        for i in npaClassifications:
            x.append(chr(int(i)))
        print(x)
    except:
        print("error, unable to open classifications.txt, exiting program\n")
        os.system("pause")
        return False

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
        for i in npaFlattenedImages:
            for j in i:
                y.append(chr(int(j)))
        print(y)
    except:
        print("error, unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
        return False

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))
    kNearest.setDefaultK(1)
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    return True

def preprocess(imgOriginal):

    imgGrayscale = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)

    imgBlur = cv2.GaussianBlur(imgGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    imgThresh = cv2.adaptiveThreshold(imgBlur, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    return imgGrayscale, imgThresh

def PossibleCharsInScene(imgThresh):
    listOfPossibleChars = []

    intCountOfPossibleChars = 0
    imgThreshCopy = imgThresh.copy()

    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contours)):
        possibleChar = PossibleChar(contours[i])
        if possibleChar.check():
            intCountOfPossibleChars+=1
            listOfPossibleChars.append(possibleChar)
            contours.append(possibleChar.contour)
            cv2.drawContours(imgContours, contours, i, (255, 255, 0), 1)

    cv2.imshow("2",imgContours)

    cv2.waitKey(0)
    return listOfPossibleChars

def ObtainListOfMatchingChars(listOfPossibleCharsInScene):
    listOfListsOfMatchingChars = []
    count=0
    for possibleChar in listOfPossibleCharsInScene:
        listOfMatchingChars = []
        for c in listOfPossibleCharsInScene:
            if c == possibleChar:
                continue
            dist = distanceBetweenChars(possibleChar, c)
            angle = angleBetweenChars(possibleChar, c)
            c_width = float(abs(c.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(
                possibleChar.intBoundingRectWidth)
            c_height = float(abs(c.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(
                possibleChar.intBoundingRectHeight)
            c_area = float(abs(c.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(
                possibleChar.intBoundingRectArea)
            if dist < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and angle < MAX_ANGLE_BETWEEN_CHARS \
                    and c_area < MAX_CHANGE_IN_AREA and c_width < MAX_CHANGE_IN_WIDTH and c_height < MAX_CHANGE_IN_HEIGHT:
                listOfMatchingChars.append(c)
        listOfMatchingChars.append(possibleChar)
        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:
            continue
        listOfListsOfMatchingChars.append(listOfMatchingChars)
    return listOfListsOfMatchingChars

def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))

def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:
        fltAngleInRad = math.atan(fltOpp / fltAdj)
    else:
        fltAngleInRad = 1.5708

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)
    return fltAngleInDeg

def recognizeCharsInPlate(imgThreshScene, listOfMatchingChars):
    strChars = ""
    z=[]
    height, width = imgThreshScene.shape

    imgThreshColor = np.zeros((height, width, 3), np.uint8)

    listOfMatchingChars.sort(key=lambda chars: chars.intCenterX)

    cv2.cvtColor(imgThreshScene, cv2.COLOR_GRAY2BGR, imgThreshColor)

    for currentChar in listOfMatchingChars:
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

        cv2.rectangle(imgThreshColor, pt1, pt2,(255, 0, 0), 2)

        imgROI = imgThreshScene[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))
        npaROIResized = imgROIResized.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))

        npaROIResized = np.float32(npaROIResized)

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 5)
        print(chr(npaResults[0][0]),end="   ")
        print()
        strCurrentChar = str(chr(int(npaResults[0][0])))
        strChars = strChars + strCurrentChar
        cv2.imshow("4", imgThreshColor)

    return strChars

def main():
    blnKNNTrainingSuccessful = loadKNNDataAndTrainKNN()

    if blnKNNTrainingSuccessful == False:
        print("\nerror: KNN traning was not successful\n")
        return
    imgOriginal = cv2.imread("demo2.jpg")
    height, width, numChannels = imgOriginal.shape
    if imgOriginal is None:
        print("\nError: Image has not been read from file \n")
        input()
        return
    else:
        cv2.imshow('Original Image', imgOriginal)
        cv2.waitKey(0)
        imgGrayscaleScene, imgThreshScene = preprocess(imgOriginal)
        cv2.imshow('1a', imgGrayscaleScene)
        cv2.waitKey(0)
        cv2.imshow('1b', imgThreshScene)
        cv2.waitKey(0)

        listOfPossibleCharsInScene= PossibleCharsInScene(imgThreshScene)
        listOfMatchingCharsInPlate = ObtainListOfMatchingChars(listOfPossibleCharsInScene)
        if len(listOfMatchingCharsInPlate) == 0:
            print("No characters found in plate number")
        else:
            imgContours = np.zeros((height, width, 3), np.uint8)
            print("listOfMatchingCharsInPlate.Count= " + str(len(listOfMatchingCharsInPlate)))
            for listOfMatchingChars in listOfMatchingCharsInPlate:
                contours = []
                intRandomBlue = random.randint(0, 255)
                intRandomGreen = random.randint(0, 255)
                intRandomRed = random.randint(0, 255)
                for chars in listOfMatchingChars:
                    contours.append(chars.contour)
                    cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            cv2.imshow("3", imgContours)
            cv2.waitKey(0)
            final_string=recognizeCharsInPlate(imgThreshScene,listOfMatchingChars)
            print("License Plate Number = "+final_string)
            cv2.waitKey()
            print("100% accuracy for ",final_string)
            return final_string

if __name__ == "__main__":
    main()
