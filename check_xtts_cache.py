#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版XTTS緩存測試
"""

import os
from pathlib import Path

def check_xtts_cache():
    """檢查XTTS v2緩存狀態"""
    print("🔍 檢查 XTTS v2 緩存狀態...")
    
    # 檢查磁盤緩存
    home_dir = Path.home()
    cache_dir = home_dir / ".cache" / "tts"
    model_path = cache_dir / "tts_models--multilingual--multi-dataset--xtts_v2"
    
    print(f"📁 緩存目錄: {cache_dir}")
    print(f"🎯 模型路徑: {model_path}")
    
    if model_path.exists():
        print("✅ 磁盤緩存: 已下載")
        print(f"📊 緩存大小: {get_folder_size(model_path):.1f} MB")
        
        # 檢查模型文件
        model_files = list(model_path.rglob("*"))
        print(f"📂 文件數量: {len(model_files)}")
        
        # 找出主要模型文件
        important_files = []
        for file in model_files:
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                if size_mb > 10:  # 大於10MB的文件
                    important_files.append((file.name, size_mb))
        
        if important_files:
            print("📋 主要模型文件:")
            for name, size in sorted(important_files, key=lambda x: x[1], reverse=True):
                print(f"  • {name}: {size:.1f} MB")
    else:
        print("❌ 磁盤緩存: 未下載")
        print("💡 首次使用XTTS v2時會自動下載約1.8GB模型")
    
    # 檢查環境變數
    print(f"\n🔧 環境設定:")
    print(f"COQUI_TOS_AGREED: {os.environ.get('COQUI_TOS_AGREED', '未設定')}")
    
    return model_path.exists()

def get_folder_size(folder_path):
    """計算資料夾大小（MB）"""
    total_size = 0
    for file in folder_path.rglob("*"):
        if file.is_file():
            total_size += file.stat().st_size
    return total_size / (1024 * 1024)

def main():
    print("🚀 XTTS v2 緩存檢查工具")
    print("=" * 40)
    
    has_cache = check_xtts_cache()
    
    print("\n" + "=" * 40)
    if has_cache:
        print("🎉 結論: XTTS v2 模型已緩存，使用時會更快！")
    else:
        print("⏳ 結論: 首次使用XTTS v2需要下載模型")
    
    return 0

if __name__ == "__main__":
    main()
