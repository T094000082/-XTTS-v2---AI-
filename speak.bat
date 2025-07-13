@echo off
chcp 65001 >nul
title 讀稿機程式

echo.
echo ================================================================
echo                        讀稿機程式 v1.0
echo ================================================================
echo.

if "%~1"=="" (
    echo 使用方法: speak.bat "你要朗讀的文字"
    echo.
    echo 範例:
    echo   speak.bat "你好世界"
    echo   speak.bat "Hello World"
    echo.
    echo 其他選項:
    echo   speak.bat --test     執行測試
    echo   speak.bat --info     顯示引擎資訊  
    echo   speak.bat --voices   列出可用語音
    echo   speak.bat --help     顯示詳細說明
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"
C:/Users/user/AppData/Local/Programs/Python/Python312/python.exe tts_final.py %*

if errorlevel 1 (
    echo.
    echo 程式執行失敗，請檢查錯誤訊息
    pause
)
