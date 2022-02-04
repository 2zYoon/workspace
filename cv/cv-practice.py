import sys
import os
import cv2
import numpy as np

def tool_gen_empty(name="img.png", size=(200, 200)):
    cv2.imwrite(name, np.zeros((size[0], size[1], 3), np.uint8))


def tool_concat(imgs, mode=0):
    if mode == 0:
        pass
        

if __name__ == "__main__":
    tool_gen_empty("img3.png", size=(500, 500))
    imgs = []
    for i in range(1, 4):
        imgs.append(cv2.imread("img{}.png".format(i)))
    
    new = cv2.vconcat(imgs)
    cv2.imshow("new", new)
    cv2.waitKey(0)