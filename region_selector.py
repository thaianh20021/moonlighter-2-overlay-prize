"""
Region Selector Tool
Allows user to select OCR region by clicking and dragging
"""

import tkinter as tk
from tkinter import messagebox
import json
import ctypes

class RegionSelector:
    def __init__(self, config_file="config.json"):
        """Initialize the region selector"""
        self.config_file = config_file
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selected_region = None
        
        # Enable DPI awareness for Windows
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
        
    def select_region(self):
        """Open a transparent overlay for region selection"""
        self.root = tk.Tk()
        
        # Get screen dimensions (DPI aware)
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        
        # Window setup
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.4)  # Slightly more opaque
        self.root.configure(bg='black')
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            cursor="cross",
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        self.canvas.create_text(
            screen_width // 2,
            100,
            text="KÉO CHUỘT ĐỂ CHỌN VÙNG\nESC: Hủy",
            font=('Segoe UI', 24, 'bold'),
            fill='#00FF00',
            justify='center'
        )
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.root.bind('<Escape>', lambda e: self.cancel())
        
        # Force focus and lift
        self.root.lift()
        self.root.focus_force()
        
        self.root.mainloop()
        return self.selected_region
    
    def on_press(self, event):
        """Mouse button pressed"""
        self.start_x = event.x
        self.start_y = event.y
        
        # Remove old rectangle if any
        if self.rect:
            self.canvas.delete(self.rect)
            
        # Create new rectangle
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='#00FF00', width=2, fill='#00FF00', stipple='gray50'
        )
    
    def on_drag(self, event):
        """Mouse dragged"""
        if self.rect:
            self.canvas.coords(
                self.rect,
                self.start_x, self.start_y,
                event.x, event.y
            )
    
    def on_release(self, event):
        """Mouse button released"""
        if self.rect:
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)
            
            width = x2 - x1
            height = y2 - y1
            
            if width < 20 or height < 20:
                return  # Ignore tiny clicks
                
            self.selected_region = {
                'left': int(x1),
                'top': int(y1),
                'width': int(width),
                'height': int(height)
            }
            
            # Ask to save
            if messagebox.askyesno("Xác nhận", "Lưu vùng chọn này?"):
                self.save_region()
                self.root.destroy()
            else:
                self.canvas.delete(self.rect)
                self.rect = None
    
    def save_region(self):
        """Save selected region to config"""
        if not self.selected_region:
            return
        
        try:
            # Load existing config
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            except FileNotFoundError:
                config = {}
            
            # Save custom region
            config['custom_ocr_region'] = self.selected_region
            config['use_custom_region'] = True
            
            # Write back
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"\n✓ Đã lưu vùng OCR: {self.selected_region}")
            messagebox.showinfo(
                "Thành công",
                "Đã lưu vùng OCR!\n"
                "Khởi động lại ứng dụng để áp dụng."
            )
        except Exception as e:
            print(f"Error saving region: {e}")
            messagebox.showerror("Lỗi", f"Không thể lưu cấu hình: {e}")
    
    def cancel(self):
        """Cancel selection"""
        self.selected_region = None
        self.root.destroy()


if __name__ == "__main__":
    print("Region Selector Tool")
    print("Nhấn và kéo để chọn vùng OCR")
    
    selector = RegionSelector()
    region = selector.select_region()
    
    if region:
        print(f"\nVùng đã chọn: {region}")
    else:
        print("\nĐã hủy")
