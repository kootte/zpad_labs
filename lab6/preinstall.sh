#!/bin/bash
echo "Встановлення необхідних залежностей..."
sudo apt-get update
sudo apt-get install -y build-essential cmake libopencv-dev gcc g++
echo "Залежності успішно встановлено!"
