"""
Font Manager Widget for CodeMaster Pro

Learning Notes:
- This module demonstrates font management in GUI applications
- Shows API integration for font services
- Implements font preview and selection interfaces
- Demonstrates typography and styling systems
"""

import customtkinter as ctk
import tkinter as tk
from typing import List, Dict, Any, Optional
import threading
from apis.fonts_api import FontsAPI
from utils.config import Config

class FontManagerWidget:
    """
    Font management widget with preview and selection features.
    
    This class provides:
    1. Font browsing and search
    2. Real-time font preview
    3. Coding font recommendations
    4. Font pairing suggestions
    5. Font installation and management
    6. Typography customization
    """
    
    def __init__(self, parent: ctk.CTkFrame, fonts_api: FontsAPI, config: Config):
        """Initialize the font manager widget."""
        
        self.parent = parent
        self.fonts_api = fonts_api
        self.config = config
        
        # Font data
        self.all_fonts = []
        self.coding_fonts = []
        self.current_fonts = []
        self.selected_font = None
        
        # Search and filter state
        self.search_query = ""
        self.current_category = "all"
        
        # Create the interface
        self.setup_layout()
        self.setup_header()
        self.setup_controls()
        self.setup_font_list()
        self.setup_preview()
        
        # Load fonts
        self.load_fonts()
        
        print("🔤 Font manager widget initialized")
    
    def setup_layout(self) -> None:
        """Set up the main layout for the font manager."""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, height=60)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 10))
        
        # Controls
        self.controls_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 10))
        
        # Font list (left side)
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=(5, 10), pady=5)
        self.list_frame.grid_rowconfigure(1, weight=1)
        
        # Preview area (right side)
        self.preview_frame = ctk.CTkFrame(self.main_frame)
        self.preview_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        self.preview_frame.grid_rowconfigure(2, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)
    
    def setup_header(self) -> None:
        """Set up the header section."""
        
        # Title
        title_label = ctk.CTkLabel(
            self.header_frame,
            text="🔤 Font Manager & Typography Studio",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="Loading fonts...",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="right", padx=20, pady=15)
    
    def setup_controls(self) -> None:
        """Set up the font search and filter controls."""
        
        # Search section
        search_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        search_frame.pack(side="left", fill="y", padx=15, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍 Search Fonts:")
        search_label.pack(anchor="w", pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by font name...",
            width=200
        )
        self.search_entry.pack(pady=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # Category filter
        category_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        category_frame.pack(side="left", fill="y", padx=15, pady=10)
        
        category_label = ctk.CTkLabel(category_frame, text="📂 Category:")
        category_label.pack(anchor="w", pady=(0, 5))
        
        self.category_var = tk.StringVar(value="all")
        self.category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=["all", "serif", "sans-serif", "monospace", "display", "handwriting", "coding"],
            variable=self.category_var,
            command=self.on_category_change,
            width=150
        )
        self.category_menu.pack()
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        button_frame.pack(side="right", fill="y", padx=15, pady=10)
        
        self.refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            width=100,
            command=self.refresh_fonts
        )
        self.refresh_btn.pack(side="right", padx=5)
        
        self.coding_fonts_btn = ctk.CTkButton(
            button_frame,
            text="⌨️ Coding Fonts",
            width=120,
            command=self.show_coding_fonts,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.coding_fonts_btn.pack(side="right", padx=5)
    
    def setup_font_list(self) -> None:
        """Set up the font list display."""
        
        # List title
        list_title = ctk.CTkLabel(
            self.list_frame,
            text="📋 Available Fonts",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Font list
        self.font_list = ctk.CTkScrollableFrame(self.list_frame, height=400)
        self.font_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Info section
        info_frame = ctk.CTkFrame(self.list_frame, height=80)
        info_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.font_count_label = ctk.CTkLabel(
            info_frame,
            text="Fonts: 0",
            font=ctk.CTkFont(size=12)
        )
        self.font_count_label.pack(pady=10)
        
        # System fonts section
        system_title = ctk.CTkLabel(
            self.list_frame,
            text="💻 System Fonts",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        system_title.grid(row=3, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.system_fonts_frame = ctk.CTkFrame(self.list_frame, height=100)
        self.system_fonts_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.show_system_fonts()
    
    def setup_preview(self) -> None:
        """Set up the font preview area."""
        
        # Preview title
        preview_title = ctk.CTkLabel(
            self.preview_frame,
            text="👁️ Font Preview",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        preview_title.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Font info
        self.font_info_frame = ctk.CTkFrame(self.preview_frame, height=100)
        self.font_info_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Selected font info
        self.selected_font_label = ctk.CTkLabel(
            self.font_info_frame,
            text="Select a font to preview",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.selected_font_label.pack(pady=10)
        
        self.font_details_label = ctk.CTkLabel(
            self.font_info_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.font_details_label.pack(pady=5)
        
        # Preview text
        self.preview_text = ctk.CTkTextbox(
            self.preview_frame,
            height=300,
            font=ctk.CTkFont(size=14)
        )
        self.preview_text.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Default preview text
        default_text = """The quick brown fox jumps over the lazy dog.
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
1234567890 !@#$%^&*()

# Python code sample
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

// JavaScript code sample
function calculateSum(a, b) {
    return a + b;
}

/* CSS code sample */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""

        self.preview_text.insert("1.0", default_text)
        
        # Preview controls
        preview_controls = ctk.CTkFrame(self.preview_frame, height=50)
        preview_controls.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Size control
        size_frame = ctk.CTkFrame(preview_controls, fg_color="transparent")
        size_frame.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(size_frame, text="Size:").pack(side="left", padx=(0, 5))
        
        self.size_var = tk.StringVar(value="14")
        size_menu = ctk.CTkOptionMenu(
            size_frame,
            values=["10", "12", "14", "16", "18", "20", "24", "28", "32"],
            variable=self.size_var,
            command=self.update_preview_size,
            width=80
        )
        size_menu.pack(side="left")
        
        # Apply button
        self.apply_btn = ctk.CTkButton(
            preview_controls,
            text="✅ Apply to Editor",
            command=self.apply_font_to_editor,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.apply_btn.pack(side="right", padx=10, pady=10)
        
        # Pairing button
        self.pairing_btn = ctk.CTkButton(
            preview_controls,
            text="🎨 Font Pairings",
            command=self.show_font_pairings
        )
        self.pairing_btn.pack(side="right", padx=5, pady=10)
    
    def load_fonts(self) -> None:
        """Load fonts in background thread."""
        
        def fetch_fonts():
            try:
                self.update_status("Loading font catalog...")
                
                # Load all fonts
                self.all_fonts = self.fonts_api.get_font_families()
                
                # Load coding fonts
                self.coding_fonts = self.fonts_api.get_coding_fonts()
                
                # Update UI on main thread
                self.parent.after(0, self.update_font_list)
                
            except Exception as e:
                self.parent.after(0, lambda: self.update_status(f"Error: {str(e)}"))
        
        # Start background thread
        threading.Thread(target=fetch_fonts, daemon=True).start()
    
    def update_font_list(self) -> None:
        """Update the font list display."""
        
        # Clear existing items
        for widget in self.font_list.winfo_children():
            widget.destroy()
        
        # Determine which fonts to show
        if self.current_category == "coding":
            fonts_to_show = self.coding_fonts
        elif self.current_category == "all":
            fonts_to_show = self.all_fonts
        else:
            fonts_to_show = [f for f in self.all_fonts if f.get('category') == self.current_category]
        
        # Apply search filter
        if self.search_query:
            fonts_to_show = [
                f for f in fonts_to_show 
                if self.search_query.lower() in f.get('family', '').lower()
            ]
        
        self.current_fonts = fonts_to_show
        
        # Create font items
        for font in fonts_to_show[:50]:  # Limit to 50 for performance
            self.create_font_item(font)
        
        # Update count
        self.font_count_label.configure(text=f"Fonts: {len(fonts_to_show)}")
        
        # Update status
        if len(fonts_to_show) > 50:
            self.update_status(f"Showing first 50 of {len(fonts_to_show)} fonts")
        else:
            self.update_status(f"Loaded {len(fonts_to_show)} fonts")
    
    def create_font_item(self, font: Dict[str, Any]) -> None:
        """Create a font item in the list."""
        
        # Font item frame
        item_frame = ctk.CTkFrame(self.font_list)
        item_frame.pack(fill="x", pady=2, padx=5)
        
        # Font info frame
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Font name
        name_label = ctk.CTkLabel(
            info_frame,
            text=font.get('family', 'Unknown'),
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Font category and info
        category = font.get('category', 'unknown')
        variants = len(font.get('variants', []))
        info_text = f"Category: {category} • Variants: {variants}"
        
        # Add coding indicator
        if font.get('recommended_for_coding', False):
            info_text += " • ⌨️ Coding"
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        info_label.pack(anchor="w")
        
        # Preview button
        preview_btn = ctk.CTkButton(
            item_frame,
            text="👁️",
            width=40,
            command=lambda f=font: self.preview_font(f)
        )
        preview_btn.pack(side="right", padx=10, pady=5)
    
    def show_system_fonts(self) -> None:
        """Display available system fonts."""
        
        system_fonts = self.fonts_api.get_system_fonts()
        
        for font in system_fonts:
            if font.get('suitable_for_coding', False):
                font_btn = ctk.CTkButton(
                    self.system_fonts_frame,
                    text=f"⌨️ {font['family']}",
                    width=180,
                    height=25,
                    command=lambda f=font: self.preview_system_font(f)
                )
                font_btn.pack(pady=1, padx=5)
    
    def preview_font(self, font: Dict[str, Any]) -> None:
        """Preview a selected font."""
        
        self.selected_font = font
        
        # Update font info
        family = font.get('family', 'Unknown')
        category = font.get('category', 'unknown')
        variants = ', '.join(font.get('variants', []))
        
        self.selected_font_label.configure(text=family)
        self.font_details_label.configure(text=f"Category: {category}\nVariants: {variants}")
        
        # Update preview (this would normally load the actual font)
        self.update_status(f"Previewing: {family}")
        
        # Note: Actual font loading would require downloading and installing the font
        # For demo purposes, we'll just show the selection
    
    def preview_system_font(self, font: Dict[str, Any]) -> None:
        """Preview a system font."""
        
        self.selected_font = font
        family = font['family']
        
        self.selected_font_label.configure(text=family)
        self.font_details_label.configure(text=f"System font • Category: {font['category']}")
        
        # Try to apply the system font
        try:
            new_font = ctk.CTkFont(family=family, size=int(self.size_var.get()))
            self.preview_text.configure(font=new_font)
            self.update_status(f"Applied system font: {family}")
        except Exception as e:
            self.update_status(f"Could not apply font: {family}")
    
    def update_preview_size(self, size: str) -> None:
        """Update preview text size."""
        
        try:
            if self.selected_font and 'family' in self.selected_font:
                family = self.selected_font['family']
                new_font = ctk.CTkFont(family=family, size=int(size))
                self.preview_text.configure(font=new_font)
        except:
            # Use default font with new size
            new_font = ctk.CTkFont(size=int(size))
            self.preview_text.configure(font=new_font)
    
    def apply_font_to_editor(self) -> None:
        """Apply selected font to the code editor."""
        
        if not self.selected_font:
            self.update_status("No font selected")
            return
        
        family = self.selected_font.get('family', 'Consolas')
        size = int(self.size_var.get())
        
        # Save to config
        self.config.set('preferred_font_family', family)
        self.config.set('font_size', size)
        self.config.save()
        
        self.update_status(f"Applied {family} ({size}pt) to editor settings")
    
    def show_font_pairings(self) -> None:
        """Show font pairing suggestions."""
        
        if not self.selected_font:
            self.update_status("Select a font first to see pairings")
            return
        
        # This would show font pairing suggestions
        self.update_status("Font pairing suggestions feature coming soon!")
    
    def show_coding_fonts(self) -> None:
        """Show only coding-friendly fonts."""
        
        self.current_category = "coding"
        self.category_var.set("coding")
        self.update_font_list()
    
    def refresh_fonts(self) -> None:
        """Refresh the font list."""
        self.load_fonts()
    
    def on_search_change(self, event=None) -> None:
        """Handle search query changes."""
        
        self.search_query = self.search_entry.get()
        self.update_font_list()
    
    def on_category_change(self, category: str) -> None:
        """Handle category filter changes."""
        
        self.current_category = category
        self.update_font_list()
    
    def update_status(self, message: str) -> None:
        """Update status message."""
        
        self.status_label.configure(text=message)
        print(f"Font Manager: {message}")
        
        # Clear status after 5 seconds
        self.parent.after(5000, lambda: self.status_label.configure(text="Ready")) 