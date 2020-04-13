from PIL import Image 
import sys

def saveCompressed(src):
    try:
        foo = Image.open(src)
        foo.save(src,quality=20,optimize=True)  
        print("Compressed")
        return True
    except:
        print("exception")
        return False