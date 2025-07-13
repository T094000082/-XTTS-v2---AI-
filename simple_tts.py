#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版讀稿機程式 - 使用系統內建的 TTS
使用 pyttsx3 或 Windows SAPI，不包含 XTTS v2
"""

import argparse
import sys

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import win32com.client
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class SimpleTTSReader:
    def __init__(self):
        """初始化簡化版 TTS 讀稿機"""
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化 TTS 引擎"""
        print("=" * 50)
        print("正在初始化 TTS 引擎...")
        
        if PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)  # 語速
                self.engine.setProperty('volume', 0.9)  # 音量
                
                # 獲取引擎詳細資訊
                engine_name = self.engine.getProperty('voice')
                voices = self.engine.getProperty('voices')
                
                print("✓ 使用 pyttsx3 TTS 引擎")
                print("  類型: 系統內建語音合成")
                print("  特徵: 機械感較強的合成語音")
                
                if voices:
                    current_voice = None
                    for voice in voices:
                        if voice.id == engine_name:
                            current_voice = voice
                            break
                    
                    if current_voice:
                        print(f"  當前語音: {current_voice.name}")
                        print(f"  語言: {current_voice.languages}")
                
                print("=" * 50)
                return
            except Exception as e:
                print(f"pyttsx3 初始化失敗: {e}")
        
        if WIN32_AVAILABLE:
            try:
                self.engine = win32com.client.Dispatch("SAPI.SpVoice")
                print("✓ 使用 Windows SAPI TTS 引擎")
                print("  類型: Windows 系統內建語音")
                print("  特徵: 標準 Windows 語音，機械感明顯")
                print("=" * 50)
                return
            except Exception as e:
                print(f"Windows SAPI 初始化失敗: {e}")
        
        print("❌ 警告: 沒有可用的 TTS 引擎")
        print("=" * 50)
        self.engine = None
    
    def speak(self, text):
        """
        將文字轉換為語音並播放
        
        Args:
            text (str): 要轉換的文字
        """
        if not text.strip():
            print("輸入文字為空")
            return
        
        if self.engine is None:
            print("錯誤: 沒有可用的 TTS 引擎")
            return
        
        try:
            print(f"正在朗讀: {text}")
            
            if PYTTSX3_AVAILABLE and hasattr(self.engine, 'say'):
                # 使用 pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()
            elif WIN32_AVAILABLE and hasattr(self.engine, 'Speak'):
                # 使用 Windows SAPI
                self.engine.Speak(text)
            else:
                print("錯誤: TTS 引擎不支持語音合成")
                
        except Exception as e:
            print(f"語音生成失敗: {e}")


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="簡化版讀稿機程式 - 使用系統內建 TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python simple_tts.py "你好，歡迎使用讀稿機程式"
  python simple_tts.py "Hello World"
        """
    )
    
    parser.add_argument(
        "text",
        help="要轉換為語音的文字"
    )
    
    args = parser.parse_args()
    
    try:
        # 初始化讀稿機
        reader = SimpleTTSReader()
        
        # 轉換並播放語音
        reader.speak(args.text)
            
    except KeyboardInterrupt:
        print("\n程式被用戶中斷")
    except Exception as e:
        print(f"錯誤: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
