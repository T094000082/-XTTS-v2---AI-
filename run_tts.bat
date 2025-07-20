@echo off
REM 激活虛擬環境並運行讀稿機程式
cd /d "%~dp0"

REM 檢查虛擬環境是否存在
if not exist "xtts_env\Scripts\activate.bat" (
    echo ❌ 錯誤: 虛擬環境不存在
    echo 請先執行 create_xtts_env.bat 創建虛擬環境
    pause
    exit /b 1
)

REM 激活虛擬環境
call xtts_env\Scripts\activate.bat

REM 檢查是否有參數
if "%~1"=="" (
    echo 📢 讀稿機程式使用方式:
    echo run_tts.bat "你要朗讀的文字"
    echo 範例: run_tts.bat "Hello World 你好世界"
    pause
) else (
    REM 運行讀稿機程式
    python tts_final.py %*
)

REM 保持命令視窗開啟
pause
