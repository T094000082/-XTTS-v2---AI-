#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增強版讀稿機示範腳本
展示新功能的使用方法
"""

import os
import sys

def demo_enhanced_tts():
    """示範增強版讀稿機的新功能"""
    print("🎉 增強版讀稿機功能示範")
    print("=" * 50)
    
    # 設定基本路徑
    base_path = "f:/VS_PJ/Python/語音模型_讀稿機"
    python_exe = f"{base_path}/xtts_env/Scripts/python.exe"
    script_path = f"{base_path}/tts_enhanced.py"
    
    print("1️⃣ 檢查引擎可用性")
    os.system(f'"{python_exe}" "{script_path}" --info')
    
    print("\n" + "=" * 50)
    print("2️⃣ 測試文字朗讀")
    test_text = "你好，這是增強版讀稿機的功能示範"
    os.system(f'"{python_exe}" "{script_path}" --text "{test_text}" --engine pyttsx3')
    
    print("\n" + "=" * 50)
    print("3️⃣ 測試TXT檔案讀取")
    if os.path.exists("test_script.txt"):
        print("使用測試腳本檔案...")
        os.system(f'"{python_exe}" "{script_path}" --file "test_script.txt" --engine pyttsx3')
    else:
        print("⚠️  test_script.txt 不存在，跳過此測試")
    
    print("\n" + "=" * 50)
    print("4️⃣ 測試MP3錄製功能")
    record_text = "這是MP3錄製測試，檔案將保存到tts_outputs資料夾"
    print("正在錄製MP3...")
    os.system(f'"{python_exe}" "{script_path}" --text "{record_text}" --engine xtts --record --output "demo_recording"')
    
    print("\n" + "=" * 50)
    print("5️⃣ 檢查輸出檔案")
    output_dir = f"{base_path}/tts_outputs"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"✅ 輸出資料夾: {output_dir}")
        print("📁 已生成的檔案:")
        for file in files:
            size = os.path.getsize(os.path.join(output_dir, file))
            print(f"   {file} ({size:,} bytes)")
    else:
        print("⚠️  輸出資料夾不存在")
    
    print("\n" + "=" * 50)
    print("🎯 示範完成！")
    print("\n💡 啟動圖形界面:")
    print(f'   run_enhanced_tts.bat')
    print(f'   或 "{python_exe}" "{script_path}"')

if __name__ == "__main__":
    try:
        demo_enhanced_tts()
    except KeyboardInterrupt:
        print("\n⏹️  示範被中斷")
    except Exception as e:
        print(f"\n❌ 示範出錯: {e}")
