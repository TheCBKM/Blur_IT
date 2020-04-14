import cv2
import sys

def face_blur (imagePath,dest): 
    cascPath = 'haarcascade_frontalface_default.xml'

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image and convert to gray
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(cv2.imread(imagePath), cv2.COLOR_BGR2GRAY)
    print(gray)
    print("imagePath")

    # now we can try to detect faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print(faces)

    # Draw a rectangle around the faces and display on screen
    result=[]
    for (x, y, w, h) in faces:
        result.append((x,y,w,h))
        face_image=image[y:y+h, x:x+w]
        face_image = cv2.GaussianBlur(face_image, (21, 21), 10)
        image[y:y+h, x:x+w]=face_image

    cv2.imwrite(dest,image)
    return result

