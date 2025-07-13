#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 正確測試 - 處理多說話者模型
"""

import os
# 設置環境變量自動同意條款
os.environ["COQUI_TOS_AGREED"] = "1"

def test_xtts_with_speaker():
    """測試 XTTS v2 多說話者模型"""
    try:
        print("🧪 測試 XTTS v2 多說話者模型...")
        
        # 導入必要套件
        from TTS.api import TTS
        import torch
        import numpy as np
        
        print("✅ TTS.api 導入成功")
        print(f"✅ PyTorch 版本: {torch.__version__}")
        print(f"✅ NumPy 版本: {np.__version__}")
        
        # 檢查 CUDA 是否可用
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✅ 使用設備: {device}")
        
        # 創建 XTTS v2 實例
        print("🤖 正在創建 XTTS v2 實例...")
        
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("✅ XTTS v2 創建成功！")
        
        # 測試語音合成
        print("🔊 測試語音合成...")
        test_text = "你好，這是 XTTS v2 測試"
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_path = temp_file.name
        
        # 方法1：使用內建說話者
        try:
            print("   嘗試方法1：使用內建說話者...")
            tts.tts_to_file(
                text=test_text,
                file_path=output_path,
                language="zh",
                speaker="Claribel Dervla"  # 使用內建說話者
            )
            print("✅ 方法1成功：使用內建說話者")
            
        except Exception as e1:
            print(f"   方法1失敗: {e1}")
            
            # 方法2：使用簡化參數
            try:
                print("   嘗試方法2：使用簡化參數...")
                tts.tts_to_file(
                    text=test_text,
                    file_path=output_path
                )
                print("✅ 方法2成功：使用簡化參數")
                
            except Exception as e2:
                print(f"   方法2失敗: {e2}")
                
                # 方法3：創建參考音頻
                try:
                    print("   嘗試方法3：生成參考音頻...")
                    # 使用 tts 對象的 synthesize 方法
                    wav = tts.tts(text=test_text, language="zh")
                    
                    # 保存音頻
                    import soundfile as sf
                    sf.write(output_path, wav, 22050)
                    print("✅ 方法3成功：直接合成")
                    
                except Exception as e3:
                    print(f"   方法3失敗: {e3}")
                    raise Exception("所有方法都失敗了")
        
        # 檢查結果
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ 語音文件已生成: {output_path}")
            print(f"✅ 文件大小: {file_size} bytes")
            
            if file_size > 1000:
                print("🎉 XTTS v2 測試完全成功！")
                print("✅ 語音合成正常工作")
                
                # 嘗試播放（可選）
                try:
                    import pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load(output_path)
                    pygame.mixer.music.play()
                    
                    import time
                    time.sleep(2)  # 播放2秒
                    pygame.mixer.music.stop()
                    print("🔊 語音播放測試成功")
                    
                except:
                    print("⚠️  語音播放測試跳過（可能是音頻格式問題）")
                
                return True
            else:
                print("⚠️  語音文件太小，可能有問題")
                return False
        else:
            print("❌ 語音文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ XTTS v2 測試失敗: {e}")
        import traceback
        print("詳細錯誤信息:")
        traceback.print_exc()
        return False
    finally:
        # 清理臨時文件
        try:
            if 'output_path' in locals() and os.path.exists(output_path):
                os.unlink(output_path)
        except:
            pass

if __name__ == "__main__":
    print("🚀 XTTS v2 多說話者模型測試")
    print("=" * 55)
    
    success = test_xtts_with_speaker()
    
    if success:
        print("\n🎯 測試結果: 成功！")
        print("XTTS v2 多說話者模型已正確配置並可以使用")
        print("\n📝 接下來您可以:")
        print("1. 運行 xtts_reader.py 進行語音合成")
        print("2. 運行 tts_compare.py 比較不同 TTS 引擎")
        print("3. 指定不同的說話者進行語音合成")
    else:
        print("\n❌ 測試結果: 失敗")
        print("請檢查安裝或查看錯誤信息")
    
    print("=" * 55)
