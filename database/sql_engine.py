"""
SQL Database Engine for CodeMaster Pro

Learning Notes:
- This module demonstrates SQLite database operations in Python
- Shows database connection management and SQL execution
- Implements educational SQL features with examples and tutorials
- Demonstrates transaction handling and error management
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

class SQLEngine:
    """
    SQL Database Engine with educational features.
    
    This class provides:
    1. SQLite database management
    2. Educational SQL tutorials and examples
    3. Safe query execution with validation
    4. Database schema management
    5. Learning progress tracking
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the SQL engine with database connection."""
        
        # Set up database path
        if db_path is None:
            db_dir = Path.home() / '.codemaster_pro' / 'database'
            db_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = db_dir / 'codemaster.db'
        else:
            self.db_path = Path(db_path)
        
        self.connection = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self.connect()
        self.create_tables()
        self.populate_sample_data()
        
        print(f"📊 SQL Database initialized: {self.db_path}")
    
    def connect(self) -> bool:
        """
        Establish database connection.
        
        Learning Notes:
        - SQLite connection management
        - Error handling for database connections
        - Connection configuration for optimal performance
        """
        try:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,  # Allow multi-threaded access
                timeout=30.0  # 30 second timeout
            )
            
            # Enable foreign key constraints
            self.connection.execute("PRAGMA foreign_keys = ON")
            
            # Set row factory for easier data access
            self.connection.row_factory = sqlite3.Row
            
            self.logger.info(f"Connected to database: {self.db_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            return False
    
    def close(self) -> None:
        """Close database connection safely."""
        if self.connection:
            try:
                self.connection.close()
                self.logger.info("Database connection closed")
            except Exception as e:
                self.logger.error(f"Error closing database: {e}")
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.
        
        Learning Notes:
        - Safe SQL query execution with parameters
        - Result formatting and processing
        - Error handling for SQL operations
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch all results and convert to list of dictionaries
            rows = cursor.fetchall()
            results = [dict(row) for row in rows]
            
            self.logger.debug(f"Query executed successfully: {len(results)} rows returned")
            return results
            
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        Learning Notes:
        - Data modification operations
        - Transaction management
        - Affected row counting
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            affected_rows = cursor.rowcount
            
            self.logger.debug(f"Update executed successfully: {affected_rows} rows affected")
            return affected_rows
            
        except Exception as e:
            self.logger.error(f"Update execution failed: {e}")
            self.connection.rollback()
            return 0
    
    def create_tables(self) -> None:
        """
        Create database tables for the application.
        
        Learning Notes:
        - Database schema design
        - Table creation with constraints
        - Primary keys, foreign keys, and indexes
        """
        
        # Projects table for codebase management
        projects_table = """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            path TEXT NOT NULL,
            description TEXT,
            language TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_count INTEGER DEFAULT 0,
            line_count INTEGER DEFAULT 0
        )
        """
        
        # SQL Tutorial progress tracking
        tutorial_progress = """
        CREATE TABLE IF NOT EXISTS tutorial_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id TEXT NOT NULL,
            lesson_title TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            completed_at DATETIME,
            score INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0
        )
        """
        
        # Sample data tables for SQL learning
        employees_table = """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            salary REAL,
            hire_date DATE,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
        )
        """
        
        departments_table = """
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INTEGER PRIMARY KEY,
            dept_name TEXT NOT NULL UNIQUE,
            location TEXT,
            budget REAL
        )
        """
        
        sales_table = """
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            product_name TEXT NOT NULL,
            sale_amount REAL NOT NULL,
            sale_date DATE NOT NULL,
            customer_name TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
        """
        
        # Weather data cache table
        weather_cache = """
        CREATE TABLE IF NOT EXISTS weather_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            weather_data TEXT NOT NULL,
            cached_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Execute table creation
        tables = [
            projects_table,
            tutorial_progress,
            employees_table,
            departments_table,
            sales_table,
            weather_cache
        ]
        
        for table_sql in tables:
            try:
                self.execute_update(table_sql)
            except Exception as e:
                self.logger.error(f"Failed to create table: {e}")
        
        self.logger.info("Database tables created successfully")
    
    def populate_sample_data(self) -> None:
        """
        Populate tables with sample data for SQL learning.
        
        Learning Notes:
        - Data insertion and batch operations
        - Sample data generation for learning
        - Transaction management for data consistency
        """
        
        # Check if data already exists
        existing_employees = self.execute_query("SELECT COUNT(*) as count FROM employees")
        if existing_employees and existing_employees[0]['count'] > 0:
            return  # Data already exists
        
        try:
            # Sample departments
            departments_data = [
                (1, 'Engineering', 'New York', 2000000),
                (2, 'Marketing', 'Los Angeles', 800000),
                (3, 'Sales', 'Chicago', 1200000),
                (4, 'HR', 'New York', 600000),
                (5, 'Finance', 'Boston', 900000)
            ]
            
            dept_insert = "INSERT INTO departments (dept_id, dept_name, location, budget) VALUES (?, ?, ?, ?)"
            for dept in departments_data:
                self.execute_update(dept_insert, dept)
            
            # Sample employees
            employees_data = [
                (1, 'John', 'Doe', 'john.doe@company.com', 'Engineering', 95000, '2020-01-15', None),
                (2, 'Jane', 'Smith', 'jane.smith@company.com', 'Engineering', 105000, '2019-03-20', 1),
                (3, 'Mike', 'Johnson', 'mike.johnson@company.com', 'Marketing', 75000, '2021-06-10', None),
                (4, 'Sarah', 'Williams', 'sarah.williams@company.com', 'Sales', 80000, '2020-11-05', None),
                (5, 'David', 'Brown', 'david.brown@company.com', 'HR', 70000, '2022-02-14', None),
                (6, 'Lisa', 'Davis', 'lisa.davis@company.com', 'Finance', 85000, '2021-09-30', None),
                (7, 'Tom', 'Wilson', 'tom.wilson@company.com', 'Engineering', 92000, '2020-07-22', 2),
                (8, 'Emma', 'Garcia', 'emma.garcia@company.com', 'Marketing', 68000, '2022-01-18', 3)
            ]
            
            emp_insert = """INSERT INTO employees 
                           (employee_id, first_name, last_name, email, department, salary, hire_date, manager_id) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            for emp in employees_data:
                self.execute_update(emp_insert, emp)
            
            # Sample sales data
            sales_data = [
                (1, 2, 'Software License', 15000, '2023-01-15', 'TechCorp Inc'),
                (2, 4, 'Consulting Service', 25000, '2023-02-20', 'StartupXYZ'),
                (3, 4, 'Training Package', 8000, '2023-03-10', 'BigCompany Ltd'),
                (4, 2, 'Custom Development', 35000, '2023-03-25', 'Enterprise Solutions'),
                (5, 4, 'Support Contract', 12000, '2023-04-05', 'Local Business'),
                (6, 2, 'Software License', 18000, '2023-04-18', 'Government Agency'),
                (7, 4, 'Consulting Service', 22000, '2023-05-02', 'NonProfit Org')
            ]
            
            sales_insert = """INSERT INTO sales 
                            (sale_id, employee_id, product_name, sale_amount, sale_date, customer_name) 
                            VALUES (?, ?, ?, ?, ?, ?)"""
            for sale in sales_data:
                self.execute_update(sales_insert, sale)
            
            self.logger.info("Sample data populated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to populate sample data: {e}")
    
    def get_sql_tutorials(self) -> List[Dict[str, Any]]:
        """
        Get list of SQL tutorials with examples.
        
        Learning Notes:
        - Educational content organization
        - Progressive learning structure
        - Practical examples with explanations
        """
        
        tutorials = [
            {
                'id': 'basic_select',
                'title': 'Basic SELECT Statements',
                'description': 'Learn how to query data from tables',
                'difficulty': 'Beginner',
                'examples': [
                    {
                        'query': 'SELECT * FROM employees;',
                        'explanation': 'Select all columns from the employees table'
                    },
                    {
                        'query': 'SELECT first_name, last_name FROM employees;',
                        'explanation': 'Select specific columns'
                    },
                    {
                        'query': 'SELECT * FROM employees WHERE department = "Engineering";',
                        'explanation': 'Filter rows with WHERE clause'
                    }
                ]
            },
            {
                'id': 'filtering_sorting',
                'title': 'Filtering and Sorting Data',
                'description': 'Use WHERE, ORDER BY, and LIMIT clauses',
                'difficulty': 'Beginner',
                'examples': [
                    {
                        'query': 'SELECT * FROM employees WHERE salary > 80000;',
                        'explanation': 'Filter by numeric condition'
                    },
                    {
                        'query': 'SELECT * FROM employees ORDER BY salary DESC;',
                        'explanation': 'Sort by salary in descending order'
                    },
                    {
                        'query': 'SELECT * FROM employees ORDER BY hire_date LIMIT 5;',
                        'explanation': 'Get the 5 earliest hired employees'
                    }
                ]
            },
            {
                'id': 'joins',
                'title': 'JOIN Operations',
                'description': 'Combine data from multiple tables',
                'difficulty': 'Intermediate',
                'examples': [
                    {
                        'query': '''SELECT e.first_name, e.last_name, s.product_name, s.sale_amount
                                   FROM employees e
                                   JOIN sales s ON e.employee_id = s.employee_id;''',
                        'explanation': 'Inner join to get employee sales data'
                    },
                    {
                        'query': '''SELECT e.first_name, e.last_name, m.first_name as manager_name
                                   FROM employees e
                                   LEFT JOIN employees m ON e.manager_id = m.employee_id;''',
                        'explanation': 'Self-join to get employee and manager names'
                    }
                ]
            },
            {
                'id': 'aggregation',
                'title': 'Aggregate Functions',
                'description': 'Use COUNT, SUM, AVG, MIN, MAX',
                'difficulty': 'Intermediate',
                'examples': [
                    {
                        'query': 'SELECT COUNT(*) as total_employees FROM employees;',
                        'explanation': 'Count total number of employees'
                    },
                    {
                        'query': 'SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department;',
                        'explanation': 'Average salary by department'
                    },
                    {
                        'query': 'SELECT SUM(sale_amount) as total_sales FROM sales;',
                        'explanation': 'Total sales amount'
                    }
                ]
            },
            {
                'id': 'advanced',
                'title': 'Advanced Queries',
                'description': 'Subqueries, window functions, and complex operations',
                'difficulty': 'Advanced',
                'examples': [
                    {
                        'query': '''SELECT * FROM employees 
                                   WHERE salary > (SELECT AVG(salary) FROM employees);''',
                        'explanation': 'Employees with above-average salary using subquery'
                    },
                    {
                        'query': '''SELECT e.first_name, e.last_name, 
                                          COUNT(s.sale_id) as total_sales
                                   FROM employees e
                                   LEFT JOIN sales s ON e.employee_id = s.employee_id
                                   GROUP BY e.employee_id
                                   ORDER BY total_sales DESC;''',
                        'explanation': 'Employee sales performance ranking'
                    }
                ]
            }
        ]
        
        return tutorials
    
    def validate_sql_query(self, query: str) -> Tuple[bool, str]:
        """
        Validate SQL query for safety and correctness.
        
        Learning Notes:
        - SQL injection prevention
        - Query validation techniques
        - Safe execution practices
        """
        
        # Remove comments and normalize whitespace
        query = query.strip()
        query_upper = query.upper()
        
        # Check for dangerous operations
        dangerous_keywords = [
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False, f"Query contains dangerous keyword: {keyword}"
        
        # Check for basic SQL syntax
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed in learning mode"
        
        # Check for semicolon at the end (should have one)
        if not query.rstrip().endswith(';'):
            return False, "Query should end with a semicolon (;)"
        
        return True, "Query validation passed"
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information for learning purposes."""
        
        try:
            schema_query = f"PRAGMA table_info({table_name})"
            schema_info = self.execute_query(schema_query)
            
            return [
                {
                    'column': row['name'],
                    'type': row['type'],
                    'not_null': bool(row['notnull']),
                    'primary_key': bool(row['pk'])
                }
                for row in schema_info
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to get schema for {table_name}: {e}")
            return []
    
    def get_available_tables(self) -> List[str]:
        """Get list of available tables for learning."""
        
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        tables = self.execute_query(query)
        return [table['name'] for table in tables] 