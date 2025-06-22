"""
Main Window for CodeMaster Pro

Learning Notes:
- This module demonstrates modern GUI design with CustomTkinter
- Shows component integration and layout management
- Implements tabbed interface for feature organization
- Demonstrates event handling and user interaction
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from typing import Dict, Any, Optional
from pathlib import Path

from gui.sql_tutor import SQLTutorWidget
from gui.weather_widget import WeatherWidget
from gui.code_editor import CodeEditorWidget
from gui.font_manager import FontManagerWidget
from apis.weather_api import WeatherAPI
from apis.fonts_api import FontsAPI
from database.sql_engine import SQLEngine
from utils.config import Config

class MainWindow:
    """
    Main application window with integrated development tools.
    
    This class provides:
    1. Tabbed interface for different features
    2. SQL learning environment
    3. Weather integration for development planning
    4. Font management and styling
    5. Code editing with AI assistance
    6. Project management
    """
    
    def __init__(self, root: ctk.CTk, db_engine: SQLEngine, config: Config):
        """Initialize the main window with all components."""
        
        self.root = root
        self.db_engine = db_engine
        self.config = config
        
        # Initialize API services
        self.weather_api = WeatherAPI(config)
        self.fonts_api = FontsAPI(config)
        
        # Create the main interface
        self.setup_main_layout()
        self.create_menu_bar()
        self.setup_status_bar()
        
        # Initialize components
        self.setup_components()
        
        print("🎨 Main window initialized successfully")
    
    def setup_main_layout(self) -> None:
        """
        Set up the main window layout structure.
        
        Learning Notes:
        - GUI layout management with frames
        - Responsive design principles
        - Component organization and hierarchy
        """
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Header frame
        self.header_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Main content area with tabbed interface
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create tabbed interface
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Add tabs
        self.setup_tabs()
        
        # Status bar frame
        self.status_frame = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
    
    def setup_tabs(self) -> None:
        """
        Create and configure tabs for different features.
        
        Learning Notes:
        - Tab management in GUI applications
        - Feature organization and user experience
        - Component lifecycle management
        """
        
        # SQL Learning Tab
        self.sql_tab = self.tab_view.add("SQL Learning")
        
        # Code Editor Tab
        self.editor_tab = self.tab_view.add("Code Editor")
        
        # Weather & Productivity Tab
        self.weather_tab = self.tab_view.add("Weather & Productivity")
        
        # Font & Styling Tab
        self.fonts_tab = self.tab_view.add("Fonts & Styling")
        
        # AI Agents Tab
        self.ai_tab = self.tab_view.add("AI Agents")
        
        # Project Management Tab
        self.projects_tab = self.tab_view.add("Projects")
        
        # Settings Tab
        self.settings_tab = self.tab_view.add("Settings")
    
    def create_menu_bar(self) -> None:
        """
        Create the application menu bar.
        
        Learning Notes:
        - Menu system implementation
        - Keyboard shortcuts and accessibility
        - User interface standards
        """
        
        # Application title and logo
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🚀 CodeMaster Pro",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Quick access buttons
        self.quick_buttons_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.quick_buttons_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # New Project button
        self.new_project_btn = ctk.CTkButton(
            self.quick_buttons_frame,
            text="New Project",
            width=100,
            command=self.new_project
        )
        self.new_project_btn.pack(side="left", padx=5)
        
        # Open Project button
        self.open_project_btn = ctk.CTkButton(
            self.quick_buttons_frame,
            text="Open Project",
            width=100,
            command=self.open_project
        )
        self.open_project_btn.pack(side="left", padx=5)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            self.quick_buttons_frame,
            text="⚙️ Settings",
            width=100,
            command=self.show_settings
        )
        self.settings_btn.pack(side="left", padx=5)
    
    def setup_status_bar(self) -> None:
        """
        Set up the status bar with real-time information.
        
        Learning Notes:
        - Status display and real-time updates
        - Threading for non-blocking operations
        - User feedback and system monitoring
        """
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready | Welcome to CodeMaster Pro!",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Weather info (right side)
        self.weather_status_label = ctk.CTkLabel(
            self.status_frame,
            text="Loading weather...",
            font=ctk.CTkFont(size=12)
        )
        self.weather_status_label.pack(side="right", padx=10, pady=5)
        
        # Start background updates
        self.start_background_updates()
    
    def setup_components(self) -> None:
        """
        Initialize all component widgets.
        
        Learning Notes:
        - Component instantiation and configuration
        - Dependency injection patterns
        - Error handling for component initialization
        """
        
        try:
            # SQL Tutorial Widget
            self.sql_tutor = SQLTutorWidget(self.sql_tab, self.db_engine, self.config)
            
            # Weather Widget
            self.weather_widget = WeatherWidget(self.weather_tab, self.weather_api, self.config)
            
            # Code Editor Widget
            self.code_editor = CodeEditorWidget(self.editor_tab, self.config)
            
            # Font Manager Widget
            self.font_manager = FontManagerWidget(self.fonts_tab, self.fonts_api, self.config)
            
            # AI Agents Interface
            self.setup_ai_interface()
            
            # Project Management Interface
            self.setup_project_interface()
            
            # Settings Interface
            self.setup_settings_interface()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize components: {e}")
    
    def setup_ai_interface(self) -> None:
        """
        Set up the AI agents interface.
        
        Learning Notes:
        - AI integration in desktop applications
        - Chat-like interfaces for AI interaction
        - Asynchronous processing for AI operations
        """
        
        # AI Chat Frame
        ai_main_frame = ctk.CTkFrame(self.ai_tab)
        ai_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # AI Title
        ai_title = ctk.CTkLabel(
            ai_main_frame,
            text="🤖 AI Development Assistant",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        ai_title.pack(pady=(10, 20))
        
        # AI Features Description
        ai_description = ctk.CTkTextbox(ai_main_frame, height=100)
        ai_description.pack(fill="x", padx=20, pady=(0, 20))
        ai_description.insert("1.0", """
AI Features Available:

• Code Analysis: Get insights about your code quality and structure
• Documentation Generator: Automatically generate documentation for your projects
• Code Suggestions: Receive intelligent suggestions for improvements
• Bug Detection: Identify potential issues in your codebase
• Architecture Advice: Get recommendations for better software architecture

Note: Add your OpenAI or Anthropic API key in the .env file to enable AI features.
        """)
        ai_description.configure(state="disabled")
        
        # AI Input Frame
        ai_input_frame = ctk.CTkFrame(ai_main_frame, fg_color="transparent")
        ai_input_frame.pack(fill="x", padx=20, pady=10)
        
        # AI Input
        self.ai_input = ctk.CTkEntry(
            ai_input_frame,
            placeholder_text="Ask the AI assistant anything about your code...",
            height=40
        )
        self.ai_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # AI Submit Button
        self.ai_submit_btn = ctk.CTkButton(
            ai_input_frame,
            text="Ask AI",
            width=100,
            command=self.ask_ai_assistant
        )
        self.ai_submit_btn.pack(side="right")
        
        # AI Response Area
        self.ai_response = ctk.CTkTextbox(ai_main_frame, height=300)
        self.ai_response.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bind Enter key to submit
        self.ai_input.bind("<Return>", lambda e: self.ask_ai_assistant())
    
    def setup_project_interface(self) -> None:
        """
        Set up the project management interface.
        
        Learning Notes:
        - File system operations in GUI
        - Project organization and management
        - Git integration concepts
        """
        
        # Project Management Frame
        project_main_frame = ctk.CTkFrame(self.projects_tab)
        project_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Project Title
        project_title = ctk.CTkLabel(
            project_main_frame,
            text="📁 Project Management",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        project_title.pack(pady=(10, 20))
        
        # Project Actions Frame
        actions_frame = ctk.CTkFrame(project_main_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        # Recent Projects
        recent_label = ctk.CTkLabel(actions_frame, text="Recent Projects:")
        recent_label.pack(anchor="w", pady=(0, 10))
        
        # Recent Projects List
        self.recent_projects_list = ctk.CTkScrollableFrame(actions_frame, height=200)
        self.recent_projects_list.pack(fill="x", pady=(0, 20))
        
        # Load recent projects
        self.load_recent_projects()
        
        # Project Info
        info_text = ctk.CTkTextbox(project_main_frame, height=200)
        info_text.pack(fill="x", padx=20, pady=20)
        info_text.insert("1.0", """
Project Management Features:

• Create New Projects: Initialize new development projects with proper structure
• Open Existing Projects: Load and manage existing codebases
• Git Integration: Version control operations and repository management
• Code Statistics: Analyze your project metrics and progress
• Backup Management: Automated backup and restore functionality
• Dependency Tracking: Monitor and manage project dependencies

Click 'New Project' or 'Open Project' in the header to get started!
        """)
        info_text.configure(state="disabled")
    
    def setup_settings_interface(self) -> None:
        """
        Set up the settings configuration interface.
        
        Learning Notes:
        - Configuration management in GUI
        - User preference handling
        - Settings persistence and validation
        """
        
        # Settings Frame
        settings_main_frame = ctk.CTkFrame(self.settings_tab)
        settings_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Settings Title
        settings_title = ctk.CTkLabel(
            settings_main_frame,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        settings_title.pack(pady=(10, 20))
        
        # Scrollable Settings Frame
        settings_scroll = ctk.CTkScrollableFrame(settings_main_frame)
        settings_scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Appearance Settings
        appearance_frame = ctk.CTkFrame(settings_scroll)
        appearance_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(appearance_frame, text="Appearance", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Theme Selection
        theme_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left", padx=(0, 10))
        self.theme_var = tk.StringVar(value=self.config.get('appearance_mode', 'dark'))
        theme_menu = ctk.CTkOptionMenu(theme_frame, values=["light", "dark", "system"], variable=self.theme_var, command=self.change_theme)
        theme_menu.pack(side="left")
        
        # Color Theme Selection
        color_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        color_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(color_frame, text="Color Theme:").pack(side="left", padx=(0, 10))
        self.color_var = tk.StringVar(value=self.config.get('color_theme', 'blue'))
        color_menu = ctk.CTkOptionMenu(color_frame, values=["blue", "green", "dark-blue"], variable=self.color_var, command=self.change_color_theme)
        color_menu.pack(side="left")
        
        # API Settings
        api_frame = ctk.CTkFrame(settings_scroll)
        api_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(api_frame, text="API Configuration", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        api_info = ctk.CTkTextbox(api_frame, height=150)
        api_info.pack(fill="x", padx=20, pady=20)
        api_info.insert("1.0", """
To enable full functionality, add your API keys to the .env file:

OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
WEATHER_API_KEY=your_openweathermap_key_here
GOOGLE_FONTS_API_KEY=your_google_fonts_key_here

These are all free APIs with generous usage limits for learning and development.
        """)
        api_info.configure(state="disabled")
        
        # Save Settings Button
        save_btn = ctk.CTkButton(
            settings_main_frame,
            text="Save Settings",
            command=self.save_settings
        )
        save_btn.pack(pady=20)
    
    def start_background_updates(self) -> None:
        """
        Start background threads for real-time updates.
        
        Learning Notes:
        - Threading in GUI applications
        - Non-blocking operations
        - Real-time data updates
        """
        
        def update_weather_status():
            try:
                weather_data = self.weather_api.get_current_weather()
                temp = weather_data.get('temperature', 'N/A')
                condition = weather_data.get('condition', 'Unknown')
                self.weather_status_label.configure(text=f"🌤️ {temp}°C, {condition}")
            except Exception as e:
                self.weather_status_label.configure(text="🌤️ Weather unavailable")
        
        # Update weather in background
        threading.Thread(target=update_weather_status, daemon=True).start()
    
    def new_project(self) -> None:
        """Create a new project."""
        messagebox.showinfo("New Project", "New project creation will be implemented here!")
    
    def open_project(self) -> None:
        """Open an existing project."""
        project_path = filedialog.askdirectory(title="Select Project Directory")
        if project_path:
            self.config.add_recent_project(project_path)
            self.load_recent_projects()
            messagebox.showinfo("Project Opened", f"Opened project: {project_path}")
    
    def show_settings(self) -> None:
        """Switch to settings tab."""
        self.tab_view.set("Settings")
    
    def ask_ai_assistant(self) -> None:
        """Handle AI assistant queries."""
        query = self.ai_input.get().strip()
        if not query:
            return
        
        self.ai_input.delete(0, "end")
        self.ai_response.insert("end", f"\n🧑 You: {query}\n")
        self.ai_response.insert("end", "🤖 AI: AI features require API key configuration. Please add your OpenAI or Anthropic API key to the .env file to enable AI assistance.\n")
        self.ai_response.see("end")
    
    def load_recent_projects(self) -> None:
        """Load and display recent projects."""
        # Clear existing items
        for widget in self.recent_projects_list.winfo_children():
            widget.destroy()
        
        recent_projects = self.config.get('recent_projects', [])
        if not recent_projects:
            no_projects_label = ctk.CTkLabel(self.recent_projects_list, text="No recent projects")
            no_projects_label.pack(pady=10)
        else:
            for project_path in recent_projects[:5]:  # Show last 5 projects
                project_frame = ctk.CTkFrame(self.recent_projects_list)
                project_frame.pack(fill="x", pady=5)
                
                project_label = ctk.CTkLabel(project_frame, text=Path(project_path).name)
                project_label.pack(side="left", padx=10, pady=5)
                
                path_label = ctk.CTkLabel(project_frame, text=str(project_path), text_color="gray")
                path_label.pack(side="left", padx=10, pady=5)
    
    def change_theme(self, theme: str) -> None:
        """Change application theme."""
        ctk.set_appearance_mode(theme)
        self.config.set('appearance_mode', theme)
        self.update_status("Theme changed to " + theme)
    
    def change_color_theme(self, color: str) -> None:
        """Change color theme."""
        ctk.set_default_color_theme(color)
        self.config.set('color_theme', color)
        self.update_status("Color theme changed to " + color + " (restart required)")
    
    def save_settings(self) -> None:
        """Save current settings."""
        self.config.save()
        self.update_status("Settings saved successfully")
    
    def update_status(self, message: str) -> None:
        """Update status bar message."""
        self.status_label.configure(text=message)
        # Clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.configure(text="Ready")) 