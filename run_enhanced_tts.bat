@echo off
title 增強版讀稿機 - TXT檔念稿與MP3錄製
chcp 65001 >nul

echo ================================================
echo 增強版讀稿機 - 啟動中...
echo ================================================

REM 設定工作目錄
set "WORK_DIR=f:\VS_PJ\Python\語音模型_讀稿機"
cd /d "%WORK_DIR%"

REM 檢查虛擬環境是否存在
if not exist "xtts_env\Scripts\python.exe" (
    echo ❌ 虛擬環境不存在
    echo 💡 請先執行 create_xtts_env.bat 創建虛擬環境
    pause
    exit /b 1
)

REM 檢查程式檔案是否存在
if not exist "tts_enhanced.py" (
    echo ❌ 增強版讀稿機程式不存在
    echo 💡 請確認 tts_enhanced.py 檔案存在
    pause
    exit /b 1
)

echo 🔧 使用虛擬環境 Python...
echo 📁 工作目錄: %WORK_DIR%

REM 直接使用虛擬環境的 Python 執行程式
"%WORK_DIR%\xtts_env\Scripts\python.exe" "%WORK_DIR%\tts_enhanced.py" %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 程式執行失敗，錯誤碼: %ERRORLEVEL%
    echo 💡 可能的原因:
    echo    1. 虛擬環境套件不完整
    echo    2. Python 程式有語法錯誤
    echo    3. 缺少必要的依賴套件
    echo.
    echo 🔧 建議解決方案:
    echo    1. 重新安裝套件: setup_xtts.bat
    echo    2. 檢查程式語法
    echo    3. 查看詳細錯誤訊息
    pause
    exit /b %ERRORLEVEL%
) else (
    echo ✅ 程式執行完成
)
