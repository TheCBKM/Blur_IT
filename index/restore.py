import cv2
import numpy as np

def restore(source,maskdir,dest):

    # Load our damaged photo
    image = cv2.imread(source)
    image=cv2.resize(image,(600,600))

    # Load the photo where we've marked the damaged areas
    marked_damages = cv2.imread(maskdir, 0)
    marked_damages=cv2.resize(marked_damages,(600,600))  

    ret, thresh1 = cv2.threshold(marked_damages, 254, 255, cv2.THRESH_BINARY)

    # Let's make a mask out of our marked image be changing all colors 
    # that are not white, to black
    kernel = np.ones((7,7), np.uint8)
    mask = cv2.dilate(thresh1, kernel, iterations = 1)  

    restored = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
    cv2.imwrite(dest, restored)

