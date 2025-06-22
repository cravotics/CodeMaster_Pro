#!/usr/bin/env python3
"""
Test Script for CodeMaster Pro

This script tests all components and helps identify any issues before running the main application.
Run this before running main.py to ensure everything is set up correctly.
"""

import sys
import os
from pathlib import Path
import traceback

def test_python_version():
    """Test if Python version is compatible."""
    print("🐍 Testing Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    else:
        print(f"✅ Python version: {sys.version}")
        return True

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'customtkinter',
        'requests',
        'gitpython',
        'python-dotenv',
        'pillow',
        'psutil',
        'matplotlib',
        'numpy',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'customtkinter':
                import customtkinter
            elif package == 'requests':
                import requests
            elif package == 'gitpython':
                import git
            elif package == 'python-dotenv':
                import dotenv
            elif package == 'pillow':
                import PIL
            elif package == 'psutil':
                import psutil
            elif package == 'matplotlib':
                import matplotlib
            elif package == 'numpy':
                import numpy
            elif package == 'pandas':
                import pandas
            
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("💡 Install with: pip install -r requirements.txt")
        return False
    
    return True

def test_project_structure():
    """Test if project structure is correct."""
    print("\n📁 Testing project structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'utils/config.py',
        'utils/helpers.py',
        'database/sql_engine.py',
        'apis/weather_api.py',
        'apis/fonts_api.py',
        'gui/main_window.py',
        'gui/sql_tutor.py',
        'gui/weather_widget.py',
        'gui/code_editor.py',
        'gui/font_manager.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def test_database():
    """Test database functionality."""
    print("\n🗄️ Testing database...")
    
    try:
        # Add project root to path
        sys.path.append(str(Path(__file__).parent))
        
        from database.sql_engine import SQLEngine
        
        # Test database creation
        db = SQLEngine()
        
        # Test basic query
        result = db.execute_query("SELECT COUNT(*) as count FROM employees")
        if result and len(result) > 0:
            print(f"✅ Database working - {result[0]['count']} employees loaded")
        else:
            print("❌ Database query failed")
            return False
        
        # Test tutorials
        tutorials = db.get_sql_tutorials()
        if tutorials and len(tutorials) > 0:
            print(f"✅ SQL tutorials loaded - {len(tutorials)} tutorials available")
        else:
            print("❌ SQL tutorials not loaded")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration system."""
    print("\n⚙️ Testing configuration...")
    
    try:
        from utils.config import Config
        
        config = Config()
        
        # Test basic config operations
        config.set('test_key', 'test_value')
        value = config.get('test_key')
        
        if value == 'test_value':
            print("✅ Configuration system working")
        else:
            print("❌ Configuration test failed")
            return False
        
        # Test API key detection
        api_keys = {
            'openai': config.get_api_key('openai'),
            'weather': config.get_api_key('weather'),
            'fonts': config.get_api_key('fonts'),
            'anthropic': config.get_api_key('anthropic')
        }
        
        has_any_key = any(key for key in api_keys.values())
        
        if has_any_key:
            print("✅ API keys detected")
            for service, key in api_keys.items():
                if key:
                    print(f"  ✅ {service}: configured")
                else:
                    print(f"  ⚠️ {service}: not configured")
        else:
            print("⚠️ No API keys configured (app will work with limited functionality)")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        traceback.print_exc()
        return False

def test_apis():
    """Test API integrations."""
    print("\n🌐 Testing API integrations...")
    
    try:
        from utils.config import Config
        from apis.weather_api import WeatherAPI
        from apis.fonts_api import FontsAPI
        
        config = Config()
        
        # Test Weather API
        print("  Testing Weather API...")
        weather_api = WeatherAPI(config)
        weather_data = weather_api.get_current_weather("New York")
        
        if weather_data and 'temperature' in weather_data:
            print(f"  ✅ Weather API working - {weather_data['temperature']}°C in {weather_data.get('location', 'Unknown')}")
        else:
            print("  ⚠️ Weather API using fallback data")
        
        # Test Fonts API
        print("  Testing Fonts API...")
        fonts_api = FontsAPI(config)
        system_fonts = fonts_api.get_system_fonts()
        
        if system_fonts and len(system_fonts) > 0:
            print(f"  ✅ Fonts API working - {len(system_fonts)} system fonts available")
        else:
            print("  ❌ Fonts API failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        traceback.print_exc()
        return False

def test_gui_imports():
    """Test GUI component imports."""
    print("\n🖼️ Testing GUI components...")
    
    try:
        # Test CustomTkinter
        import customtkinter as ctk
        print("✅ CustomTkinter imported")
        
        # Test GUI components import
        from gui.main_window import MainWindow
        from gui.sql_tutor import SQLTutorWidget
        from gui.weather_widget import WeatherWidget
        from gui.code_editor import CodeEditorWidget
        from gui.font_manager import FontManagerWidget
        
        print("✅ All GUI components imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI import test failed: {e}")
        traceback.print_exc()
        return False

def create_env_file_if_missing():
    """Create .env file from example if it doesn't exist."""
    
    if not Path('.env').exists() and Path('env_example.txt').exists():
        print("\n📝 Creating .env file from example...")
        try:
            import shutil
            shutil.copy('env_example.txt', '.env')
            print("✅ .env file created from example")
            print("💡 Edit .env file to add your API keys for full functionality")
        except Exception as e:
            print(f"⚠️ Could not create .env file: {e}")

def run_quick_app_test():
    """Run a quick app initialization test."""
    print("\n🚀 Testing app initialization...")
    
    try:
        # Set minimal display for testing
        os.environ['DISPLAY'] = os.environ.get('DISPLAY', ':0')
        
        from utils.config import Config
        from database.sql_engine import SQLEngine
        
        # Test basic initialization
        config = Config()
        db_engine = SQLEngine()
        
        print("✅ App components initialized successfully")
        
        # Test that GUI can be imported (but don't actually show it)
        import customtkinter as ctk
        
        # Set appearance for testing
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        print("✅ GUI framework configured")
        
        db_engine.close()
        return True
        
    except Exception as e:
        print(f"❌ App initialization test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    
    print("🧪 CodeMaster Pro - System Test")
    print("=" * 50)
    
    # Create .env file if missing
    create_env_file_if_missing()
    
    # Run tests
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Project Structure", test_project_structure),
        ("Database", test_database),
        ("Configuration", test_configuration),
        ("APIs", test_apis),
        ("GUI Components", test_gui_imports),
        ("App Initialization", run_quick_app_test)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! You're ready to run CodeMaster Pro!")
        print("\n🚀 Next steps:")
        print("1. Run: python main.py")
        print("2. Start with the SQL Learning tab")
        print("3. Add API keys to .env for full functionality")
        return True
    else:
        print("⚠️ Some tests failed. Please fix the issues above before running the app.")
        print("\n💡 Common solutions:")
        print("• Install dependencies: pip install -r requirements.txt")
        print("• Check Python version: python --version")
        print("• Verify file structure is complete")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test script failed: {e}")
        traceback.print_exc()
        sys.exit(1) 