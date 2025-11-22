"""
Lightweight Build Script for Moonlighter 2 Overlay
Optimized to create a minimal EXE (<50MB) using Tesseract OCR instead of EasyOCR
"""

import PyInstaller.__main__
import os
import shutil
import urllib.request
import zipfile

def download_tesseract():
    """Download portable Tesseract if not already present"""
    tesseract_dir = os.path.join(os.path.dirname(__file__), 'tesseract_portable')
    
    if os.path.exists(tesseract_dir):
        print(f"✓ Tesseract already downloaded at {tesseract_dir}")
        return tesseract_dir
    
    print("\n[Downloading Tesseract Portable]")
    print("This is a one-time download (~40MB)...")
    
    # URL for Tesseract portable (UB Mannheim build)
    tesseract_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
    
    print(f"\n⚠️ Please download Tesseract manually from:")
    print(f"   {tesseract_url}")
    print(f"\nOr install via:")
    print(f"   winget install UB-Mannheim.TesseractOCR")
    print(f"\nThen extract to: {tesseract_dir}")
    print(f"\nAlternatively, if you have Tesseract installed, create this folder structure:")
    print(f"  {tesseract_dir}/")
    print(f"    tesseract.exe")
    print(f"    tessdata/")
    print(f"      eng.traineddata")
    
    return None

def prepare_tesseract():
    """Prepare Tesseract for bundling"""
    # Check for system Tesseract installation
    system_paths = [
        r"C:\Program Files\Tesseract-OCR",
        r"C:\Program Files (x86)\Tesseract-OCR",
    ]
    
    tesseract_source = None
    for path in system_paths:
        if os.path.exists(os.path.join(path, 'tesseract.exe')):
            tesseract_source = path
            print(f"✓ Found system Tesseract at: {path}")
            break
    
    if not tesseract_source:
        print("\n⚠️ Tesseract not found in system directories")
        tesseract_source = download_tesseract()
        if not tesseract_source:
            print("\n❌ Cannot proceed without Tesseract")
            print("\nPlease install Tesseract:")
            print("  1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("  2. Or run: winget install UB-Mannheim.TesseractOCR")
            return None
    
    # Create bundle directory
    bundle_dir = os.path.join(os.path.dirname(__file__), 'tesseract_bundle')
    os.makedirs(bundle_dir, exist_ok=True)
    
    # Copy essential files only
    print(f"\n[Preparing Tesseract Bundle]")
    
    # Copy tesseract.exe
    src_exe = os.path.join(tesseract_source, 'tesseract.exe')
    dst_exe = os.path.join(bundle_dir, 'tesseract.exe')
    if os.path.exists(src_exe):
        shutil.copy2(src_exe, dst_exe)
        print(f"✓ Copied tesseract.exe ({os.path.getsize(dst_exe) / 1024 / 1024:.1f} MB)")
    
    # Copy tessdata (English only to minimize size)
    tessdata_src = os.path.join(tesseract_source, 'tessdata')
    tessdata_dst = os.path.join(bundle_dir, 'tessdata')
    os.makedirs(tessdata_dst, exist_ok=True)
    
    # Copy only English language data
    eng_file = 'eng.traineddata'
    src_lang = os.path.join(tessdata_src, eng_file)
    dst_lang = os.path.join(tessdata_dst, eng_file)
    
    if os.path.exists(src_lang):
        shutil.copy2(src_lang, dst_lang)
        print(f"✓ Copied {eng_file} ({os.path.getsize(dst_lang) / 1024 / 1024:.1f} MB)")
    else:
        print(f"⚠️ Warning: {eng_file} not found")
    
    return bundle_dir

def build_exe():
    """Build the lightweight executable"""
    
    print("=" * 60)
    print("Building LIGHTWEIGHT Moonlighter 2 Overlay EXE")
    print("=" * 60)
    
    # Prepare Tesseract
    tesseract_bundle = prepare_tesseract()
    if not tesseract_bundle:
        return
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller arguments - HEAVILY OPTIMIZED
    pyinstaller_args = [
        'overlay.py',
        '--name=MoonlighterOverlay',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        
        # Add data files
        '--add-data=data.json;.',
        '--add-data=config.json;.',
        
        # Bundle Tesseract
        f'--add-binary={os.path.join(tesseract_bundle, "tesseract.exe")};tesseract',
        f'--add-data={os.path.join(tesseract_bundle, "tessdata")};tesseract/tessdata',
        
        # Hidden imports (only what we need)
        '--hidden-import=pytesseract',
        '--hidden-import=mss',
        '--hidden-import=PIL',
        '--hidden-import=PIL.ImageEnhance',
        '--hidden-import=numpy',
        '--hidden-import=rapidfuzz',
        '--hidden-import=keyboard',
        '--hidden-import=tkinter',
        
        # EXCLUDE heavy packages
        '--exclude-module=torch',
        '--exclude-module=torchvision',
        '--exclude-module=tensorflow',
        '--exclude-module=cv2',
        '--exclude-module=scipy',
        '--exclude-module=matplotlib',
        '--exclude-module=pandas',
        '--exclude-module=IPython',
        '--exclude-module=jupyter',
        '--exclude-module=notebook',
        '--exclude-module=pytest',
        '--exclude-module=pip',
        '--exclude-module=setuptools',
        
        # Additional options
        '--clean',
        '--noconfirm',
        '--optimize=2',
        '--strip',  # Remove debug symbols
        
        # Reduce binary size
        '--noupx',  # Don't use UPX (can be unreliable)
    ]
    
    print("\n[1/2] Running PyInstaller with optimizations...")
    print(f"Working directory: {current_dir}")
    print(f"Building: overlay.py -> MoonlighterOverlay.exe")
    print("\nOptimizations enabled:")
    print("  ✓ Excluding PyTorch, TensorFlow, and other heavy libraries")
    print("  ✓ Bundling minimal Tesseract (English only)")
    print("  ✓ Bytecode optimization level 2")
    print("  ✓ Debug symbols stripped")
    
    # Run PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n[2/2] Creating distribution package...")
    
    # Create dist folder structure
    dist_folder = os.path.join(current_dir, 'MoonlighterOverlay_Release')
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Copy EXE to distribution folder
    exe_path = os.path.join(current_dir, 'dist', 'MoonlighterOverlay.exe')
    if os.path.exists(exe_path):
        shutil.copy(exe_path, dist_folder)
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"✓ Copied MoonlighterOverlay.exe ({exe_size:.1f} MB)")
    
    # Copy essential files
    files_to_copy = ['README_VN.md', 'data.json', 'config.json']
    for file in files_to_copy:
        src = os.path.join(current_dir, file)
        if os.path.exists(src):
            shutil.copy(src, dist_folder)
            print(f"✓ Copied {file}")
        else:
            print(f"⚠️ Warning: {file} not found")
    
    # Create README for users
    readme_content = """# Moonlighter 2 Price Overlay

## Cách sử dụng:
1. Chạy file MoonlighterOverlay.exe
2. Nhấn F6 để scan item
3. Nhấn F5 để chọn vùng OCR (nếu cần)
4. Nhấn F4 để ẩn/hiện overlay

## Lưu ý:
- App này đã bundle sẵn Tesseract OCR (không cần cài thêm gì)
- File data.json chứa database giá cả
- File config.json chứa cấu hình

## Yêu cầu:
- Windows 10 trở lên
- Không cần cài Python hay dependencies khác

Enjoy! 🎮
"""
    
    with open(os.path.join(dist_folder, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Created README.txt")
    
    print("\n" + "=" * 60)
    print("✓ Build complete!")
    print("=" * 60)
    print(f"\nPackage location: {dist_folder}")
    print("\nContents:")
    
    total_size = 0
    for item in os.listdir(dist_folder):
        item_path = os.path.join(dist_folder, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path) / (1024 * 1024)  # MB
            total_size += size
            print(f"  - {item} ({size:.1f} MB)")
    
    print(f"\nTotal package size: {total_size:.1f} MB")
    
    if exe_size < 100:
        print("\n🎉 SUCCESS! EXE is lightweight!")
    else:
        print(f"\n⚠️ EXE is larger than expected ({exe_size:.1f} MB)")
        print("   This might be due to dependencies not being properly excluded")
    
    print("\n" + "=" * 60)
    print("Ready to distribute!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        build_exe()
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
