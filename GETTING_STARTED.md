# 🚀 Getting Started with CodeMaster Pro

Welcome to **CodeMaster Pro** - your AI-powered development environment! This guide will help you get up and running quickly.

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Windows 10+ / macOS / Linux**
- **Internet connection** (for API features)

## 🛠️ Installation Steps

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd Git-projs

# Install required packages
pip install -r requirements.txt
```

### 2. Set Up API Keys (Optional but Recommended)

Create a `.env` file in the project root:

```bash
# Copy the example file
copy env_example.txt .env
```

Edit the `.env` file and add your API keys:

```env
# Free API keys - all completely free for learning!

# OpenAI (for AI assistance) - Get at: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_key_here

# OpenWeatherMap (for weather) - Get at: https://openweathermap.org/api
WEATHER_API_KEY=your_weather_key_here

# Google Fonts (for typography) - Get at: https://developers.google.com/fonts/docs/developer_api
GOOGLE_FONTS_API_KEY=your_google_fonts_key_here

# Anthropic (alternative AI) - Get at: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### 3. Run the Application

```bash
python main.py
```

## 🎯 First Steps - Learning Path

### 1. **Start with SQL Learning** 📚
- Open the **"SQL Learning"** tab
- Follow the interactive tutorials
- Practice with real data
- Learn from basic SELECT to advanced JOINs

### 2. **Explore Weather Integration** 🌤️
- Check the **"Weather & Productivity"** tab
- See how weather affects your coding recommendations
- Set your location for personalized insights

### 3. **Customize Your Environment** 🔤
- Visit **"Fonts & Styling"** tab
- Browse coding-friendly fonts
- Preview and apply fonts to your editor

### 4. **Code with AI Assistance** 🤖
- Use the **"Code Editor"** tab
- Try the AI analysis features
- Learn code patterns and best practices

### 5. **Manage Projects** 📁
- Explore **"Projects"** tab
- Load existing codebases
- Track your development progress

## 🎓 Learning Modules

### SQL Mastery Journey
```
Beginner → Intermediate → Advanced
   ↓           ↓            ↓
SELECT     JOINs       Subqueries
WHERE      GROUP BY    Window Functions
ORDER BY   HAVING      Performance
```

### What You'll Learn:
- **Database Design**: Proper schema creation
- **Query Optimization**: Write efficient SQL
- **Real-world Examples**: Work with realistic data
- **Best Practices**: Industry-standard approaches

## 🌟 Key Features Overview

### 1. **Interactive SQL Tutorial**
- 📊 Real sample database with employees, sales, departments
- 🎯 Progressive difficulty levels
- 💡 Instant query execution and results
- 📈 Visual result analysis and insights

### 2. **AI Development Assistant**
- 🤖 Code analysis and suggestions
- 📝 Automatic documentation generation
- 🔧 Refactoring recommendations
- 💡 Code explanation and learning

### 3. **Weather-Based Productivity**
- 🌤️ Real-time weather data
- 📅 Development planning recommendations
- 🏠 Indoor/outdoor coding suggestions
- ⚡ Productivity optimization tips

### 4. **Professional Typography**
- 🔤 Google Fonts integration
- ⌨️ Coding font recommendations
- 🎨 Font pairing suggestions
- 👁️ Real-time preview system

### 5. **Project Management**
- 📁 Multi-project support
- 🔄 Git integration
- 📊 Code statistics and metrics
- 💾 Automated backup systems

## 🚀 Quick Start Examples

### SQL Learning Example
```sql
-- Try this in the SQL Tutorial:
SELECT e.first_name, e.last_name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON e.department = d.dept_name
WHERE e.salary > 80000
ORDER BY e.salary DESC;
```

### Weather API Example
The app automatically shows:
- Current temperature and conditions
- 5-day forecast
- Coding recommendations based on weather
- Air quality information

### Font Management Example
1. Browse 900+ Google Fonts
2. Filter by "monospace" for coding
3. Preview with your actual code
4. Apply instantly to your editor

## 🛡️ Security & Privacy

- **Local Data**: All your data stays on your machine
- **API Keys**: Stored securely in environment variables
- **No Tracking**: We don't collect any personal data
- **Open Source**: Full transparency in code

## 📚 Learning Resources

### Free API Keys Setup:

#### OpenAI API ($5 free credit)
1. Go to https://platform.openai.com/api-keys
2. Create account (free)
3. Generate API key
4. Add to `.env` file

#### OpenWeatherMap (1000 calls/day free)
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env` file

#### Google Fonts API (10,000 requests/day free)
1. Go to https://developers.google.com/fonts/docs/developer_api
2. Create Google Cloud project (free)
3. Enable Fonts API
4. Generate API key

## 🔧 Troubleshooting

### Common Issues:

#### "ModuleNotFoundError"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### "API Key Error"
```bash
# Solution: Check your .env file
# Make sure API keys are correctly formatted
# No quotes needed around the keys
```

#### "Database Error"
```bash
# Solution: The app creates its own database
# Delete ~/.codemaster_pro/database/ to reset
```

#### "Font Loading Issues"
```bash
# Solution: Check internet connection
# Google Fonts requires internet access
# System fonts work offline
```

## 🎯 Next Steps

1. **Complete SQL Tutorials**: Master all 5 levels
2. **Explore AI Features**: Try code analysis
3. **Customize Your Setup**: Pick perfect fonts
4. **Build Projects**: Use the project management
5. **Share & Learn**: Use it for real development

## 💡 Pro Tips

### For Maximum Learning:
- **Practice Daily**: Spend 15-30 minutes in SQL tutorial
- **Experiment**: Try modifying the example queries
- **Use AI Help**: Ask questions about code you don't understand
- **Track Progress**: Use the built-in progress tracking

### For Best Experience:
- **Use API Keys**: Unlock full functionality
- **Choose Good Fonts**: Improves coding comfort
- **Monitor Weather**: Plan coding sessions effectively
- **Organize Projects**: Keep your work structured

## 🤝 Getting Help

1. **Check the Documentation**: Built-in help system
2. **Review Error Messages**: Usually self-explanatory
3. **Check API Status**: Ensure keys are working
4. **Reset Settings**: Delete config if needed

## 🎉 You're Ready!

Run `python main.py` and start your journey to becoming a more productive developer with AI assistance, SQL mastery, and professional tools!

---

**Happy Coding!** 🚀✨

Remember: This is a learning platform - experiment, make mistakes, and grow as a developer! 