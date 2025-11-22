# Moonlighter 2 Price Overlay

A lightweight overlay application that displays item prices for Moonlighter 2 using OCR technology.

## ✨ Features

- 🔍 **Real-time OCR** - Automatically reads item names from your screen
- 💰 **Price Display** - Shows "Perfect Stamp" prices from a comprehensive database
- 🎨 **Rarity Colors** - Items displayed in color based on rarity (Common/Uncommon/Rare/Epic/Legendary)
- 🪟 **Always-on-Top Overlay** - Stays visible while you play
- ⌨️ **Hotkey Controls** - Easy keyboard shortcuts
- 🎯 **Custom OCR Region** - Select specific screen area for better accuracy
- 📦 **Super Lightweight** - Only 32MB (down from 2.7GB!)

## 📊 Optimization Results

| Version | Size | Technology |
|---------|------|------------|
| **Previous (EasyOCR)** | 2.7 GB | PyTorch + Deep Learning |
| **Current (Tesseract)** | **32 MB** | Traditional OCR |
| **Reduction** | **98.8%** | ⭐ |

### Why So Much Smaller?

The new version uses **Tesseract OCR** instead of EasyOCR, which means:
- ✅ No PyTorch (~1GB saved)
- ✅ No CUDA libraries (~1GB saved)
- ✅ No neural network models (~500MB saved)
- ✅ Faster startup time (1-2 seconds vs 10-15 seconds)
- ✅ Lower memory usage (100-200 MB vs 2-3 GB)

## 🚀 Quick Start

### Download & Run
1. Download the latest release from `MoonlighterOverlay_Release` folder
2. Double-click `MoonlighterOverlay.exe`
3. The overlay will appear in the top-right corner of your screen

### Hotkeys
- **F6** - Scan item (read item name and display price)
- **F5** - Select custom OCR region (if needed)
- **F4** - Toggle overlay visibility (show/hide)
- **F3** - Toggle view mode (Compact/Detailed)
- **ESC** - Quit application
- **Click overlay** - Toggle between compact and detailed view

## 📖 How to Use

1. **Launch the application** - Run `MoonlighterOverlay.exe`
2. **Start Moonlighter 2** - Open your game
3. **Hover over an item** - Move your cursor over any item in your inventory
4. **Press F6** - The app will scan and display the price
5. **View the price** - Check the overlay for pricing information

### Tips for Best Results
- Make sure item text is clearly visible on screen
- If OCR accuracy is low, press **F5** to select a custom screen region
- Ensure good contrast between text and background
- The app works best with default game UI scaling

## 📦 Package Contents

```
MoonlighterOverlay_Release/
├── MoonlighterOverlay.exe    (32.3 MB) - Main executable
├── config.json                - Configuration settings
├── data.json                  - Item price database
├── README.txt                 - Quick start guide
└── README_VN.md              - Vietnamese documentation
```

## 🛠️ Configuration

Edit `config.json` to customize settings:

```json
{
  "scan_frequency": 0.5,
  "hotkey": "f6",
  "fuzzy_match_threshold": 80,
  "use_custom_region": false,
  "custom_ocr_region": {
    "left": 400,
    "top": 350,
    "width": 250,
    "height": 70
  }
}
```

### Settings Explained
- `scan_frequency` - How often to scan (in seconds)
- `hotkey` - Key to trigger scanning (default: F6)
- `fuzzy_match_threshold` - Minimum similarity for item matching (0-100)
- `use_custom_region` - Enable custom OCR region
- `custom_ocr_region` - Coordinates for custom region (set via F5)

## 💾 Item Database

The `data.json` file contains the item database with:
- Item names
- Perfect Stamp prices
- Rarity levels
- Location information

You can edit this file to add or update items.

## 🔧 Building from Source

### Requirements
- Python 3.8+
- Tesseract-OCR installed on your system
- PyInstaller

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Tesseract
**Windows:**
```bash
winget install UB-Mannheim.TesseractOCR
```

**Or download from:** [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

### Build Lightweight EXE
```bash
python build_lightweight.py
```

This will create a ~30-40MB executable in the `MoonlighterOverlay_Release` folder with:
- Bundled Tesseract (no external installation needed)
- Optimized dependencies
- All heavy libraries excluded

### Run from Source (Development)
```bash
python overlay.py
```

## 📋 Technical Details

### OCR Engine: Tesseract vs EasyOCR

| Feature | EasyOCR | Tesseract |
|---------|---------|-----------|
| Accuracy | 95-99% | 85-95% |
| Speed | Slower | Faster |
| Size | 2.7 GB | 32 MB |
| GPU Required | Recommended | No |
| Dependencies | PyTorch, CUDA | Minimal |

**Why we switched:** For reading simple English item names, Tesseract provides excellent accuracy at a fraction of the size.

### Architecture

The application consists of:
- **overlay.py** - Main application and hotkey handler
- **screen_reader.py** - OCR engine and screen capture
- **price_database.py** - Item database and fuzzy matching
- **overlay_window.py** - Tkinter-based overlay UI
- **region_selector.py** - Custom region selection tool

### Image Processing

Tesseract works best with preprocessed images:
1. Convert to grayscale
2. Enhance contrast (2x)
3. Apply OCR with optimized settings (`--oem 3 --psm 6`)

## 🐛 Troubleshooting

### OCR not detecting text
- Press **F5** to select a custom OCR region
- Ensure the selected region contains clear, readable text
- Check if game UI scaling is affecting text visibility
- Try increasing contrast in game settings

### "Tesseract not found" error
- This shouldn't happen with the bundled EXE
- If it does, install Tesseract: `winget install UB-Mannheim.TesseractOCR`

### Executable won't run
- Check Windows Defender (may flag new EXE files)
- Ensure `config.json` and `data.json` are in the same folder
- Right-click → Properties → Unblock (if downloaded from internet)

### Item not found in database
- The item may not be in the database yet
- Add it manually to `data.json`
- Check for typos in the item name

### Low accuracy compared to old version
- Tesseract is ~5-10% less accurate than EasyOCR
- For item names, this is usually acceptable
- If critical, you can rebuild with EasyOCR (will be 2.7GB)

## 📝 System Requirements

- **OS:** Windows 10 or later
- **RAM:** 200 MB minimum
- **Disk:** 50 MB for application
- **Display:** Any resolution (1920x1080 recommended)
- **Game:** Moonlighter 2

## 🤝 Contributing

To contribute:
1. Add missing items to `data.json`
2. Report bugs or accuracy issues
3. Suggest UI improvements
4. Share your custom OCR regions for different resolutions

## 📄 License

This is a fan-made tool for Moonlighter 2. Not affiliated with Digital Sun Games.

## 🎮 Credits

- **Moonlighter 2** - Digital Sun Games
- **OCR Engine** - Tesseract (Google)
- **Fuzzy Matching** - RapidFuzz library

## 📞 Support

If you encounter issues:
1. Check this README for troubleshooting
2. Verify all files are in the same folder
3. Test the custom OCR region (F5)
4. Report persistent issues with screenshots

---

**Enjoy easier trading in Moonlighter 2!** 🌙✨
