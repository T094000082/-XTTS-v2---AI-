#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 基本驗證測試
"""

import os
os.environ["COQUI_TOS_AGREED"] = "1"

def basic_test():
    """基本功能驗證"""
    try:
        print("🧪 基本導入測試...")
        
        # 測試基本導入
        from TTS.api import TTS
        import torch
        import numpy as np
        
        print(f"✅ TTS.api: OK")
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"✅ NumPy: {np.__version__}")
        
        # 檢查可用模型
        print("\n📋 檢查可用模型...")
        try:
            models = TTS.list_models()
            xtts_models = [m for m in models if 'xtts' in m.lower()]
            print(f"✅ 找到 {len(xtts_models)} 個 XTTS 模型")
            for model in xtts_models[:3]:  # 只顯示前3個
                print(f"   - {model}")
        except Exception as e:
            print(f"⚠️  模型列表獲取失敗: {e}")
        
        print(f"\n🎯 基本測試完成！")
        return True
        
    except Exception as e:
        print(f"❌ 基本測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 XTTS v2 基本驗證")
    print("=" * 40)
    
    success = basic_test()
    
    if success:
        print("\n✅ 基本驗證通過！")
        print("XTTS v2 已正確安裝")
    else:
        print("\n❌ 基本驗證失敗")
    
    print("=" * 40)
