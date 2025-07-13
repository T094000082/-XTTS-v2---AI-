#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試虛擬環境的套件安裝狀態
"""

import sys
print(f"Python 路徑: {sys.executable}")
print(f"Python 版本: {sys.version}")

try:
    import numpy
    print(f"✅ NumPy 版本: {numpy.__version__}")
except ImportError as e:
    print(f"❌ NumPy 導入失敗: {e}")

try:
    import torch
    print(f"✅ PyTorch 版本: {torch.__version__}")
except ImportError as e:
    print(f"❌ PyTorch 導入失敗: {e}")

try:
    from TTS.api import TTS
    print("✅ XTTS v2 (TTS) 導入成功！")
    
    # 顯示可用的 TTS 模型
    print("\n📋 可用的 TTS 模型:")
    tts_models = TTS.list_models()
    for model in tts_models:
        if 'xtts' in model.lower():
            print(f"  - {model}")
            
except ImportError as e:
    print(f"❌ XTTS v2 (TTS) 導入失敗: {e}")

try:
    import pygame
    print(f"✅ Pygame 版本: {pygame.version.ver}")
except ImportError as e:
    print(f"❌ Pygame 導入失敗: {e}")

print("\n🎯 測試完成！")
