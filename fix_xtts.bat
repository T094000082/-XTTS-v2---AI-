@echo off
chcp 65001 >nul
title 修復 XTTS v2 問題

echo.
echo ================================================================
echo                    修復 XTTS v2 問題
echo ================================================================
echo.

echo 🔧 這將修復 XTTS v2 的依賴和配置問題
echo.

set /p confirm="確認要修復 XTTS v2 嗎? (y/n): "
if /i not "%confirm%"=="y" (
    echo 操作已取消
    pause
    exit /b
)

echo.
echo 🔄 啟動虛擬環境...
call xtts_env\Scripts\activate.bat

echo.
echo 📦 修復依賴問題...
echo.

echo 1/5 卸載可能有問題的 NumPy...
python -m pip uninstall numpy -y

echo.
echo 2/5 安裝兼容的 NumPy 版本...
python -m pip install "numpy==1.24.3"

echo.
echo 3/5 重新安裝 TTS...
python -m pip uninstall TTS -y
python -m pip install TTS

echo.
echo 4/5 安裝額外的音頻處理套件...
python -m pip install soundfile librosa

echo.
echo 5/5 清除模型緩存...
python -c "import os, shutil; cache_dir = os.path.expanduser('~/.cache/tts'); shutil.rmtree(cache_dir, ignore_errors=True); print('✅ 緩存已清除')"

echo.
echo 🧪 測試修復結果...
python -c "import os; os.environ['COQUI_TOS_AGREED'] = '1'; from TTS.api import TTS; print('✅ TTS 導入成功'); tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2'); print('✅ XTTS v2 創建成功')"

if errorlevel 1 (
    echo ❌ 修復失敗，嘗試替代方案...
    echo.
    echo 🔄 使用替代 TTS 模型...
    python -c "import os; os.environ['COQUI_TOS_AGREED'] = '1'; from TTS.api import TTS; tts = TTS('tts_models/zh-CN/baker/tacotron2-DDC-GST'); print('✅ 中文 TTS 模型可用')"
    
    if errorlevel 1 (
        echo ❌ 所有 TTS 模型都失敗
        echo.
        echo 💡 建議方案:
        echo    1. 檢查網路連接
        echo    2. 重新創建虛擬環境
        echo    3. 使用系統內建 TTS
    ) else (
        echo ✅ 替代 TTS 模型可用！
        echo.
        echo 📋 使用替代模型的方法:
        echo    python simple_tts.py "您的文字"
    )
) else (
    echo ✅ XTTS v2 修復成功！
    echo.
    echo 🎉 修復完成！
    echo.
    echo 📋 測試方法:
    echo    1. python diagnose_xtts.py  # 診斷測試
    echo    2. python xtts_reader.py "測試文字"  # 實際使用
    echo    3. python tts_compare.py  # 比較測試
    echo.
    
    set /p test_now="現在就測試 XTTS v2 嗎? (y/n): "
    if /i "%test_now%"=="y" (
        echo.
        echo 🔊 開始測試...
        python diagnose_xtts.py
    )
)

echo.
echo ================================================================
echo 修復作業完成
echo ================================================================
echo.
pause
