#!/bin/bash
if [ -f "build/Lab6" ]; then
    echo "Запуск програми..."
    ./build/Lab6
else
    echo "Помилка: Виконуваний файл не знайдено. Спочатку запустіть ./build.sh"
fi
