#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 讀稿機 - 簡化版
避免複雜依賴，專注於 XTTS v2 功能
"""

import argparse
import sys
import os
import tempfile
import subprocess

# 設置環境變量自動同意 XTTS v2 條款
os.environ["COQUI_TOS_AGREED"] = "1"

def check_xtts_requirements():
    """檢查 XTTS v2 的相關需求"""
    print("🔍 檢查 XTTS v2 運行環境...")
    
    required_packages = [
        'TTS',
        'torch', 
        'pygame',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安裝")
        except ImportError:
            print(f"❌ {package} 未安裝")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少套件: {', '.join(missing_packages)}")
        return False
    
    # 檢查 NumPy 版本兼容性
    try:
        import numpy as np
        numpy_version = np.__version__
        print(f"📦 NumPy 版本: {numpy_version}")
        
        # 檢查是否有版本衝突
        major_version = int(numpy_version.split('.')[0])
        if major_version >= 2:
            print("⚠️  NumPy 2.x 可能與某些套件不兼容")
            return "version_conflict"
    except Exception as e:
        print(f"❌ NumPy 檢查失敗: {e}")
        return False
    
    return True

def test_xtts_import():
    """測試 XTTS 導入"""
    try:
        print("🧪 測試 XTTS 導入...")
        from TTS.api import TTS
        print("✅ TTS.api 導入成功")
        
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
        
        import pygame
        pygame.mixer.init()
        print("✅ pygame 初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ XTTS 導入失敗: {e}")
        return False

def create_xtts_reader():
    """創建 XTTS v2 讀稿機實例"""
    try:
        from TTS.api import TTS
        import pygame
        
        print("🤖 正在初始化 XTTS v2...")
        print("   這可能需要一些時間下載模型...")
        
        # 初始化 pygame
        pygame.mixer.init()
        
        # 初始化 XTTS v2
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        
        print("✅ XTTS v2 初始化成功！")
        return tts
        
    except Exception as e:
        print(f"❌ XTTS v2 初始化失敗: {e}")
        return None

def speak_with_xtts(tts, text, language="zh"):
    """使用 XTTS v2 進行語音合成和播放"""
    try:
        import pygame
        
        print(f"🔊 XTTS v2 正在生成語音: {text}")
        
        # 創建臨時檔案
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        output_path = temp_file.name
        temp_file.close()
        
        # 生成語音 (多重方法嘗試)
        success = False
        
        # 方法1：使用年輕女性說話者（按優先順序排列）
        young_female_speakers = [
            "Tammie Ema",          # 年輕女性，活潑語調
            "Daisy Studious",      # 年輕女性，學術風格
            "Gracie Wise",         # 年輕女性，溫和語調
            "Alison Dietlinde",    # 年輕女性，專業播音
            "Claribel Dervla"      # 年輕女性，清晰發音
        ]
        for speaker in young_female_speakers:
            try:
                print(f"   嘗試年輕女性說話者: {speaker}")
                tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language,
                    speaker=speaker
                )
                print(f"✅ 使用年輕女性說話者 {speaker} 成功")
                success = True
                break
            except Exception as e1:
                print(f"   說話者 {speaker} 失敗: {e1}")
                continue
        
        # 方法2：如果方法1失敗，嘗試使用說話者索引
        if not success:
            for idx in range(5):
                try:
                    print(f"   嘗試說話者索引: {idx}")
                    tts.tts_to_file(
                        text=text,
                        file_path=output_path,
                        language=language,
                        speaker_idx=idx
                    )
                    print(f"✅ 使用說話者索引 {idx} 成功")
                    success = True
                    break
                except Exception as e2:
                    print(f"   索引 {idx} 失敗: {e2}")
                    continue
        
        # 方法3：如果前面都失敗，使用直接合成
        if not success:
            try:
                print("   嘗試直接合成方法...")
                wav = tts.tts(text=text, language=language)
                
                # 保存音頻
                import soundfile as sf
                sf.write(output_path, wav, 22050)
                print("✅ 直接合成成功")
                success = True
            except Exception as e3:
                print(f"   直接合成失敗: {e3}")
        
        # 方法4：最後嘗試使用年輕女性聲音
        if not success:
            try:
                print("   嘗試預設年輕女性聲音...")
                tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker="Tammie Ema"  # 年輕女性，活潑語調
                )
                print("✅ 預設年輕女性聲音成功")
                success = True
            except Exception as e4:
                print(f"   預設年輕女性聲音失敗: {e4}")
                raise Exception("所有語音合成方法都失敗了")
        
        print("🎵 正在播放 XTTS v2 生成的語音...")
        
        # 播放語音
        pygame.mixer.music.load(output_path)
        pygame.mixer.music.play()
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        print("✅ XTTS v2 播放完成")
        
        # 清理臨時檔案
        try:
            os.unlink(output_path)
        except OSError:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ XTTS v2 語音合成失敗: {e}")
        return False

def fix_numpy_conflict():
    """嘗試修復 NumPy 版本衝突"""
    print("🔧 嘗試修復 NumPy 版本衝突...")
    
    commands = [
        [sys.executable, "-m", "pip", "uninstall", "numpy", "-y"],
        [sys.executable, "-m", "pip", "install", "numpy==1.24.3"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", "TTS"]
    ]
    
    for cmd in commands:
        try:
            print(f"執行: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"⚠️  命令執行警告: {result.stderr}")
            else:
                print("✅ 命令執行成功")
        except Exception as e:
            print(f"❌ 命令執行失敗: {e}")
    
    print("🔄 請重新啟動程式以測試修復結果")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="XTTS v2 讀稿機 - 專為 XTTS v2 設計",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python xtts_reader.py "你好，我是 XTTS v2"
  python xtts_reader.py "Hello World" --language en
  python xtts_reader.py --check                    # 檢查環境
  python xtts_reader.py --fix                      # 修復依賴問題
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
        "--check", "-c",
        action="store_true",
        help="檢查 XTTS v2 運行環境"
    )
    
    parser.add_argument(
        "--fix", "-f",
        action="store_true",
        help="嘗試修復依賴問題"
    )
    
    args = parser.parse_args()
    
    try:
        print("🤖 XTTS v2 讀稿機")
        print("=" * 50)
        
        # 修復依賴問題
        if args.fix:
            fix_numpy_conflict()
            return 0
        
        # 檢查環境
        env_status = check_xtts_requirements()
        
        if args.check:
            if env_status == True:
                print("\n✅ 環境檢查完成，可以使用 XTTS v2")
                # 進一步測試導入
                if test_xtts_import():
                    print("🎉 XTTS v2 完全可用！")
                else:
                    print("⚠️  XTTS v2 導入有問題，請嘗試 --fix")
            elif env_status == "version_conflict":
                print("\n⚠️  發現版本衝突，建議執行:")
                print("     python xtts_reader.py --fix")
            else:
                print("\n❌ 環境不完整，請安裝缺少的套件")
            return 0
        
        # 檢查是否提供文字
        if not args.text:
            print("❌ 請提供要朗讀的文字")
            parser.print_help()
            return 1
        
        # 檢查環境狀態
        if env_status != True:
            if env_status == "version_conflict":
                print("⚠️  發現版本衝突，嘗試繼續運行...")
            else:
                print("❌ 環境不完整，無法運行 XTTS v2")
                print("   請先執行: python xtts_reader.py --check")
                return 1
        
        # 測試導入
        if not test_xtts_import():
            print("❌ XTTS v2 導入失敗")
            print("   建議執行: python xtts_reader.py --fix")
            return 1
        
        # 創建 XTTS v2 讀稿機
        tts = create_xtts_reader()
        if tts is None:
            print("❌ XTTS v2 初始化失敗")
            return 1
        
        # 執行語音合成
        success = speak_with_xtts(tts, args.text, args.language)
        
        if success:
            print("🎉 XTTS v2 朗讀完成！")
            return 0
        else:
            print("❌ XTTS v2 朗讀失敗")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⏹️  程式被用戶中斷")
        return 130
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
