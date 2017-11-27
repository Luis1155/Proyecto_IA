import numpy as np
import cv2
import sys
from ImaProcessor import ImageProcessor
import MazSolver

MAZE_NAME = "Maze Display Window"
point = (-1,-1)

def setupWindow():
    filename = "Imagenes/Maze 7.png"
    
    imageProcessor = ImageProcessor(cv2.imread(filename,0))
    
    colourImage = cv2.imread(filename,1)
    
    image = imageProcessor.getThresholdedImage(False)
    
    granularity = imageProcessor.get_granularity(image, 100)
    
    print("Granularity: {0}".format(granularity))
    
    start_x,start_y,end_x,end_y = get_start_points(image)
    
    image = imageProcessor.encloseMaze(image)
    
    mazerunner = MazSolver.MazeSolver(image,granularity)
    
    solution = mazerunner.solveMaze(start_x,start_y,end_x,end_y)

    if(not solution):
        cv2.imshow(MAZE_NAME,image)
    else:
        solvedImage = draw_solution(solution, colourImage)
        solvedImage = imageProcessor.mark_point((end_x,end_y),3,(255,0,0),solvedImage)
        solvedImage = imageProcessor.mark_point((start_x,start_y),3,(255,0,0),solvedImage)
        window = cv2.namedWindow("Solved Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Solved Image", 900,900)
        cv2.moveWindow("Solved Image",100,100)
        cv2.imshow("Solved Image",solvedImage)
    print "Press any key to exit"
    cv2.waitKey(0)
    cv2.destroyAllWindows

def draw_solution(path,image):
    for i in range(len(path) -1):
        current_point = path[i]
        next_point = path[i+1]
        cv2.line(image,current_point,next_point,(0,0,200),2)
    return image

def get_start_points(image):
    window = cv2.namedWindow(MAZE_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(MAZE_NAME, 900,900)
    cv2.imshow(MAZE_NAME,image)
    cv2.moveWindow(MAZE_NAME,100,100)
    print("Please \'S\' to select start and end points")

    while(True):
        key = cv2.waitKey(0)
        if key == ord ('s'):
            print("Please select a start point")
            start_x,start_y = get_user_selected_point(image)
            print ("Start Point: {0}, please select an end point".format((start_x,start_y)))
            end_x,end_y = get_user_selected_point(image)
            print("End Pont: {0}".format((end_x,end_y)))
            break
        else:
            print("Invalid")
            continue
    cv2.destroyAllWindows()
    return start_x,start_y,end_x,end_y

def get_user_selected_point(image):
    global point
    point = (-1,-1)
    cv2.setMouseCallback(MAZE_NAME,get_mouse_point)
    print("Press any key once you have selected your point")
    while point == (-1,-1):
        cv2.waitKey(0)
        if(point == (-1,-1)):
            print("Invalid pont, please try again")
    return point[0],point[1]

def get_mouse_point(event,x,y,flags,param):
    global point
    if event == cv2.EVENT_LBUTTONUP:
        print("Point {0},{1} selected".format(x,y))
        point = (x,y)

setupWindow()