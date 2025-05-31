# CSV2HTML

[![Website](https://img.shields.io/badge/Website-csv.baycode.eu-blue)](https://csv.baycode.eu)
[![GitHub](https://img.shields.io/badge/GitHub-krystianbajno/csvhtml-green)](https://github.com/krystianbajno/csvhtml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, elegant CSV to HTML converter with professional styling and responsive design. Convert your CSV files into beautiful, interactive HTML tables with advanced features like search, filtering, and dark/light mode support.

## ✨ Features

### 🎨 Modern Design
- **Professional Styling**: Clean, elegant design with glassmorphism effects
- **Dark/Light Mode**: Toggle between themes with persistent preferences
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Focus-Friendly**: Optimized for productivity with reduced visual noise

### 📊 Advanced Functionality
- **Smart CSV Parsing**: Automatic delimiter detection (comma, semicolon, tab, pipe)
- **Real-time Search**: Instant table filtering as you type
- **Export Options**: Download processed tables in various formats
- **Statistics Dashboard**: View row/column counts and data insights
- **UTF-8 Support**: Full unicode character support

### 🔧 Two Usage Methods
1. **Web Interface** (`index.html`): Drag-and-drop CSV upload with instant preview
2. **Python Script** (`csvhtml_enhanced.py`): Command-line tool for batch processing

## 🚀 Quick Start

### Web Interface
1. Open `index.html` in your web browser
2. Drag and drop your CSV file or click to browse
3. View your data in a beautiful, interactive table
4. Use search and filtering features
5. Export or share your results

### Python Script
```bash
# Basic usage
python csv2html.py input.csv

# Specify output file
python csv2html.py input.csv -o output.html

# With custom delimiter
python csv2html.py input.csv --delimiter ";"
```

## 📋 Requirements

### For Web Interface
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies required

## 🎯 Key Features Detailed

### 🌙 Dark/Light Mode
- Automatic theme detection based on system preferences
- Manual toggle with persistent storage
- Optimized contrast ratios for accessibility
- Smooth transitions between themes

### 🔍 Advanced Search & Filtering
- Real-time search across all columns
- Case-insensitive filtering
- Instant results with highlighting
- Maintains table formatting during search

### Colors and Themes
Both the web interface and Python output support extensive customization:
- CSS custom properties for easy theme modification
- Consistent color palette across light/dark modes
- Accessible contrast ratios (WCAG AA compliant)

### Styling Options
Modify the CSS variables in either file to customize:
```css
:root {
  --primary-color: #667eea;
  --accent-color: #764ba2;
  --background: #f8fafc;
  --surface: rgba(255, 255, 255, 0.8);
}
```

<div align="center">
  <strong>Made with ❤️ by Krystian Bajno • 2025</strong>
</div> 
