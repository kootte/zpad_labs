#include "Display.hpp"

Display::Display(const std::string& windowName) : winName(windowName) {
    cv::namedWindow(winName, cv::WINDOW_AUTOSIZE);
}

Display::~Display() {
    cv::destroyWindow(winName);
}

void Display::show(const cv::Mat& frame) {
    if (!frame.empty()) {
        cv::imshow(winName, frame);
    }
}

std::string Display::getWindowName() const {
    return winName;
}
