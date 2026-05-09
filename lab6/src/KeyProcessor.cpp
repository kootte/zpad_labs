#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(Mode::NORMAL), exitFlag(false) {}

void KeyProcessor::processKey(int key) {
    switch (key) {
        case '1': currentMode = Mode::NORMAL; break;
        case '2': currentMode = Mode::INVERT; break;
        case '3': currentMode = Mode::BLUR; break;
        case '4': currentMode = Mode::CANNY; break;
        case '5': currentMode = Mode::DRAW; break;
        case 27:  // ESC
        case 'q':
        case 'Q': exitFlag = true; break;
        default: break;
    }
}

Mode KeyProcessor::getCurrentMode() const {
    return currentMode;
}

bool KeyProcessor::shouldExit() const {
    return exitFlag;
}
