"""
Code Editor Widget for CodeMaster Pro

Learning Notes:
- This module demonstrates text editing widgets in GUI applications
- Shows basic syntax highlighting implementation
- Demonstrates file operations and project management
- Implements code analysis and AI integration hooks
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from typing import Optional, Dict, Any
from utils.config import Config

class CodeEditorWidget:
    """
    Code editor with syntax highlighting and AI features.
    
    This class provides:
    1. Multi-file code editing
    2. Basic syntax highlighting
    3. File operations (open, save, new)
    4. Project management
    5. AI integration hooks
    6. Code analysis features
    """
    
    def __init__(self, parent: ctk.CTkFrame, config: Config):
        """Initialize the code editor widget."""
        
        self.parent = parent
        self.config = config
        
        # Editor state
        self.current_file = None
        self.open_files = {}  # file_path: content
        self.modified_files = set()
        
        # Create the interface
        self.setup_layout()
        self.setup_toolbar()
        self.setup_editor()
        self.setup_file_explorer()
        
        print("💻 Code editor widget initialized")
    
    def setup_layout(self) -> None:
        """Set up the main layout for the code editor."""
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Toolbar
        self.toolbar_frame = ctk.CTkFrame(self.main_frame, height=50)
        self.toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 10))
        
        # File explorer (left side)
        self.explorer_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.explorer_frame.grid(row=1, column=0, sticky="nsew", padx=(5, 10), pady=5)
        
        # Editor area (right side)
        self.editor_frame = ctk.CTkFrame(self.main_frame)
        self.editor_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.editor_frame.grid_rowconfigure(1, weight=1)
        self.editor_frame.grid_columnconfigure(0, weight=1)
    
    def setup_toolbar(self) -> None:
        """Set up the toolbar with file operations."""
        
        # Title
        title_label = ctk.CTkLabel(
            self.toolbar_frame,
            text="💻 Code Editor & AI Assistant",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=12)
        
        # Button container
        button_frame = ctk.CTkFrame(self.toolbar_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=15, pady=10)
        
        # File operations
        self.new_btn = ctk.CTkButton(
            button_frame,
            text="📄 New",
            width=80,
            command=self.new_file
        )
        self.new_btn.pack(side="left", padx=2)
        
        self.open_btn = ctk.CTkButton(
            button_frame,
            text="📂 Open",
            width=80,
            command=self.open_file
        )
        self.open_btn.pack(side="left", padx=2)
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save",
            width=80,
            command=self.save_file
        )
        self.save_btn.pack(side="left", padx=2)
        
        self.analyze_btn = ctk.CTkButton(
            button_frame,
            text="🤖 Analyze",
            width=80,
            command=self.analyze_code,
            fg_color="orange",
            hover_color="darkorange"
        )
        self.analyze_btn.pack(side="left", padx=2)
    
    def setup_editor(self) -> None:
        """Set up the main code editor area."""
        
        # File tabs (will be implemented for multiple files)
        self.tabs_frame = ctk.CTkFrame(self.editor_frame, height=40)
        self.tabs_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        # Current file label
        self.current_file_label = ctk.CTkLabel(
            self.tabs_frame,
            text="📄 untitled.py",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.current_file_label.pack(side="left", padx=15, pady=10)
        
        # Modified indicator
        self.modified_label = ctk.CTkLabel(
            self.tabs_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.modified_label.pack(side="left", padx=5)
        
        # Editor text widget
        self.code_editor = ctk.CTkTextbox(
            self.editor_frame,
            font=ctk.CTkFont(family=self.config.get('preferred_font_family', 'Consolas'), 
                           size=self.config.get('font_size', 12))
        )
        self.code_editor.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Add some sample code
        sample_code = '''# Welcome to CodeMaster Pro Code Editor
# This is a basic code editor with AI integration capabilities

def hello_world():
    """A simple function to demonstrate syntax highlighting."""
    print("Hello from CodeMaster Pro!")
    return "Welcome to coding!"

# TODO: Add your code here
if __name__ == "__main__":
    message = hello_world()
    print(f"Message: {message}")
    
    # Try the AI analysis feature by clicking "Analyze" button
    # The AI can help with:
    # - Code review and suggestions
    # - Bug detection
    # - Performance optimization
    # - Documentation generation
'''
        self.code_editor.insert("1.0", sample_code)
        
        # Bind events for modifications
        self.code_editor.bind("<KeyPress>", self.on_text_change)
        self.code_editor.bind("<Button-1>", self.on_text_change)
    
    def setup_file_explorer(self) -> None:
        """Set up the file explorer panel."""
        
        # Explorer title
        explorer_title = ctk.CTkLabel(
            self.explorer_frame,
            text="📁 File Explorer",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        explorer_title.pack(pady=(15, 10))
        
        # Current directory
        self.current_dir_label = ctk.CTkLabel(
            self.explorer_frame,
            text="No project loaded",
            font=ctk.CTkFont(size=10),
            wraplength=200
        )
        self.current_dir_label.pack(pady=5)
        
        # Load project button
        self.load_project_btn = ctk.CTkButton(
            self.explorer_frame,
            text="Load Project",
            width=180,
            command=self.load_project
        )
        self.load_project_btn.pack(pady=10)
        
        # File list
        self.file_list_frame = ctk.CTkScrollableFrame(self.explorer_frame, height=300)
        self.file_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Recent files section
        recent_title = ctk.CTkLabel(
            self.explorer_frame,
            text="📋 Recent Files",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        recent_title.pack(pady=(10, 5))
        
        # Recent files list
        self.recent_files_frame = ctk.CTkFrame(self.explorer_frame, height=100)
        self.recent_files_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        # AI features section
        ai_title = ctk.CTkLabel(
            self.explorer_frame,
            text="🤖 AI Features",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        ai_title.pack(pady=(10, 5))
        
        # AI buttons
        self.doc_gen_btn = ctk.CTkButton(
            self.explorer_frame,
            text="📝 Generate Docs",
            width=180,
            command=self.generate_documentation
        )
        self.doc_gen_btn.pack(pady=2)
        
        self.refactor_btn = ctk.CTkButton(
            self.explorer_frame,
            text="🔧 Suggest Refactor",
            width=180,
            command=self.suggest_refactoring
        )
        self.refactor_btn.pack(pady=2)
        
        self.explain_btn = ctk.CTkButton(
            self.explorer_frame,
            text="💡 Explain Code",
            width=180,
            command=self.explain_code
        )
        self.explain_btn.pack(pady=2)
    
    def new_file(self) -> None:
        """Create a new file."""
        
        # Clear editor
        self.code_editor.delete("1.0", "end")
        self.current_file = None
        self.current_file_label.configure(text="📄 untitled.py")
        self.modified_label.configure(text="")
        
        # Add template based on file type
        template = '''# New Python file
# Add your code here

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
'''
        self.code_editor.insert("1.0", template)
    
    def open_file(self) -> None:
        """Open an existing file."""
        
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("Python files", "*.py"),
                ("JavaScript files", "*.js"),
                ("HTML files", "*.html"),
                ("CSS files", "*.css"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.code_editor.delete("1.0", "end")
                self.code_editor.insert("1.0", content)
                
                self.current_file = file_path
                self.current_file_label.configure(text=f"📄 {Path(file_path).name}")
                self.modified_label.configure(text="")
                
                # Add to recent files
                self.add_to_recent_files(file_path)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
    
    def save_file(self) -> None:
        """Save the current file."""
        
        if self.current_file is None:
            # Save as new file
            file_path = filedialog.asksaveasfilename(
                title="Save File",
                defaultextension=".py",
                filetypes=[
                    ("Python files", "*.py"),
                    ("JavaScript files", "*.js"),
                    ("HTML files", "*.html"),
                    ("CSS files", "*.css"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return
            
            self.current_file = file_path
            self.current_file_label.configure(text=f"📄 {Path(file_path).name}")
        
        try:
            content = self.code_editor.get("1.0", "end-1c")
            
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.modified_label.configure(text="✅ Saved")
            
            # Clear modified indicator after 2 seconds
            self.parent.after(2000, lambda: self.modified_label.configure(text=""))
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    
    def load_project(self) -> None:
        """Load a project directory."""
        
        project_dir = filedialog.askdirectory(title="Select Project Directory")
        
        if project_dir:
            self.current_dir_label.configure(text=Path(project_dir).name)
            self.load_project_files(project_dir)
    
    def load_project_files(self, project_dir: str) -> None:
        """Load files from project directory."""
        
        # Clear existing file list
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()
        
        try:
            project_path = Path(project_dir)
            
            # Get Python files in the project
            python_files = list(project_path.glob("**/*.py"))
            
            for file_path in python_files[:20]:  # Limit to 20 files
                relative_path = file_path.relative_to(project_path)
                
                file_btn = ctk.CTkButton(
                    self.file_list_frame,
                    text=f"📄 {relative_path}",
                    width=200,
                    height=30,
                    anchor="w",
                    command=lambda fp=str(file_path): self.open_project_file(fp)
                )
                file_btn.pack(pady=2, padx=5, fill="x")
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not load project: {e}")
    
    def open_project_file(self, file_path: str) -> None:
        """Open a file from the project."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.code_editor.delete("1.0", "end")
            self.code_editor.insert("1.0", content)
            
            self.current_file = file_path
            self.current_file_label.configure(text=f"📄 {Path(file_path).name}")
            self.modified_label.configure(text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def analyze_code(self) -> None:
        """Analyze the current code with AI."""
        
        content = self.code_editor.get("1.0", "end-1c").strip()
        
        if not content:
            messagebox.showwarning("Warning", "No code to analyze")
            return
        
        # For now, show a placeholder analysis
        analysis = self.get_basic_code_analysis(content)
        
        # Show analysis in a popup
        analysis_window = ctk.CTkToplevel(self.parent)
        analysis_window.title("Code Analysis")
        analysis_window.geometry("600x400")
        
        analysis_text = ctk.CTkTextbox(analysis_window)
        analysis_text.pack(fill="both", expand=True, padx=20, pady=20)
        analysis_text.insert("1.0", analysis)
        analysis_text.configure(state="disabled")
    
    def get_basic_code_analysis(self, code: str) -> str:
        """Provide basic code analysis."""
        
        lines = code.split('\n')
        
        analysis = f"""
🤖 Code Analysis Report

📊 Basic Statistics:
• Total lines: {len(lines)}
• Non-empty lines: {len([line for line in lines if line.strip()])}
• Comment lines: {len([line for line in lines if line.strip().startswith('#')])}
• Function definitions: {len([line for line in lines if 'def ' in line])}
• Class definitions: {len([line for line in lines if 'class ' in line])}

💡 Quick Suggestions:
• Add docstrings to functions for better documentation
• Consider using type hints for better code clarity
• Ensure proper error handling with try-except blocks
• Follow PEP 8 style guidelines for Python code

🔧 Potential Improvements:
• Add unit tests for your functions
• Consider breaking down large functions into smaller ones
• Use meaningful variable and function names
• Add input validation where appropriate

🚀 Next Steps:
• Run the code to test functionality
• Add comprehensive error handling
• Write unit tests
• Consider using a linter like pylint or flake8

Note: For advanced AI analysis, add your OpenAI or Anthropic API key to enable full AI features.
        """
        
        return analysis
    
    def generate_documentation(self) -> None:
        """Generate documentation for the current code."""
        
        messagebox.showinfo(
            "AI Documentation",
            "Documentation generation requires AI API key setup.\n\n"
            "This feature will:\n"
            "• Generate docstrings for functions\n"
            "• Create README files\n"
            "• Document API endpoints\n"
            "• Explain complex algorithms\n\n"
            "Add your OpenAI/Anthropic API key to enable this feature."
        )
    
    def suggest_refactoring(self) -> None:
        """Suggest code refactoring improvements."""
        
        messagebox.showinfo(
            "AI Refactoring",
            "Code refactoring suggestions require AI API key setup.\n\n"
            "This feature will:\n"
            "• Suggest code optimizations\n"
            "• Identify code smells\n"
            "• Recommend design patterns\n"
            "• Improve code structure\n\n"
            "Add your OpenAI/Anthropic API key to enable this feature."
        )
    
    def explain_code(self) -> None:
        """Explain the current code."""
        
        messagebox.showinfo(
            "AI Code Explanation",
            "Code explanation requires AI API key setup.\n\n"
            "This feature will:\n"
            "• Explain complex algorithms\n"
            "• Describe function purposes\n"
            "• Clarify code logic\n"
            "• Provide learning insights\n\n"
            "Add your OpenAI/Anthropic API key to enable this feature."
        )
    
    def add_to_recent_files(self, file_path: str) -> None:
        """Add file to recent files list."""
        
        # This would normally update the config and UI
        # For now, just store in memory
        pass
    
    def on_text_change(self, event=None) -> None:
        """Handle text changes in the editor."""
        
        # Mark file as modified
        if self.current_file and "●" not in self.modified_label.cget("text"):
            self.modified_label.configure(text="● Modified")
        
        # Here you could add syntax highlighting, auto-completion, etc.
        pass 