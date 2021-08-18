requirements.txt 裡面定義專按所需的套件，首次執行專案先執行以下指令

```bash
pip install -r requirements.txt
```

```
brew install cmake
$ brew info cmake
$ cmake --version
pip install dlib==19.9.0
pip install opencv-contrib-python
```


[Video Streaming Using Flask and OpenCV](https://medium.datadriveninvestor.com/video-streaming-using-flask-and-opencv-c464bf8473d6)




imageio
```py
# load video
videoFile = request.files['file']
# get file enxention
fileExtention = '.'+videoFile.filename.split('.')[1]
tempVideoFile = tempfile.NamedTemporaryFile(delete=False)
tempVideoFile.write(videoFile.read())
reader = imageio.get_reader(tempVideoFile.name, fileExtention)
for im in reader:
    print(im.shape)
```

cv2
```py
# load video
videoFile = request.files['file']
tempVideoFile = tempfile.NamedTemporaryFile(delete=False)
tempVideoFile.write(videoFile.read())
cap = cv2.VideoCapture(tempVideoFile.name)
# Read until video is completed
while(cap.isOpened()):
# Capture frame-by-frame
ret, frame = cap.read()
if ret == True:

    # Display the resulting frame
    print(frame.shape)
# Break the loop
else: 
    break
# When everything done, release the video capture object
cap.release()
```