#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
public:
    FaceDetector(const std::string& prototxt, const std::string& model);
    ~FaceDetector();

    void setFrame(const cv::Mat& frame);
    std::vector<cv::Rect> getFaces();

private:
    void worker();

    cv::dnn::Net net;
    std::thread detectorThread;
    std::mutex mtx;
    std::atomic<bool> running;
    
    cv::Mat currentFrame;
    bool hasNewFrame;
    std::vector<cv::Rect> detectedFaces;
};
