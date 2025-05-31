#!/usr/bin/env python3
"""
Enhanced CSV to HTML Table Converter
Converts CSV files into beautiful, searchable, and filterable HTML tables with modern styling.

Usage:
    python csvhtml_enhanced.py input.csv [output.html]
    
If no output file is specified, it will create one based on the input filename.
"""

import pandas as pd
import argparse
import sys
import os
from pathlib import Path
import csv
import io

def create_enhanced_html_template(df, table_id="data-table", title="Data Table"):
    """
    Create a complete HTML page with enhanced modern CSS and JavaScript for a searchable table.
    """
    
    # Convert DataFrame to HTML table
    table_html = df.to_html(
        table_id=table_id,
        classes="table table-striped table-hover data-table",
        index=False,
        escape=False
    )
    
    # Get column names for filter dropdowns
    columns = df.columns.tolist()
    
    # Create filter dropdowns HTML
    filter_dropdowns = ""
    for i, col in enumerate(columns):
        unique_values = sorted(df[col].astype(str).unique())
        options = ''.join([f'<option value="{val}">{val}</option>' for val in unique_values])
        filter_dropdowns += f'''
        <div class="col-md-3 mb-3">
            <label for="filter-{i}" class="form-label fw-bold">{col}</label>
            <select class="form-select filter-select" data-column="{i}" id="filter-{i}">
                <option value="">All</option>
                {options}
            </select>
        </div>
        '''
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* Light mode colors */
            --primary-color: #2563eb;
            --primary-hover: #1d4ed8;
            --secondary-color: #64748b;
            --accent-color: #0ea5e9;
            --success-color: #059669;
            --warning-color: #d97706;
            --danger-color: #dc2626;
            
            /* Background colors */
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #f1f5f9;
            --bg-accent: rgba(37, 99, 235, 0.05);
            
            /* Text colors */
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --text-muted: #94a3b8;
            --text-inverse: #ffffff;
            
            /* Border colors */
            --border-light: #e2e8f0;
            --border-medium: #cbd5e1;
            --border-dark: #94a3b8;
            
            /* Shadow colors */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            /* Glass effect */
            --glass-bg: rgba(255, 255, 255, 0.8);
            --glass-border: rgba(255, 255, 255, 0.2);
            --glass-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }}

        [data-theme="dark"] {{
            /* Dark mode colors */
            --primary-color: #3b82f6;
            --primary-hover: #2563eb;
            --secondary-color: #94a3b8;
            --accent-color: #06b6d4;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            
            /* Background colors */
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --bg-accent: rgba(59, 130, 246, 0.1);
            
            /* Text colors */
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-inverse: #0f172a;
            
            /* Border colors */
            --border-light: #334155;
            --border-medium: #475569;
            --border-dark: #64748b;
            
            /* Glass effect */
            --glass-bg: rgba(15, 23, 42, 0.8);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            min-height: 100vh;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            transition: all 0.3s ease;
        }}
        
        .main-container {{
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow);
            margin: 2rem;
            padding: 2.5rem;
            position: relative;
        }}
        
        .page-header {{
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }}
        
        .theme-toggle {{
            position: absolute;
            top: 0;
            right: 0;
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            padding: 0.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            color: var(--text-secondary);
        }}
        
        .theme-toggle:hover {{
            background: var(--bg-accent);
            color: var(--primary-color);
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
        }}
        
        .page-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            letter-spacing: -0.025em;
        }}
        
        .page-subtitle {{
            color: var(--text-secondary);
            font-size: 1.125rem;
            font-weight: 400;
            margin: 0 auto 2rem;
        }}
        
        .stats-container {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }}
        
        .stats-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            padding: 2rem;
            text-align: center;
            min-width: 200px;
            box-shadow: var(--shadow-md);
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .stats-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }}
        
        .stats-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }}
        
        .stats-label {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .controls-section {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
        }}
        
        .search-container {{
            margin-bottom: 2rem;
        }}
        
        .form-label {{
            color: var(--text-primary);
            font-weight: 600;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .search-input, .filter-select {{
            background: var(--bg-primary);
            border: 1px solid var(--border-light);
            padding: 0.875rem 1rem;
            font-size: 0.95rem;
            color: var(--text-primary);
            transition: all 0.3s ease;
            box-shadow: var(--shadow-sm);
            width: 100%;
        }}
        
        .search-input:focus, .filter-select:focus {{
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            background: var(--bg-primary);
        }}
        
        .btn-modern {{
            background: var(--primary-color);
            border: none;
            color: var(--text-inverse);
            padding: 0.875rem 2rem;
            font-weight: 600;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-md);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}
        
        .btn-modern:hover {{
            background: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
            color: var(--text-inverse);
        }}
        
        .btn-export {{
            background: var(--success-color);
        }}
        
        .btn-export:hover {{
            background: #047857;
        }}
        
        .btn-reset {{
            background: var(--secondary-color);
        }}
        
        .btn-reset:hover {{
            background: #475569;
        }}
        
        .table-container {{
            background: var(--bg-primary);
            border: 1px solid var(--border-light);
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }}
        
        .data-table {{
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-primary);
        }}
        
        .data-table thead {{
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .data-table th {{
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: none;
            border-bottom: 1px solid var(--border-light);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 1.25rem 1rem;
            font-size: 0.8rem;
            white-space: nowrap;
        }}
        
        .data-table td {{
            padding: 1rem;
            border-bottom: 1px solid var(--border-light);
            vertical-align: middle;
            transition: all 0.2s ease;
            background: var(--bg-primary);
            color: var(--text-primary);
        }}
        
        .data-table tbody tr {{
            transition: all 0.2s ease;
            cursor: pointer;
            background: var(--bg-primary);
        }}
        
        .data-table tbody tr:nth-child(even) {{
            background: var(--bg-secondary);
        }}
        
        .data-table tbody tr:nth-child(even) td {{
            background: var(--bg-secondary);
            color: var(--text-primary);
        }}
        
        .data-table tbody tr:hover {{
            background: var(--bg-accent) !important;
            transform: scale(1.001);
        }}
        
        .data-table tbody tr:hover td {{
            background: var(--bg-accent) !important;
            color: var(--text-primary);
        }}
        
        .section-title {{
            color: var(--text-primary);
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .section-title i {{
            color: var(--primary-color);
        }}
        
        .floating-action {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 1000;
        }}
        
        .fab {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--primary-color);
            border: none;
            color: var(--text-inverse);
            font-size: 1.5rem;
            box-shadow: var(--shadow-lg);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }}
        
        .fab:hover {{
            transform: scale(1.1);
            box-shadow: var(--shadow-xl);
            background: var(--primary-hover);
        }}
        
        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }}
        
        .loading-overlay.show {{
            opacity: 1;
            visibility: visible;
        }}
        
        .loading-spinner {{
            width: 60px;
            height: 60px;
            border: 4px solid var(--border-light);
            border-left: 4px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .filter-row {{
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-light);
        }}
        
        .footer {{
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-light);
            padding: 2rem;
            margin-top: 3rem;
            text-align: center;
        }}
        
        .footer-link {{
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            margin: 0 0.5rem;
        }}
        
        .footer-link:hover {{
            color: var(--primary-color);
            background: var(--bg-accent);
            transform: translateY(-1px);
        }}
        
        .footer-credit {{
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.95rem;
        }}
        
        .footer i {{
            font-size: 1rem;
        }}
        
        /* Focus styles for accessibility */
        .btn-modern:focus,
        .search-input:focus,
        .filter-select:focus,
        .theme-toggle:focus,
        .fab:focus {{
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
        }}
        
        /* Smooth transitions for theme switching */
        * {{
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }}
        
        @media (max-width: 768px) {{
            .main-container {{
                margin: 1rem;
                padding: 1.5rem;
            }}
            
            .page-title {{
                font-size: 2rem;
            }}
            
            .stats-container {{
                gap: 1rem;
            }}
            
            .stats-card {{
                min-width: 150px;
                padding: 1.5rem;
            }}
            
            .stats-number {{
                font-size: 2rem;
            }}
            
            .controls-section {{
                padding: 1.5rem;
            }}
            
            .floating-action {{
                bottom: 1rem;
                right: 1rem;
            }}
            
            .fab {{
                width: 50px;
                height: 50px;
                font-size: 1.25rem;
            }}
            
            .theme-toggle {{
                position: relative;
                margin-bottom: 1rem;
            }}
        }}
        
        @media (max-width: 576px) {{
            .page-title {{
                font-size: 1.75rem;
            }}
            
            .btn-modern {{
                padding: 0.75rem 1.5rem;
                font-size: 0.875rem;
            }}
            
            .data-table th,
            .data-table td {{
                padding: 0.75rem 0.5rem;
                font-size: 0.875rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="main-container">
            <!-- Page Header -->
            <div class="page-header">
                <button class="theme-toggle" id="theme-toggle" title="Toggle theme">
                    <i class="bi bi-moon-fill" id="theme-icon"></i>
                </button>
                <h1 class="page-title">
                    <i class="bi bi-table"></i> {title}
                </h1>
                <p class="page-subtitle">Interactive data visualization with advanced filtering and search capabilities</p>
            </div>
            
            <!-- Statistics -->
            <div class="stats-container">
                <div class="stats-card">
                    <div class="stats-number" id="total-rows">{len(df)}</div>
                    <div class="stats-label">Total Rows</div>
                </div>
                <div class="stats-card">
                    <div class="stats-number">{len(df.columns)}</div>
                    <div class="stats-label">Columns</div>
                </div>
                <div class="stats-card">
                    <div class="stats-number" id="filtered-rows">{len(df)}</div>
                    <div class="stats-label">Filtered Rows</div>
                </div>
            </div>
            
            <!-- Controls Section -->
            <div class="controls-section">
                <div class="search-container">
                    <h5 class="section-title">
                        <i class="bi bi-search"></i>
                        Search & Filter
                    </h5>
                    <div class="row g-3 align-items-end">
                        <div class="col-md-8">
                            <label for="search-input" class="form-label fw-bold">Global Search</label>
                            <input type="text" class="form-control search-input" id="search-input" 
                                   placeholder="Search across all columns...">
                        </div>
                        <div class="col-md-4">
                            <div class="d-flex gap-2">
                                <button class="btn btn-modern btn-reset flex-fill" onclick="clearAllFilters()">
                                    <i class="bi bi-arrow-clockwise"></i> Reset
                                </button>
                                <button class="btn btn-modern btn-export flex-fill" onclick="exportToCSV()">
                                    <i class="bi bi-download"></i> Export
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="filter-row">
                    <h6 class="section-title">
                        <i class="bi bi-funnel"></i>
                        Column Filters
                    </h6>
                    <div class="row g-3">
                        {filter_dropdowns}
                    </div>
                </div>
            </div>
            
            <!-- Data Table -->
            <div class="table-container">
                <div class="table-responsive">
                    {table_html}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Floating Action Button -->
    <div class="floating-action">
        <button class="fab" onclick="scrollToTop()" title="Scroll to top">
            <i class="bi bi-arrow-up"></i>
        </button>
    </div>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row align-items-center justify-content-center text-center">
                <div class="col-md-4 mb-3 mb-md-0">
                    <a href="https://github.com/krystianbajno/csvhtml" target="_blank" class="footer-link">
                        <i class="bi bi-github"></i>
                        GitHub Repository
                    </a>
                </div>
                <div class="col-md-4 mb-3 mb-md-0">
                    <a href="https://csv.baycode.eu" target="_blank" class="footer-link">
                        <i class="bi bi-globe"></i>
                        csv.baycode.eu
                    </a>
                </div>
                <div class="col-md-4">
                    <span class="footer-credit">
                        Made with <i class="bi bi-heart-fill text-danger"></i> Krystian Bajno 2025
                    </span>
                </div>
            </div>
        </div>
    </footer>
    
    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loading-overlay">
        <div class="text-center text-white">
            <div class="loading-spinner mb-3"></div>
            <h5>Processing data...</h5>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Theme management
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const body = document.body;
        
        // Load saved theme or default to light
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);
        
        themeToggle.addEventListener('click', () => {{
            const currentTheme = body.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            setTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        }});
        
        function setTheme(theme) {{
            body.setAttribute('data-theme', theme);
            themeIcon.className = theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill';
        }}
        
        // Initialize data
        const tableElement = document.getElementById('{table_id}');
        const originalRows = Array.from(tableElement.querySelectorAll('tbody tr'));
        let filteredRows = [...originalRows];
        
        // Search functionality
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', function() {{
            showLoadingOverlay();
            setTimeout(() => {{
                applyFilters();
                hideLoadingOverlay();
            }}, 100);
        }});
        
        // Filter functionality
        const filterSelects = document.querySelectorAll('.filter-select');
        filterSelects.forEach(select => {{
            select.addEventListener('change', function() {{
                showLoadingOverlay();
                setTimeout(() => {{
                    applyFilters();
                    hideLoadingOverlay();
                }}, 100);
            }});
        }});
        
        function applyFilters() {{
            const searchTerm = searchInput.value.toLowerCase();
            let rows = [...originalRows];
            
            // Apply column filters
            filterSelects.forEach(select => {{
                const columnIndex = parseInt(select.getAttribute('data-column'));
                const filterValue = select.value;
                
                if (filterValue) {{
                    rows = rows.filter(row => {{
                        const cellText = row.cells[columnIndex].textContent.trim();
                        return cellText === filterValue;
                    }});
                }}
            }});
            
            // Apply search filter
            if (searchTerm) {{
                rows = rows.filter(row => {{
                    return Array.from(row.cells).some(cell => 
                        cell.textContent.toLowerCase().includes(searchTerm)
                    );
                }});
            }}
            
            filteredRows = rows;
            updateTableDisplay();
            updateStats();
        }}
        
        function updateTableDisplay() {{
            const tbody = tableElement.querySelector('tbody');
            
            // Hide all rows
            originalRows.forEach(row => {{
                row.style.display = 'none';
            }});
            
            // Show filtered rows
            filteredRows.forEach(row => {{
                row.style.display = '';
            }});
            
            // Add animation
            filteredRows.forEach((row, index) => {{
                row.style.animation = 'none';
                row.offsetHeight; // Trigger reflow
                row.style.animation = `fadeInUp 0.3s ease ${{index * 0.02}}s both`;
            }});
        }}
        
        function updateStats() {{
            document.getElementById('filtered-rows').textContent = filteredRows.length;
        }}
        
        function clearAllFilters() {{
            showLoadingOverlay();
            
            setTimeout(() => {{
                searchInput.value = '';
                filterSelects.forEach(select => {{
                    select.value = '';
                }});
                
                filteredRows = [...originalRows];
                updateTableDisplay();
                updateStats();
                hideLoadingOverlay();
            }}, 300);
        }}
        
        function exportToCSV() {{
            showLoadingOverlay();
            
            setTimeout(() => {{
                const headers = Array.from(tableElement.querySelectorAll('thead th')).map(th => th.textContent);
                const rows = filteredRows.map(row => 
                    Array.from(row.cells).map(cell => `"${{cell.textContent.replace(/"/g, '""')}}"`)
                );
                
                const csvContent = [
                    headers.join(','),
                    ...rows.map(row => row.join(','))
                ].join('\\n');
                
                const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'exported_data.csv';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                hideLoadingOverlay();
            }}, 500);
        }}
        
        function scrollToTop() {{
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }}
        
        function showLoadingOverlay() {{
            document.getElementById('loading-overlay').classList.add('show');
        }}
        
        function hideLoadingOverlay() {{
            document.getElementById('loading-overlay').classList.remove('show');
        }}
        
        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        `;
        document.head.appendChild(style);
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {{
            updateStats();
            
            // Add smooth scrolling to table on mobile
            if (window.innerWidth <= 768) {{
                const tableContainer = document.querySelector('.table-responsive');
                if (tableContainer) {{
                    tableContainer.style.scrollBehavior = 'smooth';
                }}
            }}
        }});
        
        // Handle responsive behavior
        window.addEventListener('resize', function() {{
            if (window.innerWidth <= 768) {{
                const fab = document.querySelector('.fab');
                if (fab) {{
                    fab.style.transform = 'scale(0.9)';
                }}
            }} else {{
                const fab = document.querySelector('.fab');
                if (fab) {{
                    fab.style.transform = 'scale(1)';
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html_template


def create_html_from_csv(csv_file, table_id="data-table", title="Data Table"):
    """
    Create HTML from CSV file content.
    """
    try:
        # Try to read the CSV with different encodings and separators
        df = repair_and_read_csv(csv_file)
        
        if df is None or df.empty:
            raise ValueError("Could not read CSV file or file is empty")
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Clean data
        df = df.fillna('')
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        return create_enhanced_html_template(df, table_id, title)
        
    except Exception as e:
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>Error processing CSV file</h2>
                <p><strong>Error:</strong> {str(e)}</p>
            </div>
        </body>
        </html>
        """
        return error_html


def convert_csv_to_html(input_file, output_file=None, title=None):
    """
    Convert CSV file to enhanced HTML with improved styling.
    """
    try:
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file '{input_file}' not found")
        
        if not input_path.suffix.lower() == '.csv':
            raise ValueError("Input file must be a CSV file")
        
        # Generate output filename if not provided
        if output_file is None:
            output_file = input_path.with_suffix('.html')
        
        # Generate title if not provided
        if title is None:
            title = f"Data from {input_path.stem}"
        
        print(f"Reading CSV file: {input_file}")
        
        # Read and process the CSV
        html_content = create_html_from_csv(input_file, title=title)
        
        print(f"Writing HTML file: {output_file}")
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Successfully converted '{input_file}' to '{output_file}'")
        print(f"📊 Open '{output_file}' in your web browser to view the interactive table")
        
        return str(output_file)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def repair_and_read_csv(csv_file):
    """
    Attempt to read CSV with various encodings and delimiters.
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    delimiters = [',', ';', '\t', '|']
    
    for encoding in encodings:
        for delimiter in delimiters:
            try:
                df = pd.read_csv(csv_file, encoding=encoding, sep=delimiter, 
                               skipinitialspace=True, quotechar='"')
                
                # Check if the DataFrame looks reasonable
                if len(df.columns) > 1 and len(df) > 0:
                    # Check if most values in first row are not NaN
                    first_row_valid = df.iloc[0].notna().sum() / len(df.columns) > 0.5
                    if first_row_valid:
                        print(f"✅ Successfully read CSV with encoding: {encoding}, delimiter: '{delimiter}'")
                        return df
                        
            except (UnicodeDecodeError, pd.errors.EmptyDataError, pd.errors.ParserError):
                continue
    
    # If all else fails, try to read as a simple text file and parse manually
    try:
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if len(lines) < 2:
            return None
        
        # Try to detect delimiter from first line
        first_line = lines[0]
        delimiter = ','
        for d in [';', '\t', '|', ',']:
            if d in first_line:
                delimiter = d
                break
        
        # Parse manually
        data = []
        headers = [h.strip().strip('"') for h in lines[0].split(delimiter)]
        
        for line in lines[1:]:
            row = [cell.strip().strip('"') for cell in line.split(delimiter)]
            if len(row) == len(headers):
                data.append(row)
        
        if data:
            df = pd.DataFrame(data, columns=headers)
            print(f"✅ Successfully parsed CSV manually with delimiter: '{delimiter}'")
            return df
            
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced CSV to HTML Table Converter with modern styling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python csvhtml_enhanced.py data.csv
    python csvhtml_enhanced.py data.csv output.html
    python csvhtml_enhanced.py data.csv --title "Sales Report"
        """
    )
    
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('output_file', nargs='?', help='Output HTML file path (optional)')
    parser.add_argument('--title', '-t', help='Custom title for the HTML page')
    parser.add_argument('--version', action='version', version='Enhanced CSV to HTML Converter 2.0')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    try:
        result = convert_csv_to_html(
            input_file=args.input_file,
            output_file=args.output_file,
            title=args.title
        )
        
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
