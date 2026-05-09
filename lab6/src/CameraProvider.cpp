#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider(int deviceId) {
    cap.open("http://192.168.1.100:4747/video");
    if (!cap.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити камеру!" << std::endl;
    }
}

CameraProvider::~CameraProvider() {
    if (cap.isOpened()) {
        cap.release();
    }
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}

bool CameraProvider::isOpened() const {
    return cap.isOpened();
}
