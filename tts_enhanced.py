#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讀稿機程式 - 增強版
新功能：
1. 選擇TXT檔念稿
2. 選擇是否在念稿時錄製mp3
3. 支援多種語音引擎 (pyttsx3, SAPI, XTTS v2)
"""

import argparse
import sys
import os
import tempfile
import subprocess
from pathlib import Path
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 設置XTTS v2環境變量
os.environ["COQUI_TOS_AGREED"] = "1"

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

try:
    from TTS.api import TTS
    import torch
    import pygame
    ENGINES['xtts'] = True
except ImportError:
    ENGINES['xtts'] = False

# MP3錄製相關
try:
    import subprocess
    # 檢查是否有 ffmpeg (用於錄製mp3)
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    FFMPEG_AVAILABLE = True
except (FileNotFoundError, subprocess.CalledProcessError):
    FFMPEG_AVAILABLE = False

# XTTS v2 模型緩存（全局變量，避免重複載入）
_XTTS_MODEL_CACHE = None

class EnhancedTTSReader:
    def __init__(self):
        """初始化增強版TTS讀稿機"""
        self.engine = None
        self.engine_type = None
        self.xtts_model = None
        self.recording = False
        self.output_folder = "tts_outputs"
        self._ensure_output_folder()
        
    def _ensure_output_folder(self):
        """確保輸出資料夾存在"""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"✅ 創建輸出資料夾: {self.output_folder}")
    
    def init_engine(self, engine_type="auto"):
        """初始化指定的TTS引擎"""
        if engine_type == "auto":
            # 自動選擇最佳引擎：XTTS v2 > pyttsx3 > SAPI
            if ENGINES['xtts']:
                engine_type = "xtts"
            elif ENGINES['pyttsx3']:
                engine_type = "pyttsx3"
            elif ENGINES['win32']:
                engine_type = "win32"
            else:
                raise Exception("沒有可用的TTS引擎")
        
        if engine_type == "xtts" and ENGINES['xtts']:
            self._init_xtts()
        elif engine_type == "pyttsx3" and ENGINES['pyttsx3']:
            self._init_pyttsx3()
        elif engine_type == "win32" and ENGINES['win32']:
            self._init_win32()
        else:
            raise Exception(f"引擎 {engine_type} 不可用")
        
        print(f"✅ TTS引擎初始化完成: {self.get_engine_info()}")
    
    def _init_pyttsx3(self):
        """初始化pyttsx3引擎"""
        print("🔧 正在初始化 pyttsx3 引擎...")
        self.engine = pyttsx3.init()
        self.engine_type = 'pyttsx3'
        
        # 設置語音參數
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # 嘗試設置中文語音
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def _init_win32(self):
        """初始化Windows SAPI引擎"""
        print("🔧 正在初始化 Windows SAPI 引擎...")
        self.engine = win32com.client.Dispatch("SAPI.SpVoice")
        self.engine_type = 'win32'
    
    def _init_xtts(self):
        """初始化XTTS v2引擎"""
        global _XTTS_MODEL_CACHE
        
        print("🔧 正在初始化 XTTS v2 引擎...")
        
        # 如果已經有緩存的模型，直接使用
        if _XTTS_MODEL_CACHE is not None:
            print("   ⚡ 使用已載入的模型緩存，瞬間完成！")
            self.xtts_model = _XTTS_MODEL_CACHE
            self.engine_type = 'xtts'
            return
        
        # 檢查模型是否已經下載到本地
        import os
        from pathlib import Path
        
        # 獲取用戶目錄下的模型緩存路徑
        home_dir = Path.home()
        cache_dir = home_dir / ".cache" / "tts"
        model_path = cache_dir / "tts_models--multilingual--multi-dataset--xtts_v2"
        
        if model_path.exists():
            print("   ✅ 發現本地緩存模型，快速載入中...")
        else:
            print("   📥 首次使用，正在下載模型（約1.8GB），請稍候...")
            print("   💡 模型將緩存到本地，之後使用會更快！")
        
        # 初始化pygame用於播放
        import pygame
        pygame.mixer.init()
        
        # 創建XTTS模型（會自動使用緩存）
        self.xtts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
        
        # 將模型保存到全局緩存
        _XTTS_MODEL_CACHE = self.xtts_model
        
        self.engine_type = 'xtts'
        print("   ✅ XTTS v2 引擎載入完成！模型已緩存，下次使用更快！")
    
    def read_txt_file(self, file_path):
        """讀取TXT文件內容"""
        try:
            # 嘗試不同編碼
            encodings = ['utf-8', 'utf-8-sig', 'gb2312', 'gbk', 'big5']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read().strip()
                        print(f"✅ 成功讀取文件 ({encoding}): {len(content)} 字符")
                        return content
                except UnicodeDecodeError:
                    continue
            
            raise Exception("無法讀取文件，嘗試所有編碼都失敗")
            
        except Exception as e:
            print(f"❌ 讀取文件失敗: {e}")
            return None
    
    def speak_text(self, text, record_mp3=False, output_filename=None):
        """朗讀文字，可選擇錄製為MP3"""
        try:
            if not text or not text.strip():
                print("❌ 文字內容為空")
                return False
                
            print(f"🔊 正在朗讀: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            if record_mp3:
                return self._speak_and_record(text, output_filename)
            else:
                return self._speak_only(text)
                
        except Exception as e:
            print(f"❌ 語音合成失敗: {e}")
            return False
    
    def _speak_only(self, text):
        """只朗讀，不錄製"""
        try:
            if self.engine_type == 'pyttsx3':
                self.engine.say(text)
                self.engine.runAndWait()
                
            elif self.engine_type == 'win32':
                self.engine.Speak(text)
                
            elif self.engine_type == 'xtts':
                # 使用XTTS v2朗讀
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    output_path = temp_file.name
                
                self.xtts_model.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language="zh",
                    speaker="Claribel Dervla"  # 使用預設說話者
                )
                
                # 播放音頻
                import pygame
                pygame.mixer.music.load(output_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # 清理臨時文件
                try:
                    os.unlink(output_path)
                except:
                    pass
            
            print("✅ 朗讀完成")
            return True
            
        except Exception as e:
            print(f"❌ 朗讀失敗: {e}")
            return False
    
    def _speak_and_record(self, text, output_filename=None):
        """朗讀並錄製為MP3"""
        try:
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"tts_recording_{timestamp}"
            
            # 移除文件擴展名（如果有）
            if output_filename.endswith('.mp3'):
                output_filename = output_filename[:-4]
                
            wav_path = os.path.join(self.output_folder, f"{output_filename}.wav")
            mp3_path = os.path.join(self.output_folder, f"{output_filename}.mp3")
            
            if self.engine_type == 'xtts':
                # XTTS v2 直接生成WAV文件
                self.xtts_model.tts_to_file(
                    text=text,
                    file_path=wav_path,
                    language="zh",
                    speaker="Claribel Dervla"
                )
                
                # 播放音頻
                import pygame
                pygame.mixer.music.load(wav_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                    
            else:
                # 對於其他引擎，需要錄製系統音頻
                print("⚠️  非XTTS引擎的錄製功能需要額外設定")
                # 先正常播放
                if self.engine_type == 'pyttsx3':
                    # 使用pyttsx3保存到文件
                    self.engine.save_to_file(text, wav_path)
                    self.engine.runAndWait()
                elif self.engine_type == 'win32':
                    self.engine.Speak(text)
            
            # 轉換為MP3（如果有ffmpeg）
            if FFMPEG_AVAILABLE and os.path.exists(wav_path):
                print(f"🔄 正在轉換為MP3格式...")
                try:
                    result = subprocess.run([
                        'ffmpeg', '-i', wav_path, '-acodec', 'mp3', 
                        '-ab', '192k', mp3_path, '-y'
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"✅ MP3文件已保存: {mp3_path}")
                        # 刪除臨時WAV文件
                        try:
                            os.remove(wav_path)
                        except:
                            pass
                    else:
                        print(f"⚠️  MP3轉換失敗，保留WAV文件: {wav_path}")
                        
                except Exception as e:
                    print(f"⚠️  MP3轉換出錯: {e}")
            
            elif os.path.exists(wav_path):
                print(f"✅ 音頻文件已保存: {wav_path}")
                print("💡 提示: 安裝 ffmpeg 可支援MP3格式")
            
            print("✅ 朗讀和錄製完成")
            return True
            
        except Exception as e:
            print(f"❌ 錄製失敗: {e}")
            return False
    
    def get_engine_info(self):
        """獲取當前引擎資訊"""
        global _XTTS_MODEL_CACHE
        
        if self.engine_type == 'pyttsx3':
            return "pyttsx3 - 跨平台文字轉語音引擎"
        elif self.engine_type == 'win32':
            return "Windows SAPI - 系統內建語音合成"
        elif self.engine_type == 'xtts':
            cache_status = "（已緩存）" if _XTTS_MODEL_CACHE is not None else "（首次載入）"
            return f"XTTS v2 - 高品質AI語音合成 {cache_status}"
        else:
            return "無引擎"
    
    def get_model_cache_info(self):
        """獲取模型緩存資訊"""
        global _XTTS_MODEL_CACHE
        from pathlib import Path
        
        info = {
            'memory_cached': _XTTS_MODEL_CACHE is not None,
            'disk_cached': False,
            'cache_path': None
        }
        
        # 檢查磁盤緩存
        home_dir = Path.home()
        cache_dir = home_dir / ".cache" / "tts"
        model_path = cache_dir / "tts_models--multilingual--multi-dataset--xtts_v2"
        
        if model_path.exists():
            info['disk_cached'] = True
            info['cache_path'] = str(model_path)
        
        return info

class TTSGui:
    def __init__(self):
        """初始化圖形界面"""
        self.root = tk.Tk()
        self.root.title("增強版讀稿機 - TXT檔念稿與MP3錄製")
        self.root.geometry("800x600")
        
        self.reader = EnhancedTTSReader()
        self.current_file_path = None
        self.current_text = ""
        
        self.setup_gui()
        
    def setup_gui(self):
        """設置圖形界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件選擇區域
        file_frame = ttk.LabelFrame(main_frame, text="文件選擇", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(file_frame, text="選擇TXT檔案", command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="未選擇檔案")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # 引擎選擇
        engine_frame = ttk.LabelFrame(main_frame, text="語音引擎", padding="10")
        engine_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.engine_var = tk.StringVar(value="auto")
        engines = [
            ("自動選擇", "auto"),
            ("XTTS v2 (高品質)", "xtts"),
            ("pyttsx3 (穩定)", "pyttsx3"),
            ("Windows SAPI (輕量)", "win32")
        ]
        
        for i, (text, value) in enumerate(engines):
            ttk.Radiobutton(engine_frame, text=text, variable=self.engine_var, 
                           value=value).grid(row=0, column=i, padx=5)
        
        # 錄製選項
        record_frame = ttk.LabelFrame(main_frame, text="錄製選項", padding="10")
        record_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.record_var = tk.BooleanVar()
        ttk.Checkbutton(record_frame, text="同時錄製為MP3檔案", 
                       variable=self.record_var).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(record_frame, text="輸出檔名:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.filename_entry = ttk.Entry(record_frame, width=50)
        self.filename_entry.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky=(tk.W, tk.E))
        
        # 文本預覽區域
        text_frame = ttk.LabelFrame(main_frame, text="文本內容預覽", padding="10")
        text_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.text_display = tk.Text(text_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_display.yview)
        self.text_display.configure(yscrollcommand=scrollbar.set)
        
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 控制按鈕
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(control_frame, text="初始化引擎", command=self.init_engine).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="開始朗讀", command=self.start_reading).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="測試引擎", command=self.test_engine).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="緩存狀態", command=self.show_cache_status).grid(row=0, column=3, padx=5)
        
        # 狀態欄
        self.status_label = ttk.Label(main_frame, text="就緒 - 請選擇TXT檔案", foreground="blue")
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 配置權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        file_frame.columnconfigure(1, weight=1)
        record_frame.columnconfigure(1, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
    
    def select_file(self):
        """選擇TXT檔案"""
        file_path = filedialog.askopenfilename(
            title="選擇TXT檔案",
            filetypes=[("文字檔案", "*.txt"), ("所有檔案", "*.*")]
        )
        
        if file_path:
            self.current_file_path = file_path
            self.file_label.config(text=f"已選擇: {os.path.basename(file_path)}")
            
            # 讀取並顯示文件內容
            content = self.reader.read_txt_file(file_path)
            if content:
                self.current_text = content
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(1.0, content)
                self.status_label.config(text=f"已載入檔案: {len(content)} 字符", foreground="green")
                
                # 自動設定檔名
                if not self.filename_entry.get():
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    self.filename_entry.delete(0, tk.END)
                    self.filename_entry.insert(0, f"{base_name}_{timestamp}")
            else:
                self.status_label.config(text="檔案讀取失敗", foreground="red")
    
    def init_engine(self):
        """初始化語音引擎"""
        try:
            self.status_label.config(text="正在初始化引擎...", foreground="orange")
            self.root.update()
            
            self.reader.init_engine(self.engine_var.get())
            self.status_label.config(text=f"引擎初始化完成: {self.reader.get_engine_info()}", foreground="green")
            
        except Exception as e:
            self.status_label.config(text=f"引擎初始化失敗: {str(e)}", foreground="red")
            messagebox.showerror("錯誤", f"引擎初始化失敗:\n{str(e)}")
    
    def start_reading(self):
        """開始朗讀"""
        if not self.current_text:
            messagebox.showwarning("警告", "請先選擇並載入TXT檔案")
            return
            
        if not self.reader.engine_type:
            messagebox.showwarning("警告", "請先初始化語音引擎")
            return
        
        try:
            self.status_label.config(text="正在朗讀...", foreground="blue")
            self.root.update()
            
            # 獲取錄製設定
            record_mp3 = self.record_var.get()
            output_filename = self.filename_entry.get() if record_mp3 else None
            
            # 開始朗讀
            success = self.reader.speak_text(
                self.current_text,
                record_mp3=record_mp3,
                output_filename=output_filename
            )
            
            if success:
                if record_mp3:
                    self.status_label.config(text="朗讀和錄製完成", foreground="green")
                else:
                    self.status_label.config(text="朗讀完成", foreground="green")
            else:
                self.status_label.config(text="朗讀失敗", foreground="red")
                
        except Exception as e:
            self.status_label.config(text=f"朗讀出錯: {str(e)}", foreground="red")
            messagebox.showerror("錯誤", f"朗讀過程出錯:\n{str(e)}")
    
    def test_engine(self):
        """測試當前引擎"""
        if not self.reader.engine_type:
            messagebox.showwarning("警告", "請先初始化語音引擎")
            return
        
        test_text = "你好，這是語音引擎測試。Hello, this is a voice engine test."
        
        try:
            self.status_label.config(text="正在測試引擎...", foreground="blue")
            self.root.update()
            
            success = self.reader.speak_text(test_text)
            
            if success:
                self.status_label.config(text="引擎測試成功", foreground="green")
            else:
                self.status_label.config(text="引擎測試失敗", foreground="red")
                
        except Exception as e:
            self.status_label.config(text=f"測試出錯: {str(e)}", foreground="red")
    
    def show_cache_status(self):
        """顯示模型緩存狀態"""
        cache_info = self.reader.get_model_cache_info()
        
        status_text = "📋 XTTS v2 模型緩存狀態:\n\n"
        
        if cache_info['memory_cached']:
            status_text += "🟢 記憶體緩存: 已載入（下次初始化會很快）\n"
        else:
            status_text += "🔴 記憶體緩存: 未載入\n"
            
        if cache_info['disk_cached']:
            status_text += "🟢 磁盤緩存: 已下載（無需重新下載）\n"
            status_text += f"📁 緩存路徑: {cache_info['cache_path']}\n"
        else:
            status_text += "🔴 磁盤緩存: 未下載（首次使用需下載約1.8GB）\n"
        
        status_text += "\n💡 提示:\n"
        status_text += "• 首次使用會下載模型到磁盤緩存\n"
        status_text += "• 之後每次程式啟動只需載入到記憶體\n"
        status_text += "• 同一程式執行期間，多次初始化會使用記憶體緩存"
        
        messagebox.showinfo("模型緩存狀態", status_text)
    
    def run(self):
        """運行GUI"""
        self.root.mainloop()

def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="增強版讀稿機 - 支援TXT檔案念稿和MP3錄製",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用方式:
  python tts_enhanced.py                    # 啟動圖形界面
  python tts_enhanced.py --gui              # 啟動圖形界面
  python tts_enhanced.py --file input.txt  # 命令行模式讀取檔案
  python tts_enhanced.py --text "文字"      # 命令行模式讀取文字
  
新功能:
  1. 圖形界面選擇TXT檔案念稿
  2. 可選擇錄製為MP3檔案
  3. 支援多種語音引擎 (XTTS v2, pyttsx3, SAPI)
  4. 自動檔名產生和管理
        """
    )
    
    parser.add_argument("--gui", "-g", action="store_true", help="啟動圖形界面 (預設)")
    parser.add_argument("--file", "-f", help="指定TXT檔案路徑")
    parser.add_argument("--text", "-t", help="直接指定要朗讀的文字")
    parser.add_argument("--engine", "-e", choices=["auto", "xtts", "pyttsx3", "win32"], 
                       default="auto", help="指定語音引擎")
    parser.add_argument("--record", "-r", action="store_true", help="錄製為MP3")
    parser.add_argument("--output", "-o", help="輸出檔名 (不含副檔名)")
    parser.add_argument("--info", "-i", action="store_true", help="顯示引擎資訊")
    
    args = parser.parse_args()
    
    # 顯示引擎資訊
    if args.info:
        print("🔍 可用的TTS引擎:")
        for engine, available in ENGINES.items():
            status = "✅ 可用" if available else "❌ 不可用"
            print(f"  {engine}: {status}")
        print(f"📁 FFmpeg (MP3支援): {'✅ 可用' if FFMPEG_AVAILABLE else '❌ 不可用'}")
        
        # 顯示XTTS v2緩存狀態
        if ENGINES.get('xtts', False):
            print("\n📋 XTTS v2 模型緩存狀態:")
            reader = EnhancedTTSReader()
            cache_info = reader.get_model_cache_info()
            
            memory_status = "✅ 已載入" if cache_info['memory_cached'] else "❌ 未載入"
            disk_status = "✅ 已下載" if cache_info['disk_cached'] else "❌ 未下載"
            
            print(f"  記憶體緩存: {memory_status}")
            print(f"  磁盤緩存: {disk_status}")
            
            if cache_info['disk_cached']:
                print(f"  緩存路徑: {cache_info['cache_path']}")
            else:
                print("  💡 首次使用XTTS v2會下載約1.8GB模型")
        
        return 0
    
    # 命令行模式
    if args.file or args.text:
        try:
            reader = EnhancedTTSReader()
            reader.init_engine(args.engine)
            
            if args.file:
                text = reader.read_txt_file(args.file)
                if not text:
                    print("❌ 無法讀取檔案")
                    return 1
            else:
                text = args.text
            
            success = reader.speak_text(
                text,
                record_mp3=args.record,
                output_filename=args.output
            )
            
            return 0 if success else 1
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            return 1
    
    # 圖形界面模式 (預設)
    try:
        app = TTSGui()
        app.run()
        return 0
    except Exception as e:
        print(f"❌ GUI啟動失敗: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
