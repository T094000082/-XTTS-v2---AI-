@echo off
echo 正在安裝讀稿機程式所需的套件...
echo.

echo 正在升級 pip...
C:/Users/user/AppData/Local/Programs/Python/Python312/python.exe -m pip install --upgrade pip

echo.
echo 正在安裝基本套件...
C:/Users/user/AppData/Local/Programs/Python/Python312/python.exe -m pip install pyttsx3 pywin32

echo.
echo 正在安裝 XTTS v2 相關套件...
C:/Users/user/AppData/Local/Programs/Python/Python312/python.exe -m pip install -r requirements.txt

echo.
echo 安裝完成！
echo.
echo 使用方法:
echo   基本版本: python simple_tts.py "你好世界"
echo   進階版本: python tts_reader.py "你好世界"
echo.
pause
