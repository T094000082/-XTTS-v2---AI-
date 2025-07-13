#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS 引擎比較工具
幫助用戶識別和比較不同 TTS 引擎的聲音特徵
"""

import argparse
import sys
import time

# 嘗試導入各種 TTS 引擎
ENGINES_AVAILABLE = {}

try:
    import pyttsx3
    ENGINES_AVAILABLE['pyttsx3'] = True
except ImportError:
    ENGINES_AVAILABLE['pyttsx3'] = False

try:
    import win32com.client
    ENGINES_AVAILABLE['win32'] = True
except ImportError:
    ENGINES_AVAILABLE['win32'] = False

try:
    from TTS.api import TTS
    import torch
    import pygame
    import tempfile
    import os
    ENGINES_AVAILABLE['xtts'] = True
except ImportError:
    ENGINES_AVAILABLE['xtts'] = False


class TTSComparator:
    def __init__(self):
        """初始化 TTS 比較工具"""
        self.engines = {}
        self._init_all_engines()
    
    def _init_all_engines(self):
        """初始化所有可用的 TTS 引擎"""
        print("🔧 TTS 引擎比較工具")
        print("=" * 60)
        print("正在檢測可用的 TTS 引擎...")
        print()
        
        # 初始化 pyttsx3
        if ENGINES_AVAILABLE['pyttsx3']:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.9)
                self.engines['pyttsx3'] = engine
                print("✅ pyttsx3 (系統內建)")
                print("   📋 特徵: 機械感較強，語調平穩")
                print("   🎯 用途: 一般文字朗讀")
                print()
            except Exception as e:
                print(f"❌ pyttsx3 初始化失敗: {e}")
        
        # 初始化 Windows SAPI
        if ENGINES_AVAILABLE['win32']:
            try:
                engine = win32com.client.Dispatch("SAPI.SpVoice")
                self.engines['win32'] = engine
                print("✅ Windows SAPI (系統內建)")
                print("   📋 特徵: 標準 Windows 語音，發音清晰")
                print("   🎯 用途: Windows 系統語音")
                print()
            except Exception as e:
                print(f"❌ Windows SAPI 初始化失敗: {e}")
        
        # 初始化 XTTS v2
        if ENGINES_AVAILABLE['xtts']:
            try:
                pygame.mixer.init()
                engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
                self.engines['xtts'] = engine
                print("✅ XTTS v2 (AI 語音合成)")
                print("   📋 特徵: 高品質 AI 語音，自然度高")
                print("   🎯 用途: 專業語音合成，支援聲音克隆")
                print()
            except Exception as e:
                print(f"❌ XTTS v2 初始化失敗: {e}")
        
        if not self.engines:
            print("❌ 沒有可用的 TTS 引擎")
        
        print("=" * 60)
    
    def speak_with_engine(self, text, engine_name):
        """使用指定引擎進行語音合成"""
        if engine_name not in self.engines:
            print(f"❌ 引擎 {engine_name} 不可用")
            return False
        
        engine = self.engines[engine_name]
        
        try:
            if engine_name == 'pyttsx3':
                print(f"🔊 pyttsx3 朗讀: {text}")
                engine.say(text)
                engine.runAndWait()
                
            elif engine_name == 'win32':
                print(f"🔊 Windows SAPI 朗讀: {text}")
                engine.Speak(text)
                
            elif engine_name == 'xtts':
                print(f"🔊 XTTS v2 朗讀: {text}")
                # 創建臨時檔案
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                output_path = temp_file.name
                temp_file.close()
                
                # 生成語音
                engine.tts_to_file(text=text, file_path=output_path, language="zh")
                
                # 播放語音
                pygame.mixer.music.load(output_path)
                pygame.mixer.music.play()
                
                # 等待播放完成
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # 清理臨時檔案
                try:
                    os.unlink(output_path)
                except OSError:
                    pass
            
            return True
            
        except Exception as e:
            print(f"❌ {engine_name} 語音合成失敗: {e}")
            return False
    
    def compare_engines(self, text):
        """比較所有可用引擎的聲音效果"""
        print(f"\n🎯 比較文字: '{text}'")
        print("=" * 60)
        
        for engine_name in self.engines.keys():
            print(f"\n--- {engine_name.upper()} ---")
            success = self.speak_with_engine(text, engine_name)
            if success:
                print("✓ 播放完成")
            else:
                print("✗ 播放失敗")
            
            # 等待一下再播放下一個
            if len(self.engines) > 1:
                print("⏳ 等待 2 秒後播放下一個...")
                time.sleep(2)
        
        print("\n" + "=" * 60)
    
    def get_engine_characteristics(self):
        """顯示各引擎的聲音特徵說明"""
        print("\n📊 TTS 引擎聲音特徵對比")
        print("=" * 60)
        
        characteristics = {
            'pyttsx3': {
                '類型': '系統內建語音',
                '自然度': '⭐⭐⭐ (中等)',
                '語調': '較平穩，機械感明顯',
                '語速': '可調整',
                '優點': '穩定、快速、無網路需求',
                '缺點': '聲音較機械化'
            },
            'win32': {
                '類型': 'Windows SAPI',
                '自然度': '⭐⭐⭐ (中等)',
                '語調': '標準 Windows 語音',
                '語速': '固定',
                '優點': '系統原生、兼容性好',
                '缺點': '聲音選擇有限'
            },
            'xtts': {
                '類型': 'AI 神經網路語音',
                '自然度': '⭐⭐⭐⭐⭐ (非常高)',
                '語調': '接近真人，情感豐富',
                '語速': '自然變化',
                '優點': '高品質、支援聲音克隆',
                '缺點': '需要較多計算資源'
            }
        }
        
        for engine, chars in characteristics.items():
            if engine in self.engines:
                print(f"\n🎤 {engine.upper()}")
                for key, value in chars.items():
                    print(f"   {key}: {value}")
        
        print("\n" + "=" * 60)


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="TTS 引擎比較工具 - 識別不同語音合成引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python tts_compare.py "你好世界"                    # 比較所有引擎
  python tts_compare.py "測試" --engine pyttsx3      # 只使用特定引擎
  python tts_compare.py --info                       # 顯示引擎特徵說明
        """
    )
    
    parser.add_argument(
        "text",
        nargs='?',
        default="你好，這是 TTS 引擎比較測試。",
        help="要朗讀的文字 (預設: 測試文字)"
    )
    
    parser.add_argument(
        "--engine", "-e",
        choices=['pyttsx3', 'win32', 'xtts'],
        help="指定特定引擎進行測試"
    )
    
    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="顯示各引擎的聲音特徵說明"
    )
    
    args = parser.parse_args()
    
    try:
        # 初始化比較工具
        comparator = TTSComparator()
        
        # 顯示引擎特徵
        if args.info:
            comparator.get_engine_characteristics()
            return 0
        
        # 使用特定引擎
        if args.engine:
            success = comparator.speak_with_engine(args.text, args.engine)
            return 0 if success else 1
        
        # 比較所有引擎
        if comparator.engines:
            comparator.compare_engines(args.text)
            comparator.get_engine_characteristics()
        else:
            print("❌ 沒有可用的 TTS 引擎")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⏹️  程式被用戶中斷")
        return 130
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
