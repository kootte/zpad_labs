#!/bin/bash
sudo apt-get update
sudo apt-get install -y libopencv-dev cmake gcc g++ wget

wget -nc https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
wget -nc https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
