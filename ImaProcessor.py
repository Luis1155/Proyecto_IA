import cv2
import random as r
import numpy as np

class ImageProcessor:
    def __init__(self,image):
        self.imageToProcess = image

    def getThresholdedImage(self,isInverted):
        threshType = cv2.THRESH_BINARY_INV if isInverted else cv2.THRESH_BINARY
        retval, threshold = cv2.threshold(self.imageToProcess,127,255,threshType)
        return threshold

    def getAdaptiveThreshold(self, image):
        return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,\
                                    cv2.THRESH_BINARY,21,0)

    def getTopBound(self,image):
        height, width = image.shape[:2]
        for i in range(height):
            for j in range(width):
                if(image[i,j] == 0):
                    return i

    def getBottomBound(self,image):
        height, width = image.shape[:2]
        for i in reversed(range(height)):
            for j in range(width):
                if(image[i,j] == 0):
                    return i

    def getLeftBound(self,image):
        height,width = image.shape[:2]
        for i in range(width):
            for j in range(height):
                if(image[j,i] == 0):
                    return i

    def getRightBound(self,image):
        height,width = image.shape[:2]
        for i in reversed(range(width)):
            for j in range(height):
                if(image[j,i] == 0):
                    return i

    def getBounds(self,image):
        height, width = image.shape[:2]
        topBound = self.getTopBound(image)
        bottomBound = self.getBottomBound(image)
        leftBound = self.getLeftBound(image)
        rightBound = self.getRightBound(image)
        return topBound,leftBound,bottomBound,rightBound

    def mark_point(self, point, rad, colour, image):
        cv2.circle(image,point,rad,colour,-1)
        return image

    def encloseMaze(self, image):
        top,left,bottom,right = self.getBounds(image)
        cv2.rectangle(image,(left,top),(right,bottom),0,1)
        return image

    def get_granularity(self,image, num_points):
        total = 0
        height,width = image.shape[:2]

        for i in range(num_points):
            point = (r.randint(0,height-1),r.randint(0,width-1))
            while(image[point[0],point[1]] == 0):
                point = (r.randint(0,height),r.randint(0,width))
            total += self._find_closest_wall(image,point,height,width)
        return int(1.2*total/num_points)

    def _find_closest_wall(self,image, point,height,width):
        reachedWall = False
        distance = 0
        while not reachedWall:
            distance +=1
            if (point[0]+distance == height or point[0]-distance == -1 or point[1]+distance == width or point[1] - distance == -1):
                break;
            for i in range(distance):
                if(image[point[0] + i,point[1] + distance - i] == 0
                    or image[point[0] - i,point[1] + distance - i] == 0
                    or image[point[0] + i,point[1] - distance - i] == 0
                    or image[point[0] - i,point[1] - distance - i] == 0):
                    reachedWall = True
                    break;
        return distance