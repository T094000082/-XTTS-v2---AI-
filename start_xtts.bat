@echo off
chcp 65001 >nul
title XTTS v2 讀稿機

echo.
echo ================================================================
echo                     XTTS v2 讀稿機啟動器
echo ================================================================
echo.

if "%~1"=="" (
    echo 用法: start_xtts.bat "您要朗讀的文字"
    echo.
    echo 範例:
    echo   start_xtts.bat "你好，歡迎使用 XTTS v2"
    echo   start_xtts.bat "這是高品質的語音合成"
    echo.
    pause
    exit /b 1
)

echo 🚀 啟動 XTTS v2 讀稿機...
echo 📝 文字內容: %~1
echo.

rem 使用虛擬環境中的 Python
xtts_env\Scripts\python.exe xtts_reader.py %~1

echo.
echo ================================================================
echo XTTS v2 執行完成
echo ================================================================
pause
