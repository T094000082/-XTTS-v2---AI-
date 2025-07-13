@echo off
chcp 65001 >nul
title 創建 XTTS v2 虛擬環境

echo.
echo ================================================================
echo                  創建 XTTS v2 專用虛擬環境
echo ================================================================
echo.

echo 🎯 這將創建一個專門用於 XTTS v2 的 Python 虛擬環境
echo    這樣可以避免與現有套件的版本衝突
echo.

set /p confirm="確認要創建虛擬環境嗎? (y/n): "
if /i not "%confirm%"=="y" (
    echo 操作已取消
    pause
    exit /b
)

echo.
echo 📁 創建虛擬環境 'xtts_env'...
python -m venv xtts_env
if errorlevel 1 (
    echo ❌ 虛擬環境創建失敗
    pause
    exit /b 1
)

echo ✅ 虛擬環境創建成功
echo.

echo 🔄 啟動虛擬環境...
call xtts_env\Scripts\activate.bat

echo.
echo 📦 安裝必要套件...
echo.

echo 1/4 升級 pip...
python -m pip install --upgrade pip

echo.
echo 2/4 安裝 NumPy (兼容版本)...
pip install "numpy<2.0"

echo.
echo 3/4 安裝 PyTorch...
pip install torch torchaudio

echo.
echo 4/4 安裝 XTTS v2...
pip install TTS pygame

echo.
echo 🧪 測試安裝結果...
python -c "from TTS.api import TTS; print('✅ XTTS v2 安裝成功!')" 2>nul
if errorlevel 1 (
    echo ❌ XTTS v2 安裝失敗
) else (
    echo ✅ XTTS v2 安裝成功！
    echo.
    echo 🎉 設置完成！
    echo.
    echo 📋 使用方法:
    echo    1. 啟動虛擬環境: xtts_env\Scripts\activate.bat
    echo    2. 測試 XTTS v2: python test_xtts_simple.py
    echo    3. 使用 XTTS v2: python xtts_reader.py "你的文字"
    echo    4. 退出虛擬環境: deactivate
    echo.
    
    set /p test_now="現在就測試 XTTS v2 嗎? (y/n): "
    if /i "%test_now%"=="y" (
        echo.
        echo 🔊 開始測試...
        python test_xtts_simple.py
    )
)

echo.
echo ================================================================
echo 虛擬環境設置完成
echo ================================================================
echo.
echo 💡 下次使用 XTTS v2 時，請先執行:
echo    xtts_env\Scripts\activate.bat
echo.
pause
