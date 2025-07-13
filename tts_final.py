#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讀稿機程式 - 最終穩定版
呼叫此程式時系統會唸出帶入的 STRING 文字
使用系統內建 TTS，無複雜依賴
"""

import argparse
import sys
import os

# 嘗試導入可用的 TTS 引擎
ENGINES = {}

try:
    import pyttsx3
    ENGINES['pyttsx3'] = True
except ImportError:
    ENGINES['pyttsx3'] = False

try:
    import win32com.client
    ENGINES['win32'] = True
except ImportError:
    ENGINES['win32'] = False


class TTSReader:
    def __init__(self):
        """初始化 TTS 讀稿機"""
        self.engine = None
        self.engine_type = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化最佳可用的 TTS 引擎"""
        
        # 優先使用 pyttsx3 (跨平台，品質較好)
        if ENGINES['pyttsx3']:
            try:
                print("正在初始化 pyttsx3 TTS 引擎...")
                self.engine = pyttsx3.init()
                
                # 設置語音參數
                self.engine.setProperty('rate', 150)    # 語速
                self.engine.setProperty('volume', 0.9)  # 音量
                
                # 嘗試設置中文語音 (如果可用)
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                
                self.engine_type = 'pyttsx3'
                print("✓ pyttsx3 TTS 引擎初始化成功")
                return
                
            except Exception as e:
                print(f"pyttsx3 初始化失敗: {e}")
        
        # 備用：Windows SAPI
        if ENGINES['win32']:
            try:
                print("正在初始化 Windows SAPI TTS 引擎...")
                self.engine = win32com.client.Dispatch("SAPI.SpVoice")
                self.engine_type = 'win32'
                print("✓ Windows SAPI TTS 引擎初始化成功")
                return
                
            except Exception as e:
                print(f"Windows SAPI 初始化失敗: {e}")
        
        # 沒有可用引擎
        print("❌ 錯誤: 沒有可用的 TTS 引擎")
        print("請安裝 pyttsx3: pip install pyttsx3")
        self.engine = None
        self.engine_type = None
    
    def speak(self, text):
        """
        將文字轉換為語音並播放
        
        Args:
            text (str): 要轉換的文字
            
        Returns:
            bool: 成功返回 True，失敗返回 False
        """
        if not text or not text.strip():
            print("⚠️  警告: 輸入文字為空")
            return False
        
        if self.engine is None:
            print("❌ 錯誤: 沒有可用的 TTS 引擎")
            return False
        
        try:
            print(f"🔊 正在朗讀: {text}")
            
            if self.engine_type == 'pyttsx3':
                self.engine.say(text)
                self.engine.runAndWait()
            elif self.engine_type == 'win32':
                self.engine.Speak(text)
            
            print("✓ 朗讀完成")
            return True
            
        except Exception as e:
            print(f"❌ 語音合成失敗: {e}")
            return False
    
    def get_engine_info(self):
        """獲取當前引擎資訊"""
        if self.engine_type == 'pyttsx3':
            return "pyttsx3 - 跨平台文字轉語音引擎"
        elif self.engine_type == 'win32':
            return "Windows SAPI - 系統內建語音合成"
        else:
            return "無可用引擎"
    
    def list_voices(self):
        """列出可用的語音"""
        if self.engine_type == 'pyttsx3' and self.engine:
            try:
                voices = self.engine.getProperty('voices')
                print("可用語音:")
                for i, voice in enumerate(voices):
                    print(f"  {i}: {voice.name} ({voice.id})")
            except Exception as e:
                print(f"無法列出語音: {e}")
        else:
            print("當前引擎不支援語音列表功能")


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="讀稿機程式 - 將文字轉換為語音",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python tts_final.py "你好，歡迎使用讀稿機程式"
  python tts_final.py "Hello World"
  python tts_final.py --info        # 查看引擎資訊
  python tts_final.py --voices      # 列出可用語音
  
支援的語言:
  - 中文 (繁體/簡體)
  - 英文
  - 其他系統支援的語言
        """
    )
    
    parser.add_argument(
        "text",
        nargs='?',
        help="要轉換為語音的文字"
    )
    
    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="顯示 TTS 引擎資訊"
    )
    
    parser.add_argument(
        "--voices", "-v",
        action="store_true",
        help="列出可用的語音"
    )
    
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="執行測試"
    )
    
    args = parser.parse_args()
    
    try:
        print("📢 讀稿機程式 v1.0")
        print("=" * 40)
        
        # 初始化讀稿機
        reader = TTSReader()
        
        # 顯示引擎資訊
        if args.info:
            print(f"當前 TTS 引擎: {reader.get_engine_info()}")
            print(f"可用引擎: {[k for k, v in ENGINES.items() if v]}")
            return 0
        
        # 列出語音
        if args.voices:
            reader.list_voices()
            return 0
        
        # 執行測試
        if args.test:
            test_texts = [
                "你好，這是讀稿機程式的測試。",
                "Hello, this is a test of the TTS reader.",
                "1234567890",
                "歡迎使用文字轉語音功能！"
            ]
            
            for i, test_text in enumerate(test_texts, 1):
                print(f"\n測試 {i}/{len(test_texts)}:")
                if not reader.speak(test_text):
                    print("測試失敗")
                    return 1
            
            print("\n✅ 所有測試完成")
            return 0
        
        # 檢查是否提供了文字
        if not args.text:
            parser.print_help()
            return 1
        
        # 執行語音合成
        success = reader.speak(args.text)
        
        if success:
            return 0
        else:
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️  程式被用戶中斷")
        return 130
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
