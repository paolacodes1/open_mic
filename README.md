# 🎤 Open Mic - Free Voice Transcriber

A completely **FREE**, **offline** voice transcription app for macOS with automatic pasting functionality. No API keys, no internet required, no subscriptions!

![Demo](https://img.shields.io/badge/Status-Working-brightgreen) ![Languages](https://img.shields.io/badge/Languages-99%20Supported-blue) ![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)

## ✨ Features

- 🎯 **Completely FREE** - No API keys or subscriptions needed
- 🌍 **99 Languages** - Automatic language detection
- 🔥 **Auto-Paste** - Text appears instantly at your cursor
- ⚡ **Hotkey Control** - Press `Ctrl+Space` to record
- 🔒 **100% Offline** - All processing happens locally
- 🎪 **Menu Bar App** - Lives quietly in your menu bar
- 📋 **Clipboard Backup** - Always copies to clipboard as backup
- ⏱️ **Auto-Stop** - 30-second safety timeout
- 🎨 **Visual Feedback** - Clear recording/processing indicators

## 🚀 Quick Start

### Prerequisites
- macOS (tested on macOS 14+)
- Python 3.8+
- Microphone access permissions

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/paolacodes1/open_mic.git
   cd open_mic
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv whisper_env
   source whisper_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install openai-whisper sounddevice rumps pynput numpy
   ```

4. **Run the app**
   ```bash
   export PYTHONHTTPSVERIFY=0
   python open_mic.py
   ```

5. **Set up permissions** (required for auto-paste)
   - Go to **System Settings > Privacy & Security > Accessibility**
   - Add **Terminal** to the allowed apps
   - Restart the app

## 🎮 How to Use

1. **Look for the 🎤 icon** in your menu bar
2. **Press `Ctrl+Space`** to start recording (icon turns 🔴)
3. **Speak your text** clearly
4. **Press `Ctrl+Space`** again to stop (icon turns 🟠 while processing)
5. **Text auto-pastes** at your cursor location (icon turns ✅)

### Menu Options
- **🧪 Test Auto-Paste Now** - Test if permissions are working
- **🔧 Open System Settings** - Quick access to fix permissions
- **📋 Copy Last Text** - Manually copy last transcription
- **✨ Auto-Paste: ON/OFF** - Toggle auto-paste feature

## 🌍 Supported Languages

Auto-detects and transcribes **99 languages** including:

- **Major Languages**: English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi
- **European**: Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Czech, Hungarian, Romanian, Bulgarian
- **Asian**: Thai, Vietnamese, Indonesian, Malay, Bengali, Tamil, Telugu, Gujarati, Punjabi
- **And many more!** See full list in [LANGUAGES.md](LANGUAGES.md)

## 🛠️ Troubleshooting

### Auto-Paste Not Working?
1. Click **"🧪 Test Auto-Paste Now"** in the menu
2. If it fails, click **"🔧 Open System Settings"**
3. Go to **Privacy & Security > Accessibility**
4. Add **Terminal** to allowed apps
5. **Restart the app**

### No Sound/Recording Issues?
1. Check microphone permissions in **System Settings > Privacy & Security > Microphone**
2. Add **Terminal** or **Python** to allowed apps
3. Test your microphone in other apps first

### Common Issues
- **"Model not loaded"** - Wait a few seconds for Whisper to initialize
- **"Recording too short"** - Speak for at least 1 second
- **"No speech detected"** - Speak louder or check microphone
- **SSL errors** - The app includes SSL workarounds, should work automatically

## 🏗️ Architecture

- **OpenAI Whisper** - Local speech recognition (base model)
- **rumps** - macOS menu bar interface
- **sounddevice** - Audio recording
- **pynput** - Global hotkey detection
- **AppleScript** - Auto-paste functionality via `osascript`

## 📝 Files

- `open_mic.py` - Main application with permission diagnostics
- `requirements.txt` - Python dependencies
- `README.md` - This documentation
- `LANGUAGES.md` - Complete list of supported languages

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional hotkey combinations
- Different Whisper model sizes
- Windows/Linux support
- Custom vocabulary
- Punctuation commands

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **OpenAI** for the incredible Whisper model
- **Community** for testing and feedback
- Built with ❤️ for the developer community

## ⭐ Star This Repo

If this saved you from expensive transcription services, please give it a star! ⭐

---

**🆓 Completely free forever. No hidden costs, no API limits, no subscriptions.**