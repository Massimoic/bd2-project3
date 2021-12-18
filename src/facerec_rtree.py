import face_recognition as fr
import heapq
import numpy as np
from rtree import index
import os, datetime

path = "data/faces"

def image_indexing(rtree_name, n_images):
  import os
  from rtree import index

  # Image collection folder path
  dirList = os.listdir(path)

  # Rtree index properties
  prop = index.Property()
  prop.dimension = 128 #D
  prop.buffering_capacity = 10 #M
  rtreeIndex = index.Index(rtree_name, properties = prop) #r-tree filename

  # Variables de apoyo
  index = 0
  breakUtility = False
  imagesList = []

  # Iterate over all person folders in collection
  for filePath in dirList:
    folderPath = path + "/" + filePath
    imgList = os.listdir(folderPath)
    
    # Iterate over all images inside folder
    for filename in imgList: 
      imagePath = folderPath + "/" + filename
      img = fr.load_image_file(imagePath)

    # Get encodings for all faces in current image
      faceEncodings = fr.face_encodings(img)

      # Para cada cara en la imagen
      for face in faceEncodings:

        # MAX Images  
        if index == n_images:
          breakUtility = True
          break

        tempCoords = list(face)

        for coord in face:
          tempCoords.append(coord)

        format = {"path": folderPath, "name": filename}

        rtreeIndex.insert(index, tempCoords, format)
        imagesList.append((index, imagePath))

        index = index + 1
        
      if breakUtility:
        break

    if breakUtility:
      break    
  rtreeIndex.close()

  print(str(index) + " images were processed.")

  return rtreeIndex

# -------------------------------------------------------------------------------------------

imagesList = os.listdir(path)

def encode(unencodedQuery):
    image = fr.load_image_file(unencodedQuery)
    return fr.face_encodings(image)[0]


def KNNSequentialIndex():
    dirList = os.listdir(path)

    count = 0
    names = []
    known = []
    raeachedN = False

    for filepath in dirList:

      folderPath = path + '/' + filepath
      imageList = os.listdir(folderPath)

      for imageFile in imageList:
        count += 1
        imagePath = folderPath + '/' + imageFile

        #processing this image

        image = fr.load_image_file(imagePath)
        encodings = fr.face_encodings(image)

        if encodings:
          names.append(imageFile)
          known.append(encodings[0])
        
        # if count > 100:
        #   return (known, names)
    
    return (known, names)


def KNNSequential(known, names, query, k, n):
  distancesList = fr.face_distance(known[:n], query)
  result = []
  if n <= len(known) and n <= len(names):
    for i in range(n):
      result.append((distancesList[i], names[i]))

  heapq.heapify(result)
  return heapq.nsmallest(k, result)

    
def KNNRtree(k, encodedQuery, n):
    rtree = 'RtreeIndexFile'
    prop = index.Property()
    prop.dimension = 128
    prop.buffering_capacity = 10
    rtreeIndex = index.Rtree(rtree, properties=prop)
    queryList = list(encodedQuery)

    for elem in encodedQuery:
        queryList.append(elem)
    return rtreeIndex.nearest(coordinates=queryList, num_results=k, objects='raw')


# rtreeName = 'RtreeIndexFile' + str(NImagenes)
# FacesRtree = image_indexing('RtreeIndexFile', 13000)

# result = list(KNNRtree(4, './data/saved/adam-sandler-test.jpeg', NImagenes))
# print(result[0]['name'])
