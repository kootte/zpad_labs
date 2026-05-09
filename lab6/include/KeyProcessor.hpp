#pragma once

enum class Mode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    DRAW
};

class KeyProcessor {
public:
    KeyProcessor();
    void processKey(int key);
    Mode getCurrentMode() const;
    bool shouldExit() const;

private:
    Mode currentMode;
    bool exitFlag;
};
