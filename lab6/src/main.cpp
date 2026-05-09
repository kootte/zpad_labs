#include <iostream>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

int main() {
    std::cout << "Ініціалізація програми..." << std::endl;

    CameraProvider camera(0);
    if (!camera.isOpened()) {
        return -1;
    }

    std::string windowName = "Lab6: Video Processing";
    Display display(windowName);
    
    
    FrameProcessor frameProcessor(display.getWindowName());
    KeyProcessor keyProcessor;

    std::cout << "Готово! Натисніть 1-5 для зміни режимів, ESC або Q для виходу." << std::endl;

    while (!keyProcessor.shouldExit()) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) {
            std::cerr << "Помилка: Порожній кадр!" << std::endl;
            break;
        }

        
        frameProcessor.process(frame, keyProcessor.getCurrentMode());

        
        display.show(frame);

        
        int key = cv::waitKey(10);
        if (key != -1) {
            keyProcessor.processKey(key);
        }
    }

    std::cout << "Завершення роботи..." << std::endl;
    return 0;
}
