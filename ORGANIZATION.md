# 📁 Open Mic Project Organization

This document outlines the organized structure of the Open Mic voice transcription project.

## 🏗️ Project Structure

```
open_mic/
├── open_mic.py                 # Main application (production-ready)
├── README.md                   # Project documentation
├── LANGUAGES.md               # Supported languages list
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── whisper_env/              # Python virtual environment
├── experiments/              # Development experiments & iterations
│   ├── README.md             # Experiments documentation
│   ├── menubar_versions/     # Menu bar interface experiments
│   ├── hotkey_versions/      # Hotkey functionality experiments
│   ├── autopaste_versions/   # Auto-paste functionality experiments
│   ├── gui_versions/         # GUI interface experiments
│   ├── test_versions/        # Basic testing & functionality
│   └── whisper_permission_fix.py  # Permission handling utility
└── archive/                  # Future archive directory
```

## 📚 Key Files

### Production Files
- **`open_mic.py`** - The main, stable application
- **`requirements.txt`** - All Python dependencies
- **`README.md`** - Complete user documentation
- **`LANGUAGES.md`** - List of 99 supported languages

### Development Environment
- **`whisper_env/`** - Virtual environment with all dependencies installed
- **`experiments/`** - All development iterations and experimental versions

## 🧪 Experiment Categories

### Menu Bar Versions (`experiments/menubar_versions/`)
- Different approaches to macOS menu bar integration
- Evolution from basic to refined implementations

### Hotkey Versions (`experiments/hotkey_versions/`)
- Global hotkey detection experiments
- Thread-safe implementations
- Performance optimizations

### Auto-Paste Versions (`experiments/autopaste_versions/`)
- Automatic text pasting functionality
- macOS permission handling
- AppleScript integration attempts

### GUI Versions (`experiments/gui_versions/`)
- Traditional GUI window approaches
- Alternative user interfaces

### Test Versions (`experiments/test_versions/`)
- Basic Whisper functionality testing
- Audio capture experiments
- Simple transcription tests

## 🔧 Setup & Usage

1. **Activate environment**: `source whisper_env/bin/activate`
2. **Run application**: `python open_mic.py`
3. **Explore experiments**: Check `experiments/` for development history

## 📝 Development Notes

- All scattered development files have been organized into logical categories
- Virtual environment moved into project directory for better organization
- `.gitignore` updated to reflect new structure
- Experiments are preserved for reference and learning

## 🎯 Clean Organization Benefits

- **Clear separation** between production code and experiments
- **Easy navigation** with logical directory structure
- **Complete history** preserved in experiments folder
- **Professional structure** suitable for collaboration or portfolio

---

**🧹 Organization completed on**: September 16, 2025