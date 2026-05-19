#include <opencv2/opencv.hpp>
#include <iostream>
#include "FaceDetector.hpp"

class CameraProvider {
    cv::VideoCapture cap;
public:
    // Змінили конструктор, щоб він приймав URL-адресу замість індексу (0)
    CameraProvider(const std::string& url) { 
        cap.open(url); 
    }
    cv::Mat getFrame() {
        cv::Mat frame;
        cap >> frame;
        return frame;
    }
    bool isOpened() { return cap.isOpened(); }
};

class KeyProcessor {
public:
    enum Mode { NORMAL, FACE_DETECT, QUIT };
    Mode currentMode = NORMAL;
    
    void process(int key) {
        if (key == 'q' || key == 27) currentMode = QUIT;
        else if (key == 'f' || key == 'F') currentMode = FACE_DETECT;
        else if (key == 'n' || key == 'N') currentMode = NORMAL;
    }
};

class Display {
public:
    void show(const std::string& windowName, const cv::Mat& frame) {
        cv::imshow(windowName, frame);
    }
};

int main() {
   
    std::string droidCamUrl = "http://192.168.1.100:4747/video"; 
    
    CameraProvider camera(droidCamUrl);
    if (!camera.isOpened()) {
        std::cerr << "Помилка: неможливо підключитися до DroidCam за адресою: " << droidCamUrl << std::endl;
        std::cerr << "Перевір IP-адресу та чи запущено додаток на телефоні." << std::endl;
        return -1;
    }

    FaceDetector faceDetector("../deploy.prototxt", "../res10_300x300_ssd_iter_140000.caffemodel");
    KeyProcessor keyProcessor;
    Display display;

    while (keyProcessor.currentMode != KeyProcessor::QUIT) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) {
            std::cerr << "Втрачено з'єднання з камерою!" << std::endl;
            break;
        }

        if (keyProcessor.currentMode == KeyProcessor::FACE_DETECT) {
            faceDetector.setFrame(frame);
            
            std::vector<cv::Rect> faces = faceDetector.getFaces();
            for (const auto& face : faces) {
                cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2);
            }
        }

        display.show("Lab 7 (DroidCam)", frame);
        
        int key = cv::waitKey(30);
        if (key >= 0) {
            keyProcessor.process(key);
        }
    }
    return 0;
}
