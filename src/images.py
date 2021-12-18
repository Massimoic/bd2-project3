import face_recognition as frec
import numpy as np

def getEncoding(file):
    # Make sure you're in src folder
    # img = frec.load_image_file('./data/faces/Aaron_Eckhart/Aaron_Eckhart_0001.jpg')
    encoding = frec.face_encodings(file)[0]
    # print(encoding)
    return encoding