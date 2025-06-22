"""
SQL Tutorial Widget for CodeMaster Pro

Learning Notes:
- This module demonstrates interactive educational interfaces
- Shows SQL query execution and result display
- Implements progressive learning with tutorials and exercises
- Demonstrates syntax highlighting and code formatting
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, List, Optional
import re
from database.sql_engine import SQLEngine
from utils.config import Config

class SQLTutorWidget:
    """
    Interactive SQL learning widget with tutorials and exercises.
    
    This class provides:
    1. Progressive SQL tutorials from basic to advanced
    2. Interactive query editor with syntax highlighting
    3. Real-time query execution and results display
    4. Learning progress tracking
    5. Example database with realistic data
    6. SQL best practices and explanations
    """
    
    def __init__(self, parent: ctk.CTkFrame, db_engine: SQLEngine, config: Config):
        """Initialize the SQL tutorial widget."""
        
        self.parent = parent
        self.db_engine = db_engine
        self.config = config
        
        # Current tutorial state
        self.current_tutorial = 0
        self.current_lesson = 0
        
        # Get tutorials from database engine
        self.tutorials = self.db_engine.get_sql_tutorials()
        
        # Create the interface
        self.setup_layout()
        self.setup_tutorial_content()
        self.setup_query_interface()
        self.setup_results_display()
        
        # Load first tutorial
        self.load_tutorial(0)
        
        print("📚 SQL Tutorial widget initialized")
    
    def setup_layout(self) -> None:
        """
        Set up the main layout for the SQL tutorial.
        
        Learning Notes:
        - Complex GUI layout with multiple panels
        - Resizable components for better usability
        - Organized information hierarchy
        """
        
        # Main container with padding
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights for responsive design
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Title section
        self.title_frame = ctk.CTkFrame(self.main_frame, height=60)
        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 10))
        self.title_frame.grid_columnconfigure(1, weight=1)
        
        # Tutorial selection sidebar
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew", padx=(5, 10), pady=5)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(3, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def setup_tutorial_content(self) -> None:
        """
        Set up the tutorial content display area.
        
        Learning Notes:
        - Content management and display
        - Tutorial navigation and progress tracking
        - User interface for educational content
        """
        
        # Title display
        self.main_title = ctk.CTkLabel(
            self.title_frame,
            text="📚 Interactive SQL Learning Lab",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.main_title.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Progress indicator
        self.progress_label = ctk.CTkLabel(
            self.title_frame,
            text="Lesson 1 of 5",
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.grid(row=0, column=1, padx=20, pady=15, sticky="e")
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            self.sidebar_frame,
            text="🎯 SQL Tutorials",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        sidebar_title.grid(row=0, column=0, padx=10, pady=10)
        
        # Tutorial list
        self.tutorial_list_frame = ctk.CTkScrollableFrame(self.sidebar_frame)
        self.tutorial_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Populate tutorial list
        self.create_tutorial_list()
        
        # Database schema info
        schema_frame = ctk.CTkFrame(self.sidebar_frame)
        schema_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        schema_title = ctk.CTkLabel(schema_frame, text="📊 Database Tables", font=ctk.CTkFont(weight="bold"))
        schema_title.pack(pady=(10, 5))
        
        # Show available tables
        tables = self.db_engine.get_available_tables()
        for table in tables:
            if not table.startswith('sqlite_') and table != 'tutorial_progress':
                table_btn = ctk.CTkButton(
                    schema_frame,
                    text=f"📋 {table}",
                    width=200,
                    height=30,
                    command=lambda t=table: self.show_table_schema(t)
                )
                table_btn.pack(pady=2, padx=10)
    
    def setup_query_interface(self) -> None:
        """
        Set up the SQL query input and execution interface.
        
        Learning Notes:
        - Text input widgets with syntax highlighting
        - Query validation and execution
        - Error handling and user feedback
        """
        
        # Tutorial content display
        self.lesson_frame = ctk.CTkFrame(self.content_frame)
        self.lesson_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.lesson_frame.grid_columnconfigure(0, weight=1)
        
        # Current lesson title
        self.lesson_title = ctk.CTkLabel(
            self.lesson_frame,
            text="Getting Started with SQL",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lesson_title.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        # Lesson description
        self.lesson_description = ctk.CTkTextbox(self.lesson_frame, height=80)
        self.lesson_description.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Query input section
        query_frame = ctk.CTkFrame(self.content_frame)
        query_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        query_frame.grid_rowconfigure(1, weight=1)
        query_frame.grid_columnconfigure(0, weight=1)
        
        # Query input header
        query_header_frame = ctk.CTkFrame(query_frame, fg_color="transparent")
        query_header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        query_header_frame.grid_columnconfigure(1, weight=1)
        
        query_label = ctk.CTkLabel(query_header_frame, text="💻 SQL Query Editor", font=ctk.CTkFont(size=16, weight="bold"))
        query_label.grid(row=0, column=0, padx=10, sticky="w")
        
        # Query action buttons
        button_frame = ctk.CTkFrame(query_header_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=10, sticky="e")
        
        self.execute_btn = ctk.CTkButton(
            button_frame,
            text="▶️ Execute",
            width=100,
            command=self.execute_query,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.execute_btn.pack(side="right", padx=5)
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            width=80,
            command=self.clear_query
        )
        self.clear_btn.pack(side="right", padx=5)
        
        self.example_btn = ctk.CTkButton(
            button_frame,
            text="💡 Example",
            width=80,
            command=self.load_example_query
        )
        self.example_btn.pack(side="right", padx=5)
        
        # SQL Query input
        self.query_input = ctk.CTkTextbox(
            query_frame,
            height=150,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.query_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Bind Ctrl+Enter to execute
        self.query_input.bind("<Control-Return>", lambda e: self.execute_query())
        
        # Query validation indicator
        self.validation_frame = ctk.CTkFrame(self.content_frame, height=30)
        self.validation_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.validation_label = ctk.CTkLabel(
            self.validation_frame,
            text="✅ Ready to execute SQL queries",
            font=ctk.CTkFont(size=12)
        )
        self.validation_label.pack(pady=5)
    
    def setup_results_display(self) -> None:
        """
        Set up the query results display area.
        
        Learning Notes:
        - Tabular data display in GUI
        - Dynamic content rendering
        - Result formatting and presentation
        """
        
        # Results section
        results_frame = ctk.CTkFrame(self.content_frame)
        results_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(5, 10))
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Results header
        results_header = ctk.CTkLabel(
            results_frame,
            text="📊 Query Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_header.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Results display
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Show welcome message
        self.show_welcome_message()
    
    def create_tutorial_list(self) -> None:
        """Create the list of available tutorials."""
        
        for i, tutorial in enumerate(self.tutorials):
            # Tutorial button
            tutorial_btn = ctk.CTkButton(
                self.tutorial_list_frame,
                text=f"{i+1}. {tutorial['title']}",
                width=220,
                height=40,
                anchor="w",
                command=lambda idx=i: self.load_tutorial(idx)
            )
            tutorial_btn.pack(pady=5, padx=5, fill="x")
            
            # Difficulty indicator
            difficulty_colors = {
                'Beginner': 'green',
                'Intermediate': 'orange', 
                'Advanced': 'red'
            }
            
            difficulty_label = ctk.CTkLabel(
                self.tutorial_list_frame,
                text=f"Level: {tutorial['difficulty']}",
                font=ctk.CTkFont(size=10),
                text_color=difficulty_colors.get(tutorial['difficulty'], 'gray')
            )
            difficulty_label.pack(pady=(0, 10))
    
    def load_tutorial(self, tutorial_index: int) -> None:
        """
        Load a specific tutorial.
        
        Learning Notes:
        - Content loading and state management
        - Dynamic UI updates
        - Progress tracking
        """
        
        if tutorial_index >= len(self.tutorials):
            return
        
        self.current_tutorial = tutorial_index
        tutorial = self.tutorials[tutorial_index]
        
        # Update UI
        self.lesson_title.configure(text=tutorial['title'])
        self.progress_label.configure(text=f"Lesson {tutorial_index + 1} of {len(self.tutorials)}")
        
        # Update description
        self.lesson_description.delete("1.0", "end")
        description_text = f"Difficulty: {tutorial['difficulty']}\n\n{tutorial['description']}\n\nExamples available: {len(tutorial['examples'])}"
        self.lesson_description.insert("1.0", description_text)
        self.lesson_description.configure(state="disabled")
        
        # Clear previous results
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", f"📖 Tutorial loaded: {tutorial['title']}\n\nClick 'Example' to see sample queries, or write your own SQL query below.\n\nTip: Press Ctrl+Enter to execute queries quickly!")
        
        self.current_lesson = 0
    
    def load_example_query(self) -> None:
        """Load an example query from the current tutorial."""
        
        if self.current_tutorial >= len(self.tutorials):
            return
        
        tutorial = self.tutorials[self.current_tutorial]
        examples = tutorial.get('examples', [])
        
        if not examples:
            messagebox.showinfo("No Examples", "No examples available for this tutorial.")
            return
        
        # Get next example (cycle through them)
        example = examples[self.current_lesson % len(examples)]
        
        # Load the query
        self.query_input.delete("1.0", "end")
        self.query_input.insert("1.0", example['query'])
        
        # Show explanation
        self.validation_label.configure(text=f"💡 Example: {example['explanation']}")
        
        # Move to next example for next time
        self.current_lesson = (self.current_lesson + 1) % len(examples)
    
    def execute_query(self) -> None:
        """
        Execute the SQL query and display results.
        
        Learning Notes:
        - SQL query execution and error handling
        - Result formatting and display
        - User feedback and validation
        """
        
        query = self.query_input.get("1.0", "end").strip()
        
        if not query:
            self.validation_label.configure(text="⚠️ Please enter a SQL query")
            return
        
        # Validate query
        is_valid, validation_message = self.db_engine.validate_sql_query(query)
        
        if not is_valid:
            self.validation_label.configure(text=f"❌ {validation_message}")
            return
        
        try:
            # Execute query
            self.validation_label.configure(text="⏳ Executing query...")
            
            results = self.db_engine.execute_query(query)
            
            # Display results
            self.display_query_results(query, results)
            
            self.validation_label.configure(text=f"✅ Query executed successfully - {len(results)} rows returned")
            
        except Exception as e:
            self.validation_label.configure(text=f"❌ Query error: {str(e)}")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"Query Error:\n{str(e)}\n\nPlease check your SQL syntax and try again.")
    
    def display_query_results(self, query: str, results: List[Dict[str, Any]]) -> None:
        """
        Display query results in a formatted table.
        
        Learning Notes:
        - Data formatting and presentation
        - Table rendering in text widgets
        - Result analysis and insights
        """
        
        self.results_text.delete("1.0", "end")
        
        # Show query
        self.results_text.insert("end", f"📝 Executed Query:\n{query}\n\n")
        
        if not results:
            self.results_text.insert("end", "📊 Results: No rows returned.\n\n")
            self.results_text.insert("end", "💡 This might mean:\n")
            self.results_text.insert("end", "   • The query conditions didn't match any data\n")
            self.results_text.insert("end", "   • The table is empty\n")
            self.results_text.insert("end", "   • There might be a logical error in the query\n")
            return
        
        # Show row count
        self.results_text.insert("end", f"📊 Results: {len(results)} row(s) returned\n\n")
        
        # Get column names
        if results:
            columns = list(results[0].keys())
            
            # Calculate column widths
            col_widths = {}
            for col in columns:
                col_widths[col] = max(len(str(col)), max(len(str(row.get(col, ''))) for row in results[:10]))
                col_widths[col] = min(col_widths[col], 20)  # Max width of 20
            
            # Header
            header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
            self.results_text.insert("end", header + "\n")
            self.results_text.insert("end", "-" * len(header) + "\n")
            
            # Data rows (limit to first 100 rows for performance)
            for i, row in enumerate(results[:100]):
                row_text = " | ".join(f"{str(row.get(col, '')):<{col_widths[col]}}" for col in columns)
                self.results_text.insert("end", row_text + "\n")
            
            if len(results) > 100:
                self.results_text.insert("end", f"\n... and {len(results) - 100} more rows\n")
            
            # Add analysis
            self.add_result_analysis(results, columns)
    
    def add_result_analysis(self, results: List[Dict], columns: List[str]) -> None:
        """Add helpful analysis of the query results."""
        
        self.results_text.insert("end", "\n" + "="*50 + "\n")
        self.results_text.insert("end", "📈 Result Analysis:\n\n")
        
        # Basic statistics
        self.results_text.insert("end", f"• Total rows: {len(results)}\n")
        self.results_text.insert("end", f"• Columns: {len(columns)}\n")
        self.results_text.insert("end", f"• Column names: {', '.join(columns)}\n\n")
        
        # Data type analysis
        if results:
            self.results_text.insert("end", "💡 Learning Notes:\n")
            
            # Check for numeric columns
            numeric_cols = []
            for col in columns:
                try:
                    float(results[0].get(col, ''))
                    numeric_cols.append(col)
                except (ValueError, TypeError):
                    pass
            
            if numeric_cols:
                self.results_text.insert("end", f"• Numeric columns detected: {', '.join(numeric_cols)}\n")
                self.results_text.insert("end", "  Try using functions like SUM(), AVG(), MIN(), MAX() on these!\n")
            
            # Check for date patterns
            date_cols = [col for col in columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_cols:
                self.results_text.insert("end", f"• Date columns: {', '.join(date_cols)}\n")
                self.results_text.insert("end", "  Try using date functions and ORDER BY for time-based analysis!\n")
            
            # Suggest next steps
            self.results_text.insert("end", "\n🎯 Try these next:\n")
            if len(results) > 1:
                self.results_text.insert("end", "• Add WHERE clauses to filter specific data\n")
                self.results_text.insert("end", "• Use ORDER BY to sort the results\n")
                self.results_text.insert("end", "• Try GROUP BY for data aggregation\n")
    
    def clear_query(self) -> None:
        """Clear the query input."""
        self.query_input.delete("1.0", "end")
        self.validation_label.configure(text="✅ Query cleared - Ready for new input")
    
    def show_table_schema(self, table_name: str) -> None:
        """Show the schema for a specific table."""
        
        schema = self.db_engine.get_table_schema(table_name)
        
        if not schema:
            messagebox.showerror("Error", f"Could not retrieve schema for table: {table_name}")
            return
        
        # Show schema in results area
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", f"📋 Table Schema: {table_name}\n\n")
        
        # Column information
        self.results_text.insert("end", "Column Name        | Data Type    | Nullable | Primary Key\n")
        self.results_text.insert("end", "-" * 60 + "\n")
        
        for col in schema:
            pk_marker = "✓" if col['primary_key'] else " "
            null_marker = "✓" if not col['not_null'] else " "
            
            line = f"{col['column']:<18} | {col['type']:<12} | {null_marker:<8} | {pk_marker}\n"
            self.results_text.insert("end", line)
        
        # Sample data query
        self.results_text.insert("end", f"\n💡 Try this query to see sample data:\nSELECT * FROM {table_name} LIMIT 5;\n")
        
        # Load sample query
        self.query_input.delete("1.0", "end")
        self.query_input.insert("1.0", f"SELECT * FROM {table_name} LIMIT 5;")
    
    def show_welcome_message(self) -> None:
        """Show the welcome message with getting started info."""
        
        welcome_text = """
🎉 Welcome to the SQL Learning Lab!

This interactive environment helps you learn SQL with hands-on practice using real data.

📊 Available Tables:
• employees - Company employee data
• departments - Department information  
• sales - Sales transaction records

🎯 Getting Started:
1. Choose a tutorial from the left sidebar
2. Click "Example" to see sample queries
3. Modify queries or write your own
4. Press "Execute" or Ctrl+Enter to run queries
5. Analyze the results and learn!

💡 Tips:
• Start with "Basic SELECT" tutorial
• Click on table names to see their structure
• Experiment with different WHERE conditions
• Try combining data from multiple tables

Ready to become an SQL expert? Let's start learning! 🚀
        """
        
        self.results_text.insert("1.0", welcome_text) 