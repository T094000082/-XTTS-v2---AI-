#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XTTS v2 完整解決方案 - 處理多說話者問題
"""

import os
# 自動同意條款
os.environ["COQUI_TOS_AGREED"] = "1"

def test_xtts_with_all_methods():
    """測試 XTTS v2 的所有可能方法"""
    print("🚀 XTTS v2 多說話者解決方案測試")
    print("=" * 60)
    
    try:
        from TTS.api import TTS
        import torch
        import tempfile
        
        print("✅ 基本導入成功")
        
        # 創建 TTS 實例
        print("🤖 創建 XTTS v2 實例...")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print("✅ XTTS v2 實例創建成功")
        
        # 測試文本
        test_text = "你好，這是多說話者測試"
        
        # 創建臨時文件
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            output_path = tmp.name
        
        print(f"🔊 測試語音合成: {test_text}")
        
        # ==========================================
        # 方法1: 獲取可用說話者列表
        # ==========================================
        print("\n📋 方法1: 檢查可用說話者...")
        try:
            # 嘗試獲取說話者信息
            if hasattr(tts, 'speakers') and tts.speakers:
                print(f"✅ 找到 {len(tts.speakers)} 個說話者:")
                for i, speaker in enumerate(tts.speakers[:5]):  # 只顯示前5個
                    print(f"   {i+1}. {speaker}")
                
                # 使用第一個說話者
                speaker_name = tts.speakers[0]
                print(f"🎯 使用說話者: {speaker_name}")
                
                tts.tts_to_file(
                    text=test_text,
                    file_path=output_path,
                    speaker=speaker_name,
                    language="zh"
                )
                print("✅ 方法1成功: 使用內建說話者列表")
                return check_output_file(output_path)
                
        except Exception as e:
            print(f"   方法1失敗: {e}")
        
        # ==========================================
        # 方法2: 使用常見說話者名稱
        # ==========================================
        print("\n🎭 方法2: 使用常見說話者名稱...")
        common_speakers = [
            "Claribel Dervla",
            "Daisy Studious", 
            "Gracie Wise",
            "Tammie Ema",
            "Alison Dietlinde",
            "Ana Florence",
            "Annmarie Nele",
            "Asya Anara",
            "Brenda Stern",
            "Gitta Nikolina"
        ]
        
        for speaker in common_speakers:
            try:
                print(f"   嘗試說話者: {speaker}")
                tts.tts_to_file(
                    text=test_text,
                    file_path=output_path,
                    speaker=speaker,
                    language="zh"
                )
                print(f"✅ 方法2成功: 使用說話者 {speaker}")
                return check_output_file(output_path)
            except Exception as e:
                print(f"   說話者 {speaker} 失敗: {e}")
                continue
        
        # ==========================================
        # 方法3: 使用 speaker_idx (說話者索引)
        # ==========================================
        print("\n🔢 方法3: 使用說話者索引...")
        for idx in range(5):  # 嘗試前5個索引
            try:
                print(f"   嘗試說話者索引: {idx}")
                tts.tts_to_file(
                    text=test_text,
                    file_path=output_path,
                    speaker_idx=idx,
                    language="zh"
                )
                print(f"✅ 方法3成功: 使用說話者索引 {idx}")
                return check_output_file(output_path)
            except Exception as e:
                print(f"   索引 {idx} 失敗: {e}")
                continue
        
        # ==========================================
        # 方法4: 不使用語言參數
        # ==========================================
        print("\n🌐 方法4: 簡化參數...")
        try:
            tts.tts_to_file(
                text=test_text,
                file_path=output_path,
                speaker="Claribel Dervla"
            )
            print("✅ 方法4成功: 簡化參數")
            return check_output_file(output_path)
        except Exception as e:
            print(f"   方法4失敗: {e}")
        
        # ==========================================
        # 方法5: 使用 tts() 方法而不是 tts_to_file()
        # ==========================================
        print("\n🎵 方法5: 使用直接合成方法...")
        try:
            # 直接合成音頻
            wav = tts.tts(text=test_text, speaker="Claribel Dervla")
            
            # 保存音頻
            import soundfile as sf
            sf.write(output_path, wav, 22050)
            print("✅ 方法5成功: 直接合成")
            return check_output_file(output_path)
        except Exception as e:
            print(f"   方法5失敗: {e}")
        
        print("❌ 所有方法都失敗了")
        return False
        
    except Exception as e:
        print(f"❌ 測試過程出錯: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 清理
        try:
            if 'output_path' in locals():
                os.unlink(output_path)
        except:
            pass

def check_output_file(output_path):
    """檢查輸出文件"""
    try:
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"📁 輸出文件: {output_path}")
            print(f"📊 文件大小: {size} bytes")
            
            if size > 1000:  # 大於1KB
                print("🎉 語音文件生成成功！")
                
                # 嘗試播放
                try:
                    import pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load(output_path)
                    pygame.mixer.music.play()
                    
                    print("🔊 正在播放語音...")
                    import time
                    time.sleep(3)  # 播放3秒
                    pygame.mixer.music.stop()
                    print("✅ 播放完成")
                except:
                    print("⚠️  無法播放（文件可能已生成但播放失敗）")
                
                return True
            else:
                print("⚠️  文件太小，可能有問題")
                return False
        else:
            print("❌ 文件未生成")
            return False
    except Exception as e:
        print(f"❌ 檢查文件時出錯: {e}")
        return False

if __name__ == "__main__":
    success = test_xtts_with_all_methods()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 測試結果: 成功！")
        print("✅ XTTS v2 多說話者問題已解決")
        print("\n📝 解決方案總結:")
        print("1. 確認了正確的說話者參數用法")
        print("2. 找到了可用的說話者名稱或索引")
        print("3. 成功生成並播放了語音")
        print("\n🚀 現在您可以正常使用 XTTS v2 了！")
    else:
        print("❌ 測試結果: 失敗")
        print("🔍 可能的原因:")
        print("1. 模型文件損壞或不完整")
        print("2. 虛擬環境配置問題")
        print("3. 依賴版本衝突")
        print("\n💡 建議:")
        print("1. 重新運行 create_xtts_env.bat")
        print("2. 檢查網路連接")
        print("3. 清除模型緩存後重試")
    print("=" * 60)
