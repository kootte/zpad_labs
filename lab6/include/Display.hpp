#pragma once
#include <opencv2/opencv.hpp>
#include <string>

class Display {
public:
    Display(const std::string& windowName);
    ~Display();
    void show(const cv::Mat& frame);
    std::string getWindowName() const;

private:
    std::string winName;
};
