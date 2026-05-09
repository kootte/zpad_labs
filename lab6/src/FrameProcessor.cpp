#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor(const std::string& windowName) 
    : winName(windowName), brightness(50), isDrawing(false), prevTime(cv::getTickCount()) {
    
    // Створюємо Trackbar для регулювання яскравості
    cv::createTrackbar("Brightness", winName, &brightness, 100);
    
    // Встановлюємо callback для миші
    cv::setMouseCallback(winName, FrameProcessor::onMouse, this);
}

void FrameProcessor::onMouse(int event, int x, int y, int flags, void* userdata) {
    FrameProcessor* fp = static_cast<FrameProcessor*>(userdata);
    
    if (event == cv::EVENT_LBUTTONDOWN) {
        fp->isDrawing = true;
        fp->startPt = cv::Point(x, y);
        fp->drawRect = cv::Rect(x, y, 0, 0);
    } else if (event == cv::EVENT_MOUSEMOVE && fp->isDrawing) {
        fp->drawRect = cv::Rect(fp->startPt, cv::Point(x, y));
    } else if (event == cv::EVENT_LBUTTONUP) {
        fp->isDrawing = false;
        fp->drawRect = cv::Rect(fp->startPt, cv::Point(x, y));
    }
}

double FrameProcessor::getFPS() {
    int64 currTime = cv::getTickCount();
    double fps = cv::getTickFrequency() / (currTime - prevTime);
    prevTime = currTime;
    return fps;
}

void FrameProcessor::applyBrightness(cv::Mat& frame) {
    // brightness: 0-100. 50 - без змін. <50 - темніше, >50 - світліше.
    int beta = (brightness - 50) * 2; 
    frame.convertTo(frame, -1, 1.0, beta);
}

void FrameProcessor::drawOverlay(cv::Mat& frame, double fps) {
    std::string fpsText = "FPS: " + std::to_string((int)fps);
    cv::putText(frame, fpsText, cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 0), 2);
}

void FrameProcessor::process(cv::Mat& frame, Mode mode) {
    if (frame.empty()) return;

    applyBrightness(frame);
    double fps = getFPS();

    switch (mode) {
        case Mode::INVERT:
            cv::bitwise_not(frame, frame);
            break;
        case Mode::BLUR:
            cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0);
            break;
        case Mode::CANNY: {
            cv::Mat gray, edges;
            cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
            cv::Canny(gray, edges, 50, 150);
            cv::cvtColor(edges, frame, cv::COLOR_GRAY2BGR);
            break;
        }
        case Mode::DRAW:
            // Якщо малюємо, відображаємо прямокутник
            if (drawRect.width > 0 || drawRect.height > 0) {
                cv::rectangle(frame, drawRect, cv::Scalar(0, 0, 255), 3);
            }
            break;
        case Mode::NORMAL:
        default:
            break;
    }

    drawOverlay(frame, fps);
}
