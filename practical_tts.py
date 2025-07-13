#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
實用讀稿機程式 - 混合版本
優先使用 XTTS v2，回退到系統 TTS
"""

import argparse
import os
import sys
import logging

# 嘗試導入各種 TTS 套件
TTS_ENGINES = {
    'pyttsx3': False,
    'win32': False,
    'xtts': False
}

try:
    import pyttsx3
    TTS_ENGINES['pyttsx3'] = True
except ImportError:
    pass

try:
    import win32com.client
    TTS_ENGINES['win32'] = True
except ImportError:
    pass

try:
    from TTS.api import TTS
    import torch
    import pygame
    TTS_ENGINES['xtts'] = True
except ImportError:
    pass


class UniversalTTSReader:
    def __init__(self):
        """初始化通用 TTS 讀稿機"""
        # 設置日誌
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)
        
        self.engine = None
        self.engine_type = None
        
        # 按優先級順序嘗試初始化引擎
        self._init_best_engine()
    
    def _init_best_engine(self):
        """按優先級初始化最佳可用引擎"""
        
        # 優先級 1: XTTS v2 (最高品質)
        if TTS_ENGINES['xtts']:
            try:
                self.logger.info("嘗試初始化 XTTS v2...")
                pygame.mixer.init()
                self.engine = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
                self.engine_type = 'xtts'
                self.logger.info("✓ XTTS v2 初始化成功")
                return
            except Exception as e:
                self.logger.warning(f"XTTS v2 初始化失敗: {e}")
        
        # 優先級 2: pyttsx3 (跨平台)
        if TTS_ENGINES['pyttsx3']:
            try:
                self.logger.info("嘗試初始化 pyttsx3...")
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.9)
                self.engine_type = 'pyttsx3'
                self.logger.info("✓ pyttsx3 初始化成功")
                return
            except Exception as e:
                self.logger.warning(f"pyttsx3 初始化失敗: {e}")
        
        # 優先級 3: Windows SAPI (Windows 內建)
        if TTS_ENGINES['win32']:
            try:
                self.logger.info("嘗試初始化 Windows SAPI...")
                self.engine = win32com.client.Dispatch("SAPI.SpVoice")
                self.engine_type = 'win32'
                self.logger.info("✓ Windows SAPI 初始化成功")
                return
            except Exception as e:
                self.logger.warning(f"Windows SAPI 初始化失敗: {e}")
        
        # 沒有可用引擎
        self.logger.error("❌ 沒有可用的 TTS 引擎")
        self.engine = None
        self.engine_type = None
    
    def speak(self, text, language="zh", save_path=None):
        """
        將文字轉換為語音並播放
        
        Args:
            text (str): 要轉換的文字
            language (str): 語言代碼
            save_path (str): 保存路徑 (僅 XTTS v2 支援)
        """
        if not text.strip():
            self.logger.warning("輸入文字為空")
            return False
        
        if self.engine is None:
            self.logger.error("沒有可用的 TTS 引擎")
            return False
        
        try:
            self.logger.info(f"正在朗讀: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            if self.engine_type == 'xtts':
                return self._speak_xtts(text, language, save_path)
            elif self.engine_type == 'pyttsx3':
                return self._speak_pyttsx3(text)
            elif self.engine_type == 'win32':
                return self._speak_win32(text)
            
        except Exception as e:
            self.logger.error(f"語音合成失敗: {e}")
            return False
    
    def _speak_xtts(self, text, language, save_path):
        """使用 XTTS v2 進行語音合成"""
        try:
            import tempfile
            
            # 確定輸出檔案路徑
            if save_path:
                output_path = save_path
            else:
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                output_path = temp_file.name
                temp_file.close()
            
            # 生成語音
            self.engine.tts_to_file(
                text=text,
                file_path=output_path,
                language=language
            )
            
            # 播放語音
            pygame.mixer.music.load(output_path)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # 清理臨時檔案
            if not save_path:
                try:
                    os.unlink(output_path)
                except OSError:
                    pass
            else:
                self.logger.info(f"音頻已保存到: {save_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"XTTS v2 語音合成失敗: {e}")
            return False
    
    def _speak_pyttsx3(self, text):
        """使用 pyttsx3 進行語音合成"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            self.logger.error(f"pyttsx3 語音合成失敗: {e}")
            return False
    
    def _speak_win32(self, text):
        """使用 Windows SAPI 進行語音合成"""
        try:
            self.engine.Speak(text)
            return True
        except Exception as e:
            self.logger.error(f"Windows SAPI 語音合成失敗: {e}")
            return False
    
    def get_engine_info(self):
        """獲取當前引擎資訊"""
        if self.engine_type == 'xtts':
            return "XTTS v2 (Coqui TTS) - 高品質多語言語音合成"
        elif self.engine_type == 'pyttsx3':
            return "pyttsx3 - 跨平台文字轉語音"
        elif self.engine_type == 'win32':
            return "Windows SAPI - 系統內建語音"
        else:
            return "無可用引擎"


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="實用讀稿機程式 - 智能選擇最佳 TTS 引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python practical_tts.py "你好，歡迎使用讀稿機程式"
  python practical_tts.py "Hello World" --language en
  python practical_tts.py "測試語音" --save output.wav
  python practical_tts.py --info  # 查看當前引擎資訊
        """
    )
    
    parser.add_argument(
        "text",
        nargs='?',
        help="要轉換為語音的文字"
    )
    
    parser.add_argument(
        "--language", "-l",
        default="zh",
        help="語言代碼 (預設: zh)"
    )
    
    parser.add_argument(
        "--save", "-s",
        help="保存語音檔案的路徑 (僅 XTTS v2 支援)"
    )
    
    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="顯示當前 TTS 引擎資訊"
    )
    
    args = parser.parse_args()
    
    try:
        # 初始化讀稿機
        reader = UniversalTTSReader()
        
        # 顯示引擎資訊
        if args.info:
            print(f"當前 TTS 引擎: {reader.get_engine_info()}")
            print(f"可用引擎: {[k for k, v in TTS_ENGINES.items() if v]}")
            return 0
        
        # 檢查是否提供了文字
        if not args.text:
            parser.print_help()
            return 1
        
        # 執行語音合成
        success = reader.speak(
            text=args.text,
            language=args.language,
            save_path=args.save
        )
        
        if success:
            print("✓ 語音合成完成")
            return 0
        else:
            print("❌ 語音合成失敗")
            return 1
            
    except KeyboardInterrupt:
        print("\n程式被用戶中斷")
        return 1
    except Exception as e:
        print(f"錯誤: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
