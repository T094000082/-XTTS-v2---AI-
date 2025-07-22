@echo off
chcp 65001 >nul
title 讀稿機 - 快速啟動

REM 快速啟動增強版讀稿機
echo 🚀 讀稿機快速啟動...

REM 設定路徑
set "APP_DIR=f:\VS_PJ\Python\語音模型_讀稿機"
cd /d "%APP_DIR%"

REM 直接執行
"%APP_DIR%\xtts_env\Scripts\python.exe" "%APP_DIR%\tts_enhanced.py"

REM 如果程式正常結束則不暫停，有錯誤才暫停
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 執行失敗
    pause
)
