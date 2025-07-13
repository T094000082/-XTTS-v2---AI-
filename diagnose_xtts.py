#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 診斷工具 - 找出失敗原因
"""

import os
os.environ["COQUI_TOS_AGREED"] = "1"

def diagnose_xtts_issues():
    """診斷 XTTS v2 問題"""
    print("🔍 XTTS v2 問題診斷工具")
    print("=" * 50)
    
    # 1. 檢查基本導入
    print("1️⃣ 檢查基本套件導入...")
    try:
        import sys
        print(f"✅ Python 版本: {sys.version}")
        
        import numpy as np
        print(f"✅ NumPy 版本: {np.__version__}")
        
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
        
        import pygame
        print(f"✅ Pygame 版本: {pygame.version.ver}")
        
    except Exception as e:
        print(f"❌ 基本導入失敗: {e}")
        return False
    
    # 2. 檢查 TTS 導入
    print("\n2️⃣ 檢查 TTS 導入...")
    try:
        from TTS.api import TTS
        print("✅ TTS.api 導入成功")
    except Exception as e:
        print(f"❌ TTS 導入失敗: {e}")
        print("💡 建議: 重新安裝 TTS")
        return False
    
    # 3. 檢查模型列表
    print("\n3️⃣ 檢查可用模型...")
    try:
        models = TTS.list_models()
        xtts_models = [m for m in models if 'xtts' in m.lower()]
        print(f"✅ 找到 {len(xtts_models)} 個 XTTS 模型:")
        for model in xtts_models:
            print(f"   - {model}")
    except Exception as e:
        print(f"❌ 模型列表獲取失敗: {e}")
    
    # 4. 嘗試創建簡單實例
    print("\n4️⃣ 嘗試創建 TTS 實例...")
    try:
        print("   正在創建實例（可能需要下載模型）...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print("✅ TTS 實例創建成功")
        
        # 檢查說話者信息
        print("\n5️⃣ 檢查說話者信息...")
        if hasattr(tts, 'speakers') and tts.speakers:
            print(f"✅ 找到 {len(tts.speakers)} 個說話者:")
            for i, speaker in enumerate(tts.speakers[:5]):
                print(f"   {i+1}. {speaker}")
        else:
            print("⚠️  沒有找到說話者列表")
            
            # 檢查其他屬性
            attrs = ['speaker_manager', 'language_manager', 'speakers_file']
            for attr in attrs:
                if hasattr(tts, attr):
                    print(f"   找到屬性: {attr} = {getattr(tts, attr)}")
        
        return tts
        
    except Exception as e:
        print(f"❌ TTS 實例創建失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_simple_synthesis(tts):
    """測試簡單語音合成"""
    print("\n6️⃣ 測試最簡單的語音合成...")
    
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name
    
    # 嘗試最基本的合成
    try:
        print("   嘗試最基本的 tts() 方法...")
        wav = tts.tts("Hello world")
        print(f"✅ 基本合成成功，音頻長度: {len(wav)} samples")
        
        # 保存並檢查
        import soundfile as sf
        sf.write(output_path, wav, 22050)
        
        size = os.path.getsize(output_path)
        print(f"✅ 文件保存成功，大小: {size} bytes")
        
        if size > 1000:
            print("🎉 簡單語音合成測試成功！")
            return True
        else:
            print("⚠️  文件太小，可能有問題")
            
    except Exception as e:
        print(f"❌ 簡單合成失敗: {e}")
        
        # 嘗試帶參數的合成
        try:
            print("   嘗試帶參數的合成...")
            wav = tts.tts("Hello world", speaker_idx=0)
            print("✅ 帶參數合成成功")
            return True
        except Exception as e2:
            print(f"❌ 帶參數合成也失敗: {e2}")
    
    finally:
        try:
            os.unlink(output_path)
        except:
            pass
    
    return False

def main():
    """主診斷流程"""
    print("🚀 開始診斷...")
    
    tts = diagnose_xtts_issues()
    
    if tts:
        success = test_simple_synthesis(tts)
        
        print("\n" + "=" * 50)
        if success:
            print("🎯 診斷結果: XTTS v2 基本可用")
            print("💡 建議嘗試使用最簡單的調用方式")
        else:
            print("❌ 診斷結果: XTTS v2 存在問題")
            print("🛠️  可能需要重新安裝或使用不同的模型")
    else:
        print("\n" + "=" * 50)
        print("❌ 診斷結果: TTS 無法正常工作")
        print("🛠️  建議重新創建虛擬環境")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
