#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from skimage import io
from skimage.transform import resize
import os
import sys
import imageio
import base64


def get_face_landmark(image):
    points = []
    image = image.copy()
    shape_predictor = 'app/modules/shape_predictor_68_face_landmarks.dat'
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    # load the input image, resize it, and convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    rects = detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the face number
        cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        for (x, y) in shape:
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

        for (x, y) in shape:
            points.append((int(x), int(y)))

    resultTag = True
    if len(rects) == 0 : 
        resultTag = False
    return resultTag, image[:,:,::-1], points

# ## faceMorph

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []


    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask

# Gets delaunay 2D segmentation and return a list with the the triangles' indexes
def get_delaunay_indexes(image, points) :

    rect = (0, 0, image.shape[1], image.shape[0])
    subdiv = cv2.Subdiv2D(rect);
    for p in points :
        subdiv.insert( p )

    triangleList = subdiv.getTriangleList();
    triangles = []
    for p in triangleList :
        vertexes = [0, 0, 0]
        for v in range(3) :
            vv = v * 2
            for i in range(len(points)) :
                if p[vv] == points[i][0] and p[vv+1] == points[i][1] :
                    vertexes[v] = i

        triangles.append(vertexes)

    return triangles

# cv2 to base64
def cv2_base64(image):
    base64_str = cv2.imencode('.jpg',image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str

# base64 to cv2
def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString,np.uint8)  
    image = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    return image

def image_to_video(insertValues, filename):
    # config
    videoPath='app/static/'+filename+'.gif'
    nframes=10
    fps=4
    writer = imageio.get_writer(videoPath, fps=fps)
    # writer = imageio.get_writer(videoPath)
    # Read images
    if insertValues=='':
        img1 = cv2.imread('app/image/cat.jpg')
        img2 = cv2.imread('app/image/dog.jpg')
    else:
        img1=base64_cv2(insertValues['image1'])
        img2=base64_cv2(insertValues['image2'])
    # Resize image
    img1 = cv2.resize(img1, (254, 254), interpolation=cv2.INTER_AREA)
    img2 = cv2.resize(img2, (254, 254), interpolation=cv2.INTER_AREA)

    # GET two image points
    resultTag1, img_landmark1, points1 = get_face_landmark(img1)
    resultTag2, img_landmark2, points2 = get_face_landmark(img2)
    ## Write 4 sec image 1
    for i in range(fps*1):
        writer.append_data(np.uint8(img1[:,:,::-1]))
    
    # Convert Mat to float data type
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    # Read array of corresponding points
    points = []

    # Append 8 additional points: corners and half way points
    size = img1.shape
    h = size[0]
    w = size[1]
    h2 = int(size[0]/2)
    w2 = int(size[1]/2)

    points1.append( (0    , 0    ) )
    points1.append( (0    , h - 1) )
    points1.append( (w - 1, 0    ) )
    points1.append( (w - 1, h - 1) )

    points1.append( (0    , h2   ) )
    points1.append( (w2   , 0    ) )
    points1.append( (w - 1, h2   ) )
    points1.append( (w2   , h - 1) )

    size = img2.shape
    h = size[0]
    w = size[1]
    h2 = int(size[0]/2)
    w2 = int(size[1]/2)

    points2.append( (0    , 0    ) )
    points2.append( (0    , h - 1) )
    points2.append( (w - 1, 0    ) )
    points2.append( (w - 1, h - 1) )

    points2.append( (0    , h2   ) )
    points2.append( (w2   , 0    ) )
    points2.append( (w - 1, h2   ) )
    points2.append( (w2   , h - 1) )

    # Delaunay points
    delaunay = get_delaunay_indexes(img1,points1)

    # Alpha values
    alpha_values = []

    if nframes :
        # Number of intermediate frames (morphing frames)
        alpha_values = np.linspace(0, 100, int(nframes))

    else: 
        # Single alpha morph blending
        alpha_values = [ float(args["alpha"]) ]

    # Main loop
    for (f, a) in enumerate(alpha_values) :

        alpha = float(a) / 100
        
        # Uncomment these lines to make loop-back effect
        # alpha = 2 * alpha
        # if alpha > 1 :  alpha = 2 - alpha
        
        # Comment this line to get a cartoon effect 
        points = []         

        # Compute weighted average point coordinates
        for i in range(0, len(points1)):
            x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
            y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
            points.append((x,y))

        # Allocate space for final output
        imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

        for v1, v2, v3 in delaunay :
                        
            t1 = [points1[v1], points1[v2], points1[v3]]
            t2 = [points2[v1], points2[v2], points2[v3]]
            t  = [ points[v1],  points[v2],  points[v3]]

            # Morph one triangle at a time.
            morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)

        # Save morphing frame
        index = []
        if nframes :
            index = str(f).zfill(4)
        else : index = 'a' + str(int(a)).zfill(4)
        writer.append_data(np.uint8(imgMorph[:,:,::-1]))
    ## Write 4 sec image 2
    for i in range(fps*1):
        writer.append_data(np.uint8(img2[:,:,::-1]))
    writer.close()



def getResult():
    return 'ddon'