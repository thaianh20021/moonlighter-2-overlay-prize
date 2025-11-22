"""
Overlay Window Module for Moonlighter 2
Displays item pricing information in an always-on-top window
"""

import tkinter as tk
from tkinter import font
from typing import Optional, Dict


class OverlayWindow:
    # Rarity color scheme
    RARITY_COLORS = {
        'Common': '#FFFFFF',      # White
        'Uncommon': '#1EFF00',    # Green
        'Rare': '#0070DD',        # Blue
        'Epic': '#A335EE',        # Purple
        'Legendary': '#FF8000'    # Orange
    }
    
    def __init__(self):
        """Initialize the overlay window"""
        self.root = tk.Tk()
        self.root.title("Moonlighter 2 Price Overlay")
        
        # Window properties
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', 0.9)     # Slight transparency
        
        # Remove window decorations but keep it visible
        self.root.overrideredirect(True)
        
        # Dark background
        self.root.configure(bg='#1a1a1a')
        
        # Current state
        self.scanning = False
        self.current_item = None
        self.compact_mode = True  # Start in compact mode
        
        # Position and create UI
        self._create_ui()
        
        # Bind click to toggle mode
        self.root.bind('<Button-1>', lambda e: self.toggle_mode())
        
    def _create_ui(self):
        """Create UI based on current mode"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        if self.compact_mode:
            self._create_compact_ui()
        else:
            self._create_detailed_ui()
    
    def _create_compact_ui(self):
        """Create compact UI (just name + price)"""
        width = 280
        height = 70
        
        # Position at top-right
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 10
        y = 10
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Item name
        self.compact_name_label = tk.Label(
            main_frame,
            text="Moonlighter 2 Prices",
            font=('Segoe UI', 10, 'bold'),
            bg='#1a1a1a',
            fg='#FFD700',
            wraplength=260,
            justify='left'
        )
        self.compact_name_label.pack(anchor='w')
        
        # Price
        self.compact_price_label = tk.Label(
            main_frame,
            text="F6: Scan | F5: Region",
            font=('Segoe UI', 12, 'bold'),
            bg='#1a1a1a',
            fg='#00FF00'
        )
        self.compact_price_label.pack(anchor='w')
        
        # Make labels clickable too
        main_frame.bind('<Button-1>', lambda e: self.toggle_mode())
        self.compact_name_label.bind('<Button-1>', lambda e: self.toggle_mode())
        self.compact_price_label.bind('<Button-1>', lambda e: self.toggle_mode())
    
    def _create_detailed_ui(self):
        """Create detailed UI (full info)"""
        width = 320
        height = 200
        
        # Position at top-right
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 10
        y = 10
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main frame with padding
        main_frame = tk.Frame(self.root, bg='#1a1a1a', padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Title
        title_font = font.Font(family='Segoe UI', size=11, weight='bold')
        title = tk.Label(
            main_frame,
            text="🌙 Moonlighter 2 Prices",
            font=title_font,
            bg='#1a1a1a',
            fg='#FFD700'
        )
        title.pack(anchor='w', pady=(0, 5))
        title.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Status: OFF",
            font=('Segoe UI', 9),
            bg='#1a1a1a',
            fg='#FF4444'
        )
        self.status_label.pack(anchor='w', pady=(0, 5))
        self.status_label.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Separator
        separator = tk.Frame(main_frame, height=1, bg='#444444')
        separator.pack(fill='x', pady=(0, 10))
        
        # Item info frame
        self.info_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        self.info_frame.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Item name
        self.item_name_label = tk.Label(
            self.info_frame,
            text="Click để toggle",
            font=('Segoe UI', 11, 'bold'),
            bg='#1a1a1a',
            fg='#CCCCCC',
            wraplength=280,
            justify='left'
        )
        self.item_name_label.pack(anchor='w', pady=(0, 5))
        self.item_name_label.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Rarity
        self.rarity_label = tk.Label(
            self.info_frame,
            text="",
            font=('Segoe UI', 9),
            bg='#1a1a1a',
            fg='#AAAAAA'
        )
        self.rarity_label.pack(anchor='w', pady=(0, 3))
        self.rarity_label.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Location
        self.location_label = tk.Label(
            self.info_frame,
            text="",
            font=('Segoe UI', 9),
            bg='#1a1a1a',
            fg='#AAAAAA'
        )
        self.location_label.pack(anchor='w', pady=(0, 10))
        self.location_label.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Price (big and prominent)
        self.price_label = tk.Label(
            self.info_frame,
            text="",
            font=('Segoe UI', 16, 'bold'),
            bg='#1a1a1a',
            fg='#00FF00'
        )
        self.price_label.pack(anchor='w')
        self.price_label.bind('<Button-1>', lambda e: self.toggle_mode())
        
        # Hotkey hints at bottom
        hint_label = tk.Label(
            main_frame,
            text="F6: Scan | F5: Region",
            font=('Segoe UI', 8),
            bg='#1a1a1a',
            fg='#666666'
        )
        hint_label.pack(side=tk.BOTTOM, anchor='w', pady=(10, 0))
        hint_label.bind('<Button-1>', lambda e: self.toggle_mode())
    
    def toggle_mode(self):
        """Toggle between compact and detailed mode"""
        self.compact_mode = not self.compact_mode
        self._create_ui()
        # Restore current item display
        if self.current_item:
            self.update_display(item=self.current_item, scanning=self.scanning)
    
    
    def update_display(self, item: Optional[Dict] = None, scanning: bool = None):
        """
        Update the overlay display
        
        Args:
            item: Item data dict with name, rarity, price, location
            scanning: Whether scanning is active
        """
        # Update scanning status
        if scanning is not None:
            self.scanning = scanning
        
        # Update item info
        if item is not None:
            self.current_item = item
        
        # Update based on mode
        if self.compact_mode:
            self._update_compact_display()
        else:
            self._update_detailed_display()
    
    def _update_compact_display(self):
        """Update compact mode display"""
        if self.current_item:
            # Get item info
            name = self.current_item.get('name', 'Unknown')
            price = self.current_item.get('price', 0)
            rarity = self.current_item.get('rarity', 'Common')
            color = self.RARITY_COLORS.get(rarity, '#FFFFFF')
            
            # Update name with color
            self.compact_name_label.config(text=name, fg=color)
            
            # Update price
            if price > 0:
                self.compact_price_label.config(
                    text=f"💰 {price:,}g",
                    fg='#FFD700'
                )
            else:
                self.compact_price_label.config(
                    text="Cannot sell",
                    fg='#FF4444'
                )
        else:
            # No item
            self.compact_name_label.config(
                text="Moonlighter 2 Prices",
                fg='#FFD700'
            )
            self.compact_price_label.config(
                text="F6: Scan | F5: Region",
                fg='#00FF00'
            )
    
    def _update_detailed_display(self):
        """Update detailed mode display"""
        # Update scanning status
        if hasattr(self, 'status_label'):
            if self.scanning:
                self.status_label.config(text="Status: SCANNING", fg='#00FF00')
            else:
                self.status_label.config(text="Status: OFF", fg='#FF4444')
        
        # Update item info
        if self.current_item:
            # Item name (color by rarity)
            rarity = self.current_item.get('rarity', 'Common')
            color = self.RARITY_COLORS.get(rarity, '#FFFFFF')
            self.item_name_label.config(
                text=self.current_item.get('name', 'Unknown'),
                fg=color
            )
            
            # Rarity
            self.rarity_label.config(
                text=f"Rarity: {rarity}",
                fg=color
            )
            
            # Location
            location = self.current_item.get('location', 'Unknown')
            self.location_label.config(text=f"Location: {location}")
            
            # Price
            price = self.current_item.get('price', 0)
            if price > 0:
                self.price_label.config(
                    text=f"💰 {price:,}g",
                    fg='#FFD700'
                )
            else:
                self.price_label.config(
                    text="Cannot be sold",
                    fg='#FF4444'
                )
        elif not self.scanning:
            # Clear display when not scanning
            self.item_name_label.config(text="Click để toggle", fg='#CCCCCC')
            self.rarity_label.config(text="")
            self.location_label.config(text="")
            self.price_label.config(text="")
        else:
            # Show waiting message when scanning but no item
            self.item_name_label.config(text="Waiting for item...", fg='#CCCCCC')
            self.rarity_label.config(text="")
            self.location_label.config(text="")
            self.price_label.config(text="")
    
    def run(self, update_callback):
        """
        Start the overlay window
        
        Args:
            update_callback: Function to call periodically for updates
        """
        def periodic_update():
            update_callback()
            self.root.after(100, periodic_update)  # Update every 100ms
        
        # Start periodic updates
        self.root.after(100, periodic_update)
        
        # Run the window
        self.root.mainloop()
    
    def close(self):
        """Close the overlay window"""
        self.root.destroy()


if __name__ == "__main__":
    # Test the overlay window
    def test_update():
        pass
    
    overlay = OverlayWindow()
    
    # Test with sample data after 2 seconds
    def show_sample():
        sample_item = {
            'name': 'Broken Battery',
            'rarity': 'Common',
            'price': 26,
            'location': 'The Gallery'
        }
        overlay.update_display(item=sample_item, scanning=True)
    
    overlay.root.after(2000, show_sample)
    overlay.run(test_update)
