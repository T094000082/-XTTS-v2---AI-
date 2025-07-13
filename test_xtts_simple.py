#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 測試程式 - 最簡版
直接測試 XTTS v2 是否可用
"""

def test_xtts_simple():
    """簡單測試 XTTS v2"""
    try:
        print("🧪 測試 XTTS v2 導入...")
        
        # 嘗試導入 TTS
        from TTS.api import TTS
        print("✅ TTS.api 導入成功")
        
        # 嘗試導入其他必要套件
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
        
        import pygame
        pygame.mixer.init()
        print("✅ pygame 初始化成功")
        
        # 嘗試創建 XTTS v2 實例
        print("🤖 正在創建 XTTS v2 實例...")
        print("   (首次使用會下載模型，請稍候...)")
        print("   自動同意 XTTS v2 使用條款...")
        
        # 自動同意條款
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
        print("✅ XTTS v2 創建成功！")
        
        return tts
        
    except Exception as e:
        print(f"❌ XTTS v2 測試失敗: {e}")
        return None

def speak_xtts_test(tts, text="你好，我是 XTTS v2 語音合成系統"):
    """使用 XTTS v2 進行測試語音合成"""
    try:
        import tempfile
        import os
        import pygame
        
        print(f"🔊 XTTS v2 正在合成: {text}")
        
        # 創建臨時檔案
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_path = temp_file.name
        
        # 生成語音
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            language="zh"
        )
        
        print("🎵 正在播放 XTTS v2 語音...")
        
        # 播放語音
        pygame.mixer.music.load(output_path)
        pygame.mixer.music.play()
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        print("✅ XTTS v2 語音播放完成！")
        
        # 清理
        try:
            os.unlink(output_path)
        except OSError:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ XTTS v2 語音合成失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 XTTS v2 簡單測試")
    print("=" * 40)
    
    # 測試 XTTS v2
    tts = test_xtts_simple()
    
    if tts:
        print("\n🎯 開始語音合成測試...")
        success = speak_xtts_test(tts)
        
        if success:
            print("\n🎉 XTTS v2 測試完全成功！")
            print("您現在可以使用 XTTS v2 進行高品質語音合成了。")
        else:
            print("\n⚠️  XTTS v2 創建成功但語音合成失敗")
    else:
        print("\n❌ XTTS v2 測試失敗")
        print("可能的原因:")
        print("1. 套件版本衝突")
        print("2. 缺少必要的依賴")
        print("3. 網路問題 (下載模型失敗)")
    
    print("\n" + "=" * 40)
