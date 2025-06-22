#!/usr/bin/env python3
"""
CodeMaster Pro - AI-Powered Development Environment
Main application entry point

This file demonstrates:
1. Application initialization and setup
2. GUI framework integration (CustomTkinter)
3. Component orchestration
4. Cross-platform compatibility
"""

import tkinter as tk
import customtkinter as ctk
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project directories to Python path for imports
sys.path.append(str(Path(__file__).parent))

from gui.main_window import MainWindow
from utils.config import Config
from database.sql_engine import SQLEngine
from utils.helpers import setup_logging

class CodeMasterApp:
    """
    Main application class that orchestrates all components.
    
    Learning Notes:
    - This class follows the Singleton pattern for application management
    - It demonstrates proper resource initialization and cleanup
    - Shows how to integrate multiple subsystems in a desktop app
    """
    
    def __init__(self):
        """Initialize the application with all required components."""
        
        # Set up logging for debugging and learning
        setup_logging()
        
        # Load environment variables for API keys
        load_dotenv()
        
        # Initialize configuration
        self.config = Config()
        
        # Set appearance mode and color theme for modern UI
        ctk.set_appearance_mode(self.config.get('appearance_mode', 'dark'))
        ctk.set_default_color_theme(self.config.get('color_theme', 'blue'))
        
        # Initialize database engine
        self.db_engine = SQLEngine()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("CodeMaster Pro - AI Development Environment")
        self.root.geometry("1400x900")
        
        # Center window on screen
        self.center_window()
        
        # Initialize main window with all components
        self.main_window = MainWindow(self.root, self.db_engine, self.config)
        
        # Set up proper cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center the application window on the screen."""
        self.root.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width // 2) - (1400 // 2)
        y = (screen_height // 2) - (900 // 2)
        
        self.root.geometry(f"1400x900+{x}+{y}")
        
    def on_closing(self):
        """Handle application shutdown gracefully."""
        try:
            # Save configuration
            self.config.save()
            
            # Close database connections
            self.db_engine.close()
            
            # Destroy the window
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.destroy()
    
    def run(self):
        """Start the application main loop."""
        try:
            # Show splash screen or welcome message
            print("🚀 Starting CodeMaster Pro...")
            print("📚 Educational AI Development Environment")
            print("💡 Check the SQL Tutorial tab to start learning!")
            
            # Start the GUI main loop
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\n👋 Application closed by user")
        except Exception as e:
            print(f"❌ Application error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """
    Application entry point.
    
    Learning Notes:
    - This function demonstrates proper application structure
    - Error handling for production applications
    - Resource management and cleanup
    """
    
    # Check Python version compatibility
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Create and run the application
    try:
        app = CodeMasterApp()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 