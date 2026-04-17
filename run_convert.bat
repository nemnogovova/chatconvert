@echo off
setlocal
cd /d "%~dp0"

echo [1/3] Проверка наличия Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не установлен! Пожалуйста, установите Python.
    pause
    exit /b
)

echo [2/3] Установка необходимых библиотек (BeautifulSoup4)...
pip install beautifulsoup4 --quiet

echo [3/3] Запуск конвертации...
python convert.py

echo.
echo Обработка завершена.
pause