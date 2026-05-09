#pragma once
#include <opencv2/opencv.hpp>
#include <string>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    FrameProcessor(const std::string& windowName);
    void process(cv::Mat& frame, Mode mode);
    
    // Статичний метод для обробки подій миші
    static void onMouse(int event, int x, int y, int flags, void* userdata);

private:
    std::string winName;
    int brightness;
    int64 prevTime;

    // Дані для малювання мишкою
    bool isDrawing;
    cv::Point startPt;
    cv::Rect drawRect;

    double getFPS();
    void applyBrightness(cv::Mat& frame);
    void drawOverlay(cv::Mat& frame, double fps);
};
