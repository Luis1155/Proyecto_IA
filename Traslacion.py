import math
import numpy as np
import cv2

src = cv2.imread('Imagenes/Maze 2.png')


MAZE_NAME = "Maze Display Window"

def translation(image):
    window = cv2.namedWindow(MAZE_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(MAZE_NAME, 900,900)
    cv2.imshow(MAZE_NAME,image)
    cv2.moveWindow(MAZE_NAME,100,100)
    print("Please \'S\' to select points")

    i=1
    lista=[]
    while(i<=4):
        key = cv2.waitKey(0)
        if key == ord ('s'):
            print("Please select a start point")
            x,y = get_user_selected_point(image)
            lista.append([x,y])
            i = i+1
        else:
            print("Invalid")
            continue
    cv2.destroyAllWindows()
    return lista

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

lista1 = translation(src)

pts1 = np.float32(lista1)
pts2 = np.float32([[0, 0], [600, 0], [600, 600], [0, 600]])

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(src, M, (600, 600))

cv2.imwrite('lab1Gr.png',dst)

cv2.imshow('lab.jpg', src)
cv2.imshow('Transform', dst)
cv2.waitKey()