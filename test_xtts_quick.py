#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 快速測試 - 自動同意條款版本
"""

import os
# 設置環境變量自動同意條款
os.environ["COQUI_TOS_AGREED"] = "1"

def test_xtts_quick():
    """快速測試 XTTS v2"""
    try:
        print("🧪 測試 XTTS v2 導入...")
        
        # 導入必要套件
        from TTS.api import TTS
        import torch
        import numpy as np
        
        print("✅ TTS.api 導入成功")
        print(f"✅ PyTorch 版本: {torch.__version__}")
        print(f"✅ NumPy 版本: {np.__version__}")
        
        # 檢查 CUDA 是否可用
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✅ 使用設備: {device}")
        
        # 創建 XTTS v2 實例
        print("🤖 正在創建 XTTS v2 實例...")
        print("   (首次使用會下載模型，請稍候...)")
        
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("✅ XTTS v2 創建成功！")
        
        # 簡單測試語音合成
        print("🔊 測試語音合成...")
        test_text = "你好，這是 XTTS v2 測試"
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_path = temp_file.name
        
        # 生成語音 (添加說話者參數)
        tts.tts_to_file(
            text=test_text,
            file_path=output_path,
            language="zh",
            speaker_wav=None  # 使用默認說話者
        )
        
        print(f"✅ 語音文件已生成: {output_path}")
        
        # 檢查文件大小
        file_size = os.path.getsize(output_path)
        print(f"✅ 文件大小: {file_size} bytes")
        
        if file_size > 1000:  # 如果文件大於 1KB，應該是成功的
            print("🎉 XTTS v2 測試完全成功！")
            print("✅ 語音合成正常工作")
            return True
        else:
            print("⚠️  語音文件太小，可能有問題")
            return False
            
    except Exception as e:
        print(f"❌ XTTS v2 測試失敗: {e}")
        import traceback
        print("詳細錯誤信息:")
        traceback.print_exc()
        return False
    finally:
        # 清理臨時文件
        try:
            if 'output_path' in locals():
                os.unlink(output_path)
        except:
            pass

if __name__ == "__main__":
    print("🚀 XTTS v2 快速測試")
    print("=" * 50)
    
    success = test_xtts_quick()
    
    if success:
        print("\n🎯 測試結果: 成功！")
        print("XTTS v2 已正確安裝並可以使用")
        print("\n📝 接下來您可以:")
        print("1. 運行 xtts_reader.py 進行語音合成")
        print("2. 運行 tts_compare.py 比較不同 TTS 引擎")
    else:
        print("\n❌ 測試結果: 失敗")
        print("請檢查安裝或查看錯誤信息")
    
    print("=" * 50)
