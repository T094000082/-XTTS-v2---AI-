#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讀稿機程式測試腳本
"""

import os
import sys
import subprocess


def test_simple_tts():
    """測試簡化版 TTS"""
    print("=" * 50)
    print("測試簡化版 TTS")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "simple_tts.py", "這是簡化版讀稿機的測試"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ 簡化版 TTS 測試成功")
        else:
            print(f"✗ 簡化版 TTS 測試失敗: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("✗ 簡化版 TTS 測試超時")
    except Exception as e:
        print(f"✗ 簡化版 TTS 測試錯誤: {e}")


def test_xtts_v2():
    """測試 XTTS v2"""
    print("\n" + "=" * 50)
    print("測試 XTTS v2")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, "tts_reader.py", "這是進階版讀稿機的測試"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ XTTS v2 測試成功")
        else:
            print(f"✗ XTTS v2 測試失敗: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("✗ XTTS v2 測試超時")
    except Exception as e:
        print(f"✗ XTTS v2 測試錯誤: {e}")


def test_save_to_file():
    """測試保存到檔案功能"""
    print("\n" + "=" * 50)
    print("測試保存到檔案功能")
    print("=" * 50)
    
    output_file = "test_output.wav"
    
    try:
        result = subprocess.run([
            sys.executable, "tts_reader.py", 
            "這是保存到檔案的測試", 
            "--save", output_file
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_file):
            print(f"✓ 保存到檔案測試成功: {output_file}")
            file_size = os.path.getsize(output_file)
            print(f"  檔案大小: {file_size} bytes")
        else:
            print(f"✗ 保存到檔案測試失敗: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("✗ 保存到檔案測試超時")
    except Exception as e:
        print(f"✗ 保存到檔案測試錯誤: {e}")
    finally:
        # 清理測試檔案
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
                print(f"  已清理測試檔案: {output_file}")
            except OSError:
                pass


def check_dependencies():
    """檢查相依套件"""
    print("=" * 50)
    print("檢查相依套件")
    print("=" * 50)
    
    packages = [
        "pyttsx3",
        "pygame", 
        "torch",
        "TTS"
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} 已安裝")
        except ImportError:
            print(f"✗ {package} 未安裝")


def main():
    """主函數"""
    print("讀稿機程式測試開始")
    print("注意: 測試過程中會播放語音，請確保音響設備正常")
    
    # 檢查相依套件
    check_dependencies()
    
    # 測試簡化版 TTS
    test_simple_tts()
    
    # 測試 XTTS v2 (如果可用)
    test_xtts_v2()
    
    # 測試保存到檔案功能
    test_save_to_file()
    
    print("\n" + "=" * 50)
    print("測試完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
