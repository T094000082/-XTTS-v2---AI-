#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 緩存測試腳本
用於測試模型緩存機制的效果
"""

import time
from tts_enhanced import EnhancedTTSReader

def test_cache_performance():
    """測試緩存性能"""
    print("🧪 XTTS v2 緩存機制測試")
    print("=" * 50)
    
    # 第一次初始化（可能需要下載或載入模型）
    print("\n🔄 第一次初始化 XTTS v2...")
    start_time = time.time()
    
    reader1 = EnhancedTTSReader()
    
    try:
        reader1.init_engine("xtts")
        first_load_time = time.time() - start_time
        print(f"✅ 第一次載入完成，耗時: {first_load_time:.2f} 秒")
        
        # 測試語音合成
        test_text = "這是第一次測試，正在驗證XTTS v2的緩存機制。"
        reader1.speak_text(test_text)
        
    except Exception as e:
        print(f"❌ 第一次初始化失敗: {e}")
        return
    
    # 第二次初始化（應該使用緩存）
    print("\n🔄 第二次初始化 XTTS v2...")
    start_time = time.time()
    
    reader2 = EnhancedTTSReader()
    
    try:
        reader2.init_engine("xtts")
        second_load_time = time.time() - start_time
        print(f"✅ 第二次載入完成，耗時: {second_load_time:.2f} 秒")
        
        # 測試語音合成
        test_text = "這是第二次測試，應該使用了緩存的模型。"
        reader2.speak_text(test_text)
        
        # 顯示性能比較
        print("\n📊 性能比較:")
        print(f"  第一次載入: {first_load_time:.2f} 秒")
        print(f"  第二次載入: {second_load_time:.2f} 秒")
        
        if second_load_time < first_load_time:
            speedup = first_load_time / second_load_time
            print(f"  🚀 加速比: {speedup:.1f}x 倍")
            print("  ✅ 緩存機制工作正常！")
        else:
            print("  ⚠️ 緩存效果不明顯，可能需要檢查")
            
    except Exception as e:
        print(f"❌ 第二次初始化失敗: {e}")
    
    # 顯示緩存狀態
    print("\n📋 最終緩存狀態:")
    cache_info = reader2.get_model_cache_info()
    print(f"  記憶體緩存: {'✅ 已載入' if cache_info['memory_cached'] else '❌ 未載入'}")
    print(f"  磁盤緩存: {'✅ 已下載' if cache_info['disk_cached'] else '❌ 未下載'}")
    
    if cache_info['cache_path']:
        print(f"  緩存路徑: {cache_info['cache_path']}")

if __name__ == "__main__":
    test_cache_performance()
