@echo off
chcp 65001 >nul
title XTTS v2 環境設置

echo.
echo ================================================================
echo                    XTTS v2 環境設置工具
echo ================================================================
echo.

echo 🔍 檢查當前 Python 環境...
python --version
echo.

echo 📦 檢查 NumPy 版本...
python -c "import numpy; print('NumPy 版本:', numpy.__version__)" 2>nul
if errorlevel 1 (
    echo ❌ NumPy 未安裝
) else (
    echo ✅ NumPy 已安裝
)
echo.

echo 🤖 測試 XTTS v2 可用性...
python -c "from TTS.api import TTS; print('✅ XTTS v2 可用')" 2>nul
if errorlevel 1 (
    echo ❌ XTTS v2 不可用 - 可能是版本衝突
    echo.
    echo 💡 建議解決方案:
    echo    1. 創建虛擬環境
    echo    2. 降級 NumPy 版本
    echo    3. 重新安裝 TTS 套件
    echo.
    
    set /p choice="是否要自動修復? (y/n): "
    if /i "%choice%"=="y" (
        echo.
        echo 🔧 正在修復環境...
        echo 📥 卸載舊版 NumPy...
        python -m pip uninstall numpy -y
        
        echo 📦 安裝兼容版本 NumPy...
        python -m pip install "numpy==1.24.3"
        
        echo 🔄 重新安裝 TTS...
        python -m pip install --force-reinstall TTS
        
        echo.
        echo 🧪 重新測試 XTTS v2...
        python -c "from TTS.api import TTS; print('✅ XTTS v2 修復成功')" 2>nul
        if errorlevel 1 (
            echo ❌ 修復失敗，建議使用虛擬環境
        ) else (
            echo ✅ 修復成功！
            echo.
            echo 🎉 現在可以使用 XTTS v2 了！
            echo    測試命令: python test_xtts_simple.py
        )
    )
) else (
    echo ✅ XTTS v2 已可用！
    echo.
    echo 🎯 可以直接使用以下命令測試:
    echo    python test_xtts_simple.py
    echo    python xtts_reader.py "你好，我是 XTTS v2"
)

echo.
echo ================================================================
echo 設置完成
echo ================================================================
pause
