#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讀稿機程式 - 使用 XTTS v2
呼叫此程式時系統會唸出帶入的 STRING 文字
"""

import argparse
import os
import tempfile
import logging

# 嘗試導入進階 TTS 套件
try:
    import pygame
    import torch
    from TTS.api import TTS
    ADVANCED_TTS_AVAILABLE = True
except ImportError as e:
    print(f"進階 TTS 套件未安裝: {e}")
    print("回退到簡化版 TTS")
    ADVANCED_TTS_AVAILABLE = False
    
    # 嘗試導入簡化版 TTS
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

class TTSReader:
    def __init__(self, model_name="tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        初始化 TTS 讀稿機
        
        Args:
            model_name (str): XTTS v2 模型名稱
        """
        self.model_name = model_name
        self.tts = None
        self.simple_engine = None
        self.use_advanced = ADVANCED_TTS_AVAILABLE
        
        # 設置日誌
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        if self.use_advanced:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            # 初始化 pygame mixer 用於播放音頻
            pygame.mixer.init()
            self._load_model()
        else:
            self._init_simple_engine()
    
    def _init_simple_engine(self):
        """初始化簡化版 TTS 引擎"""
        if PYTTSX3_AVAILABLE:
            try:
                self.simple_engine = pyttsx3.init()
                self.simple_engine.setProperty('rate', 150)  # 語速
                self.simple_engine.setProperty('volume', 0.9)  # 音量
                self.logger.info("使用 pyttsx3 TTS 引擎")
                return
            except Exception as e:
                self.logger.error(f"pyttsx3 初始化失敗: {e}")
        
        if WIN32_AVAILABLE:
            try:
                self.simple_engine = win32com.client.Dispatch("SAPI.SpVoice")
                self.logger.info("使用 Windows SAPI TTS 引擎")
                return
            except Exception as e:
                self.logger.error(f"Windows SAPI 初始化失敗: {e}")
        
        self.logger.error("沒有可用的 TTS 引擎")
        self.simple_engine = None
    
    def _load_model(self):
        """載入 XTTS v2 模型"""
        try:
            self.logger.info(f"正在載入 XTTS v2 模型: {self.model_name}")
            self.logger.info(f"使用設備: {self.device}")
            
            self.tts = TTS(self.model_name).to(self.device)
            self.logger.info("模型載入完成")
            
        except Exception as e:
            self.logger.error(f"模型載入失敗: {e}")
            raise
    
    def speak(self, text, language="zh", speaker_wav=None, save_path=None):
        """
        將文字轉換為語音並播放
        
        Args:
            text (str): 要轉換的文字
            language (str): 語言代碼 (zh, en, ja, etc.)
            speaker_wav (str): 參考語音檔案路徑 (可選)
            save_path (str): 保存音頻檔案的路徑 (可選)
        """
        if not text.strip():
            self.logger.warning("輸入文字為空")
            return
        
        if self.use_advanced and self.tts:
            self._speak_advanced(text, language, speaker_wav, save_path)
        else:
            self._speak_simple(text)
    
    def _play_audio(self, audio_path):
        """
        播放音頻檔案
        
        Args:
            audio_path (str): 音頻檔案路徑
        """
        try:
            self.logger.info("正在播放語音...")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
            self.logger.info("播放完成")
            
        except Exception as e:
            self.logger.error(f"音頻播放失敗: {e}")
            raise
    
    def save_to_file(self, text, output_path, language="zh", speaker_wav=None):
        """
        將文字轉換為語音並保存到檔案
        
        Args:
            text (str): 要轉換的文字
            output_path (str): 輸出檔案路徑
            language (str): 語言代碼
            speaker_wav (str): 參考語音檔案路徑 (可選)
        """
        if self.use_advanced and self.tts:
            self._speak_advanced(text, language, speaker_wav, output_path)
            self.logger.info(f"語音檔案已保存到: {output_path}")
        else:
            self.logger.warning("簡化版 TTS 不支援保存到檔案功能")
            # 仍然可以播放
            self._speak_simple(text)
    
    def _speak_advanced(self, text, language, speaker_wav, save_path):
        """使用進階 TTS 進行語音合成"""
        try:
            # 如果沒有指定保存路徑，使用臨時檔案
            if save_path is None:
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                output_path = temp_file.name
                temp_file.close()
            else:
                output_path = save_path
            
            self.logger.info(f"正在生成語音: {text[:50]}...")
            
            # 生成語音
            if speaker_wav and os.path.exists(speaker_wav):
                # 使用參考語音進行聲音克隆
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=speaker_wav,
                    language=language
                )
            else:
                # 使用預設語音
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language
                )
            
            self.logger.info(f"語音檔案已生成: {output_path}")
            
            # 播放音頻
            self._play_audio(output_path)
            
            # 如果是臨時檔案，播放完後刪除
            if save_path is None:
                try:
                    os.unlink(output_path)
                except OSError:
                    pass  # 忽略刪除錯誤
                    
        except Exception as e:
            self.logger.error(f"進階語音生成失敗: {e}")
            # 回退到簡化版
            self.logger.info("回退到簡化版 TTS")
            self._speak_simple(text)
    
    def _speak_simple(self, text):
        """使用簡化版 TTS 進行語音合成"""
        if self.simple_engine is None:
            self.logger.error("沒有可用的 TTS 引擎")
            return
        
        try:
            self.logger.info(f"正在朗讀: {text}")
            
            if PYTTSX3_AVAILABLE and hasattr(self.simple_engine, 'say'):
                # 使用 pyttsx3
                self.simple_engine.say(text)
                self.simple_engine.runAndWait()
            elif WIN32_AVAILABLE and hasattr(self.simple_engine, 'Speak'):
                # 使用 Windows SAPI
                self.simple_engine.Speak(text)
            else:
                self.logger.error("TTS 引擎不支持語音合成")
                
        except Exception as e:
            self.logger.error(f"簡化版語音生成失敗: {e}")


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="讀稿機程式 - 使用 XTTS v2 將文字轉換為語音",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python tts_reader.py "你好，歡迎使用讀稿機程式"
  python tts_reader.py "Hello World" --language en
  python tts_reader.py "こんにちは" --language ja
  python tts_reader.py "測試語音" --save output.wav
  python tts_reader.py "克隆語音測試" --speaker reference.wav
        """
    )
    
    parser.add_argument(
        "text",
        help="要轉換為語音的文字"
    )
    
    parser.add_argument(
        "--language", "-l",
        default="zh",
        help="語言代碼 (預設: zh)"
    )
    
    parser.add_argument(
        "--speaker", "-s",
        help="參考語音檔案路徑 (用於聲音克隆)"
    )
    
    parser.add_argument(
        "--save", "-o",
        help="保存語音檔案的路徑"
    )
    
    parser.add_argument(
        "--model",
        default="tts_models/multilingual/multi-dataset/xtts_v2",
        help="TTS 模型名稱 (預設: XTTS v2)"
    )
    
    args = parser.parse_args()
    
    try:
        # 初始化讀稿機
        reader = TTSReader(model_name=args.model)
        
        # 轉換並播放/保存語音
        if args.save:
            reader.save_to_file(
                text=args.text,
                output_path=args.save,
                language=args.language,
                speaker_wav=args.speaker
            )
        else:
            reader.speak(
                text=args.text,
                language=args.language,
                speaker_wav=args.speaker
            )
            
    except KeyboardInterrupt:
        print("\n程式被用戶中斷")
    except Exception as e:
        print(f"錯誤: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
