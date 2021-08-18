#coding:utf-8
#style
from flask import Blueprint, request,jsonify,redirect
from datetime import datetime
import numpy as np
import cv2
import base64
import config
import app.modules.video_transfer as transferModule
import tempfile
import imageio

style = Blueprint('style',__name__)

@style.route('/test', methods=['GET'])
def styleGetTest():
  transferModule.predict()
  return redirect('/static/output.mp4')

@style.route('', methods=['POST'])
def stylePost():
  # load style image
  styleImage = request.files['styleImage'].read()
  styleImage = np.fromstring(styleImage, np.uint8)
  styleImage = cv2.imdecode(styleImage, cv2.IMREAD_COLOR)[:,:,::-1]
  # load video
  videoFile = request.files['file']
  # get file enxention
  fileExtention = '.'+videoFile.filename.split('.')[1]
  # make temp file
  tempVideoFile = tempfile.NamedTemporaryFile()
  tempVideoFile.write(videoFile.read())
  reader = imageio.get_reader(tempVideoFile.name, fileExtention)

  # start transfer
  transferModule.predict(styleImage, reader)
  print('done')
  return redirect('/static/output.mp4')
  

# @style.route('', methods=['GET','POST'])
# def add():
#   if request.method == 'GET':
#     morphModule.image_to_video('', 'test')
#     with open('app/static/test.gif', "rb") as image_file:
#       encoded_string = base64.b64encode(image_file.read())
#       return jsonify({'filename':'test', 'result': str(encoded_string)})
#   else:
#     insertValues = request.get_json()
#     image1=insertValues['image1']
#     image2=insertValues['image2']
#     filename='img_'+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
#     if config.DEBUG:
#       filename='test'
#     morphModule.image_to_video(insertValues, filename)
#     with open('app/static/'+filename+'.gif', "rb") as image_file:
#       encoded_string = base64.b64encode(image_file.read())
#       return jsonify({'filename':filename, 'result': str(encoded_string)})

@style.route('/show')
def show():
  return redirect('/static/output.mp4')
