import math
import numpy as np
import cv2

src = cv2.imread('Imagenes/Maze 6.png')


MAZE_NAME = "Ventana de Visualizacion del Laberinto"

def translation(image):
    window = cv2.namedWindow(MAZE_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(MAZE_NAME, 900,900)
    cv2.imshow(MAZE_NAME,image)
    cv2.moveWindow(MAZE_NAME,100,100)
    print("Por favor presiona \'S\' para seleccionar los puntos")

    i=1
    lista=[]
    while(i<=4):
        key = cv2.waitKey(0)
        if key == ord ('s'):
            print("Por favor selecciona un punto")
            x,y = get_user_selected_point(image)
            lista.append([x,y])
            i = i+1
        else:
            print("Invalido")
            continue
    cv2.destroyAllWindows()
    return lista

def get_user_selected_point(image):
    global point
    point = (-1,-1)
    cv2.setMouseCallback(MAZE_NAME,get_mouse_point)
    print("Presiona alguna tecla despues de haber seleccionado un punto")
    while point == (-1,-1):
        cv2.waitKey(0)
        if(point == (-1,-1)):
            print("Punto invalido, por favor intenta de nuevo")
    return point[0],point[1]

def get_mouse_point(event,x,y,flags,param):
    global point
    if event == cv2.EVENT_LBUTTONUP:
        print("Punto {0},{1} seleccionado".format(x,y))
        point = (x,y)

lista1 = translation(src)

pts1 = np.float32(lista1)
pts2 = np.float32([[0, 0], [600, 0], [600, 600], [0, 600]])

M = cv2.getPerspectiveTransform(pts1, pts2)

dst = cv2.warpPerspective(src, M, (600, 600))

cv2.imwrite('Imagenes/MazeTrans.png',dst)

cv2.imshow('Original', src)
cv2.imshow('Transformada', dst)
cv2.waitKey()