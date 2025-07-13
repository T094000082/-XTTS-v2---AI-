#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版 TTS 讀稿機 - 確保可用
結合系統 TTS 和 XTTS v2，提供可靠的語音合成
"""

import sys
import os
import tempfile
import argparse

def try_system_tts(text):
    """嘗試使用系統 TTS"""
    try:
        import pyttsx3
        
        print("🔊 使用系統 TTS (pyttsx3)...")
        engine = pyttsx3.init()
        
        # 設置中文語音（如果可用）
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # 調整語速
        engine.setProperty('rate', 150)
        
        engine.say(text)
        engine.runAndWait()
        
        print("✅ 系統 TTS 播放完成")
        return True
        
    except Exception as e:
        print(f"❌ 系統 TTS 失敗: {e}")
        return False

def try_windows_sapi(text):
    """嘗試使用 Windows SAPI"""
    try:
        import win32com.client
        
        print("🔊 使用 Windows SAPI...")
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        
        # 嘗試設置中文語音
        voices = speaker.GetVoices()
        for i, voice in enumerate(voices):
            if 'chinese' in voice.GetDescription().lower():
                speaker.Voice = voice
                break
        
        speaker.Speak(text)
        print("✅ Windows SAPI 播放完成")
        return True
        
    except Exception as e:
        print(f"❌ Windows SAPI 失敗: {e}")
        return False

def try_xtts_simple(text):
    """嘗試使用 XTTS v2 (簡化版)"""
    try:
        os.environ["COQUI_TOS_AGREED"] = "1"
        
        print("🔊 嘗試 XTTS v2 (簡化版)...")
        from TTS.api import TTS
        
        # 使用更簡單的模型
        models_to_try = [
            "tts_models/zh-CN/baker/tacotron2-DDC-GST",  # 中文模型
            "tts_models/en/ljspeech/tacotron2-DDC",      # 英文模型
            "tts_models/multilingual/multi-dataset/xtts_v2"  # XTTS v2
        ]
        
        for model_name in models_to_try:
            try:
                print(f"   嘗試模型: {model_name}")
                tts = TTS(model_name)
                
                # 創建臨時文件
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    output_path = tmp.name
                
                # 嘗試合成
                if "xtts" in model_name.lower():
                    # XTTS v2 需要說話者參數
                    try:
                        wav = tts.tts(text, speaker_idx=0)
                    except:
                        wav = tts.tts(text)
                else:
                    # 其他模型直接合成
                    wav = tts.tts(text)
                
                # 保存音頻
                import soundfile as sf
                sf.write(output_path, wav, 22050)
                
                # 播放音頻
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(output_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                print(f"✅ {model_name} 播放完成")
                
                # 清理
                try:
                    os.unlink(output_path)
                except:
                    pass
                
                return True
                
            except Exception as e:
                print(f"   模型 {model_name} 失敗: {e}")
                continue
        
        print("❌ 所有 TTS 模型都失敗")
        return False
        
    except Exception as e:
        print(f"❌ XTTS 初始化失敗: {e}")
        return False

def smart_tts(text):
    """智能 TTS - 嘗試多種方法"""
    print(f"🎯 智能 TTS 開始合成: {text}")
    print("=" * 50)
    
    # 方法優先級
    methods = [
        ("XTTS v2", try_xtts_simple),
        ("系統 TTS", try_system_tts),
        ("Windows SAPI", try_windows_sapi)
    ]
    
    for method_name, method_func in methods:
        print(f"\n🔄 嘗試 {method_name}...")
        try:
            if method_func(text):
                print(f"🎉 {method_name} 成功！")
                return True
        except Exception as e:
            print(f"❌ {method_name} 異常: {e}")
    
    print("\n❌ 所有 TTS 方法都失敗")
    print("💡 建議:")
    print("1. 檢查音響設備")
    print("2. 重新安裝依賴")
    print("3. 使用 fix_xtts.bat 修復")
    return False

def main():
    """主程序"""
    parser = argparse.ArgumentParser(description="智能 TTS 讀稿機")
    parser.add_argument("text", nargs="?", default="你好，這是智能 TTS 測試", 
                       help="要合成的文字")
    parser.add_argument("--method", choices=["auto", "xtts", "system", "sapi"], 
                       default="auto", help="指定 TTS 方法")
    
    args = parser.parse_args()
    
    print("🚀 智能 TTS 讀稿機")
    print("=" * 50)
    
    if args.method == "auto":
        success = smart_tts(args.text)
    elif args.method == "xtts":
        success = try_xtts_simple(args.text)
    elif args.method == "system":
        success = try_system_tts(args.text)
    elif args.method == "sapi":
        success = try_windows_sapi(args.text)
    
    print("=" * 50)
    if success:
        print("🎯 TTS 合成成功！")
    else:
        print("❌ TTS 合成失敗")
        print("請嘗試運行 fix_xtts.bat 修復問題")

if __name__ == "__main__":
    main()
