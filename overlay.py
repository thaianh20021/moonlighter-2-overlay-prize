"""
Moonlighter 2 Price Overlay Application
Main application that integrates all components
"""

import time
import keyboard
from price_database import PriceDatabase
from screen_reader import ScreenReader
from overlay_window import OverlayWindow
import json


class MoonlighterOverlay:
    def __init__(self):
        """Initialize the overlay application"""
        print("=" * 50)
        print("Moonlighter 2 Price Overlay")
        print("=" * 50)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        print("\n[1/3] Loading price database...")
        self.database = PriceDatabase()
        print(f"✓ Loaded {len(self.database.all_items)} items")
        
        print("\n[2/3] Initializing screen reader...")
        self.screen_reader = ScreenReader()
        print("✓ Screen reader ready")
        
        print("\n[3/3] Creating overlay window...")
        self.overlay = OverlayWindow()
        print("✓ Overlay window created")
        
        # State
        self.scanning_enabled = False
        self.last_item_name = None
        self.last_scan_time = 0
        self.visible = True
        
        # Setup hotkey
        self._setup_hotkey()
        
        print("\n" + "=" * 50)
        print("✓ Application ready!")
        print(f"Press {self.config['hotkey'].upper()} to scan item")
        print("Press F5 to select custom OCR region")
        print("Press F4 to toggle overlay visibility")
        print("Press F3 to toggle view mode")
        print("Press ESC to quit application")
        print("=" * 50 + "\n")
    
    def _load_config(self):
        """Load configuration file"""
        try:
            with open("config.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "scan_frequency": 0.5,
                "hotkey": "f6",
                "fuzzy_match_threshold": 80
            }
    
    def _setup_hotkey(self):
        """Setup keyboard hotkeys"""
        hotkey_scan = self.config.get('hotkey', 'f6')
        hotkey_select = 'f5'  # Region selection hotkey
        hotkey_toggle = 'f4'  # Visibility toggle hotkey
        hotkey_view = 'f3'    # View mode toggle hotkey
        hotkey_quit = 'esc'   # Quit application hotkey
        
        keyboard.add_hotkey(hotkey_scan, self.toggle_scanning)
        keyboard.add_hotkey(hotkey_select, self.select_region)
        keyboard.add_hotkey(hotkey_toggle, self.toggle_visibility)
        keyboard.add_hotkey(hotkey_view, self.toggle_view_mode)
        keyboard.add_hotkey(hotkey_quit, self.quit_application)
        
        print(f"Hotkey registered: {hotkey_scan.upper()} (scan item)")
        print(f"Hotkey registered: {hotkey_select.upper()} (select OCR region)")
        print(f"Hotkey registered: {hotkey_toggle.upper()} (toggle visibility)")
        print(f"Hotkey registered: {hotkey_view.upper()} (toggle view mode)")
        print(f"Hotkey registered: {hotkey_quit.upper()} (quit application)")
    
    def select_region(self):
        """Open region selector (F5)"""
        print("\n📐 Opening region selector...")
        print("Vui lòng click và kéo để chọn vùng OCR")
        
        try:
            from region_selector import RegionSelector
            
            # Minimize overlay temporarily
            self.overlay.root.withdraw()
            
            # Open selector
            selector = RegionSelector(config_file="config.json")
            region = selector.select_region()
            
            # Restore overlay
            self.overlay.root.deiconify()
            
            if region:
                print("✓ Vùng OCR đã được cập nhật. Vui lòng khởi động lại app!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    def toggle_visibility(self):
        """Toggle overlay visibility (F4)"""
        if self.visible:
            self.overlay.root.withdraw()
            self.visible = False
            print("\n👻 Overlay hidden")
        else:
            self.overlay.root.deiconify()
            self.visible = True
            print("\n👀 Overlay visible")
    
    def toggle_view_mode(self):
        """Toggle view mode (F3)"""
        self.overlay.toggle_mode()
        mode = "Compact" if self.overlay.compact_mode else "Detailed"
        print(f"\n🔄 View mode: {mode}")

    def quit_application(self):
        """Quit the application (ESC)"""
        print("\n👋 Shutting down...")
        self.overlay.close()
        import sys
        sys.exit(0)
    
    def toggle_scanning(self):
        """Execute a single scan when F6 is pressed"""
        print("\n🔍 Scanning...")
        
        # Initialize OCR on first use (lazy loading)
        if not hasattr(self, 'ocr_initialized') or not self.ocr_initialized:
            self.screen_reader.initialize_ocr()
            self.ocr_initialized = True
        
        # Update overlay to show scanning status
        self.overlay.update_display(scanning=True)
        
        # Capture and read screen
        item_name = self.screen_reader.get_current_item_name()
        
        if item_name:
            print(f"📖 Detected text: '{item_name}'")
            
            # Search in database
            threshold = self.config.get('fuzzy_match_threshold', 80)
            item = self.database.find_item(item_name, threshold=threshold)
            
            if item:
                print(f"✓ Found: {item['name']} - {item['price']}g (match: {item.get('match_score', 100)}%)")
                self.overlay.update_display(item=item, scanning=False)
                self.last_item_name = item_name
            else:
                print(f"✗ Not found: '{item_name}'")
                # Show unknown item in overlay
                self.overlay.update_display(item={
                    'name': f"Unknown: {item_name}",
                    'rarity': 'Common',
                    'price': 0,
                    'location': 'Unknown'
                }, scanning=False)
                self.last_item_name = item_name
        else:
            print("⚠️ No text detected")
            self.overlay.update_display(scanning=False)
    
    def scan_and_update(self):
        """
        Periodic update callback (no longer used for scanning)
        This just keeps the UI responsive
        """
        pass
    
    def run(self):
        """Run the application"""
        # Start the overlay window with update callback
        self.overlay.run(self.scan_and_update)


def main():
    """Main entry point"""
    try:
        app = MoonlighterOverlay()
        app.run()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
