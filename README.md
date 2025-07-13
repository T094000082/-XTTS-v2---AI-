# 🎤 XTTS v2 讀稿機 - AI 語音合成專案

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![XTTS](https://img.shields.io/badge/XTTS-v2-green.svg)](https://github.com/coqui-ai/TTS)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

這是一個功能完整的 AI 語音合成專案，整合了 **XTTS v2** 高品質語音合成與系統內建 TTS，提供多層次的語音解決方案。

## ✨ **功能特色**

### 🎯 **多引擎支持**
- **🚀 XTTS v2**: 高品質 AI 語音合成，支援多說話者與聲音克隆
- **🔧 系統 TTS**: Windows SAPI/pyttsx3 作為穩定備用方案
- **📊 智能選擇**: 自動偵測最佳可用引擎

### 🌏 **多語言支持**
- **中文**: 完整的中文語音合成支持
- **英文**: 原生英文語音
- **多語言**: 支援 XTTS v2 的所有語言

### 🛠️ **便利工具**
- **一鍵安裝**: 自動環境配置與依賴安裝
- **智能修復**: 自動解決依賴衝突問題
- **引擎比較**: 不同 TTS 引擎效果對比
- **批次腳本**: 便利的啟動與使用腳本

## 🚀 **快速開始**

### 📦 **自動安裝（推薦）**

```batch
# 1. 下載專案
git clone https://github.com/your-username/xtts-reader.git
cd xtts-reader

# 2. 一鍵建立 XTTS v2 環境
create_xtts_env.bat

# 3. 開始使用
start_xtts.bat "你好，歡迎使用 XTTS v2 讀稿機"
```

### ⚡ **快速測試**

```batch
# 系統內建 TTS（立即可用）
python simple_tts.py "Hello World"

# XTTS v2 高品質語音
.\xtts_env\Scripts\python.exe xtts_reader.py "你好世界"
```

## 📋 **專案結構**

```
📁 xtts-reader/
├── 🎤 主要程式
│   ├── xtts_reader.py          # XTTS v2 主程式
│   ├── simple_tts.py           # 系統 TTS 備用方案
│   ├── tts_compare.py          # 引擎比較工具
│   └── smart_tts.py            # 智能 TTS 選擇器
├── 🔧 環境配置
│   ├── create_xtts_env.bat     # XTTS v2 環境建立
│   ├── setup_xtts.bat          # 環境修復腳本
│   └── requirements.txt        # Python 依賴
├── 🧪 測試工具
│   ├── test_xtts_final.py      # 完整功能測試
│   ├── test_xtts_quick.py      # 快速測試
│   └── diagnose_xtts.py        # 問題診斷
├── 📚 說明文件
│   ├── XTTS_v2_解決方案.md     # 技術解決方案
│   ├── 使用指南.md             # 詳細使用說明
│   └── 引擎識別指南.md         # 引擎識別說明
└── 🚀 便利腳本
    ├── start_xtts.bat          # 快速啟動
    └── fix_xtts.bat            # 問題修復
```
```

## 💻 **使用方法**

### 🎯 **方法1：使用便利腳本（推薦）**

```batch
# 啟動 XTTS v2 讀稿機
start_xtts.bat "你好，這是高品質的 AI 語音合成"

# 比較不同 TTS 引擎效果
.\xtts_env\Scripts\python.exe tts_compare.py
```

### 🔧 **方法2：直接使用程式**

```batch
# 系統內建 TTS（永遠可用）
python simple_tts.py "你的文字內容"

# XTTS v2 高品質語音合成
.\xtts_env\Scripts\python.exe xtts_reader.py "你的文字內容"

# 智能 TTS（自動選擇最佳引擎）
python smart_tts.py "你的文字內容"
```

### 🧪 **方法3：測試與診斷**

```batch
# 快速測試所有功能
.\xtts_env\Scripts\python.exe test_xtts_final.py

# 檢查環境狀態
.\xtts_env\Scripts\python.exe xtts_reader.py --check

# 修復環境問題
.\xtts_env\Scripts\python.exe xtts_reader.py --fix
```

## 🔧 **命令列參數**

### **xtts_reader.py**
```bash
python xtts_reader.py [文字] [選項]

選項:
  --language, -l    語言代碼 (zh, en, ja...)
  --check, -c       檢查運行環境
  --fix, -f         修復依賴問題
```

### **支援的語言代碼**
- `zh` - 中文（繁體/簡體）
- `en` - 英文
- `ja` - 日文
- `ko` - 韓文
- `es` - 西班牙文
- `fr` - 法文
- `de` - 德文

## 🛠️ **故障排除**

### ❗ **常見問題**

#### **1. XTTS v2 初始化失敗**
```batch
# 解決方案：重建環境
create_xtts_env.bat
```

#### **2. NumPy 版本衝突**
```batch
# 解決方案：自動修復
.\xtts_env\Scripts\python.exe xtts_reader.py --fix
```

#### **3. 缺少中文支持**
```batch
# 解決方案：安裝中文依賴
.\xtts_env\Scripts\pip.exe install pypinyin
```

#### **4. 模型下載失敗**
```batch
# 解決方案：檢查網路連接並重試
setup_xtts.bat
```

### 🔍 **診斷工具**

```batch
# 完整系統診斷
.\xtts_env\Scripts\python.exe diagnose_xtts.py

# 檢查環境狀態
.\xtts_env\Scripts\python.exe xtts_reader.py --check
```

## 📊 **效能對比**

| 引擎 | 音質 | 速度 | 語言支持 | 安裝難度 |
|------|------|------|----------|----------|
| **XTTS v2** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Windows SAPI** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **pyttsx3** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🔄 **更新日誌**

### **v2.0** (Latest)
- ✅ 整合 XTTS v2 高品質語音合成
- ✅ 多說話者模型支持
- ✅ 自動環境配置與修復
- ✅ 智能引擎選擇機制
- ✅ 完整的故障診斷工具

### **v1.0**
- ✅ 基本系統 TTS 支持
- ✅ 簡單的語音合成功能

## 🤝 **貢獻指南**

歡迎提交 Issues 和 Pull Requests！

### **開發環境設置**
```bash
git clone https://github.com/your-username/xtts-reader.git
cd xtts-reader
create_xtts_env.bat
```

### **提交代碼**
1. Fork 專案
2. 創建功能分支
3. 提交變更
4. 發起 Pull Request

## 📄 **授權協議**

本專案採用 MIT 授權協議 - 詳見 [LICENSE](LICENSE) 文件

## 🙏 **致謝**

- [Coqui TTS](https://github.com/coqui-ai/TTS) - XTTS v2 模型
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Python TTS 庫
- [pygame](https://www.pygame.org/) - 音頻播放支持

## 📞 **聯繫方式**

- **GitHub Issues**: [提交問題](https://github.com/your-username/xtts-reader/issues)
- **技術支持**: 請查看 [使用指南.md](使用指南.md)

---

🎉 **享受高品質的 AI 語音合成體驗！**
- `ko`: 韓文
- `es`: 西班牙文
- `fr`: 法文
- `de`: 德文
- `it`: 義大利文

## 系統需求

- Python 3.8 或更高版本
- Windows 10/11 (推薦)
- 至少 4GB RAM
- 有 GPU 的話會更快 (可選)

## 故障排除

### 問題: XTTS v2 安裝失敗
**解決方案**: 使用簡化版本
```cmd
python simple_tts.py "測試文字"
```

### 問題: 語音播放沒有聲音
**解決方案**: 
1. 檢查系統音量設定
2. 確認音響設備正常運作
3. 嘗試保存為檔案後手動播放

### 問題: 中文語音效果不佳
**解決方案**: 
1. 確保文字使用繁體或簡體中文
2. 可以嘗試提供中文語音樣本進行聲音克隆

## 技術細節

- **進階版本**: 使用 Coqui TTS 的 XTTS v2 模型
- **簡化版本**: 使用 pyttsx3 和 Windows SAPI
- **音頻播放**: 使用 pygame
- **支援格式**: WAV 音頻輸出

## 開發者資訊

此程式使用以下主要套件:
- [Coqui TTS](https://github.com/coqui-ai/TTS): XTTS v2 模型
- [pyttsx3](https://pypi.org/project/pyttsx3/): 跨平台 TTS
- [pygame](https://www.pygame.org/): 音頻播放
- [torch](https://pytorch.org/): 深度學習框架
