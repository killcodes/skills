#!/usr/bin/env python3
"""
Frontend Design Integration for JStack Analyzer
Implements distinctive, production-grade frontend design principles
"""

class FrontendDesignStyling:
    """Frontend design system following frontend-design skill principles"""
    
    @staticmethod
    def get_typography():
        """Get clean, minimal typography imports"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
        """
    
    @staticmethod
    def get_color_schemes():
        """Get clean, minimal color schemes"""
        return {
            "minimal": {
                "primary": "#2563eb",
                "secondary": "#64748b",
                "accent": "#3b82f6",
                "success": "#10b981",
                "warning": "#f59e0b",
                "danger": "#ef4444",
                "dark": "#1e293b",
                "light": "#f8fafc",
                "neutral": "#64748b",
                "gradient_primary": "linear-gradient(135deg, #2563eb, #3b82f6)",
                "gradient_secondary": "linear-gradient(135deg, #64748b, #94a3b8)",
                "description": "Minimal - Clean, professional design with subtle gradients"
            },
            "modern": {
                "primary": "#059669",
                "secondary": "#374151",
                "accent": "#10b981",
                "success": "#059669",
                "warning": "#d97706",
                "danger": "#dc2626",
                "dark": "#111827",
                "light": "#f9fafb",
                "neutral": "#6b7280",
                "gradient_primary": "linear-gradient(135deg, #059669, #10b981)",
                "gradient_secondary": "linear-gradient(135deg, #374151, #4b5563)",
                "description": "Modern - Contemporary design with green accents"
            },
            "classic": {
                "primary": "#1f2937",
                "secondary": "#4b5563",
                "accent": "#6366f1",
                "success": "#10b981",
                "warning": "#f59e0b",
                "danger": "#ef4444",
                "dark": "#111827",
                "light": "#ffffff",
                "neutral": "#6b7280",
                "gradient_primary": "linear-gradient(135deg, #1f2937, #374151)",
                "gradient_secondary": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                "description": "Classic - Traditional monochrome design with subtle purple accents"
            }
        }
    
    @staticmethod
    def generate_base_css(theme="industrial"):
        """Generate base CSS following frontend-design principles"""
        colors = FrontendDesignStyling.get_color_schemes()[theme]
        
        return f"""
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --success: {colors['success']};
            --warning: {colors['warning']};
            --danger: {colors['danger']};
            --dark: {colors['dark']};
            --light: {colors['light']};
            --neutral: {colors['neutral']};
            --gradient-primary: {colors['gradient_primary']};
            --gradient-secondary: {colors['gradient_secondary']};
            --shadow-color: rgba(0, 0, 0, 0.3);
            --border-radius: 12px;
            --transition-smooth: cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            background: #f5f7fa;
            color: #2c3e50;
            line-height: 1.6;
            overflow-x: auto;
            font-size: 14px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px;
            background: #ffffff;
            color: #2c3e50;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            min-width: 800px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e1e4e8;
        }}
        
        .header h1 {{
            font-family: 'Inter', sans-serif;
            font-size: 28px;
            font-weight: 700;
            margin: 0;
            color: #24292e;
            letter-spacing: -0.01em;
        }}
        
        .header p {{
            color: #586069;
            margin: 10px 0;
            font-size: 14px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: #ffffff;
            padding: 24px;
            border-radius: 6px;
            border: 1px solid #e1e4e8;
            transition: all 0.2s ease;
        }}
        
        .stat-card:hover {{
            border-color: #2563eb;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
        }}
        
        .stat-card h3 {{
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 600;
            margin: 0 0 12px 0;
            color: #586069;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }}
        
        .stat-card .value {{
            font-size: 24px;
            font-weight: 700;
            color: #2563eb;
            font-family: 'Inter', sans-serif;
            line-height: 1;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section h2 {{
            font-family: 'Inter', sans-serif;
            font-size: 20px;
            font-weight: 600;
            color: #24292e;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 8px;
            margin-bottom: 24px;
        }}
        
        .thread-table {{
            width: 100%;
            max-width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: #ffffff;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            overflow: hidden;
            table-layout: fixed;
        }}
        
        .thread-table th,
        .thread-table td {{
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #e1e4e8;
            font-size: 12px;
            color: #2c3e50;
            word-wrap: break-word;
            white-space: normal;
            max-width: 200px;
            overflow: hidden;
        }}
        
        .thread-table th {{
            background: #f6f8fa;
            color: #24292e;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            border-bottom: 2px solid #e1e4e8;
        }}
        
        .thread-table th:nth-child(1),
        .thread-table td:nth-child(1) {{ width: 25%; }}
        .thread-table th:nth-child(2),
        .thread-table td:nth-child(2) {{ width: 8%; }}
        .thread-table th:nth-child(3),
        .thread-table td:nth-child(3) {{ width: 15%; }}
        .thread-table th:nth-child(4),
        .thread-table td:nth-child(4) {{ width: 8%; }}
        .thread-table th:nth-child(5),
        .thread-table td:nth-child(5) {{ width: 8%; }}
        .thread-table th:nth-child(6),
        .thread-table td:nth-child(6) {{ width: 36%; }}
        
        .thread-table tbody tr {{
            transition: background-color 0.2s ease;
        }}
        
        .thread-table tbody tr:hover {{
            background: #f0f4f8;
        }}
        
        .thread-table tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .state-badge {{
            padding: 3px 6px;
            border-radius: 3px;
            font-size: 10px;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.025em;
            border: 1px solid transparent;
            display: inline-block;
            white-space: nowrap;
        }}
        
        .state-runnable {{
            background: #10b981;
            color: white;
            opacity: 0.9;
        }}
        
        .state-waiting {{
            background: #f59e0b;
            color: white;
            opacity: 0.9;
        }}
        
        .state-blocked {{
            background: #ef4444;
            color: white;
            opacity: 0.9;
        }}
        
        .state-timed_waiting {{
            background: #3b82f6;
            color: white;
            opacity: 0.9;
        }}
        
        .state-other {{
            background: #64748b;
            color: white;
            opacity: 0.8;
        }}
        
        .daemon {{
            color: #ef4444;
            font-weight: 500;
        }}
        
        .stack-trace {{
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 10px;
            background: #f6f8fa;
            color: #2c3e50;
            padding: 8px;
            border-radius: 4px;
            max-height: 150px;
            overflow-y: auto;
            border-left: 3px solid #2563eb;
            line-height: 1.3;
            word-break: break-all;
        }}
        
        .stack-trace::-webkit-scrollbar {{
            width: 6px;
        }}
        
        .stack-trace::-webkit-scrollbar-track {{
            background: var(--neutral);
            opacity: 0.2;
        }}
        
        .stack-trace::-webkit-scrollbar-thumb {{
            background: var(--primary);
            opacity: 0.6;
            border-radius: 2px;
        }}
        
        .chart-container {{
            margin: 24px 0;
            padding: 20px;
            background: #f6f8fa;
            border-radius: 6px;
            border: 1px solid #e1e4e8;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 16px;
            background: #e1e4e8;
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .progress-fill {{
            height: 100%;
            background: #2563eb;
            transition: width 0.3s ease;
        }}
        
        .alert {{
            padding: 12px;
            border-radius: 4px;
            margin: 12px 0;
            border-left: 4px solid;
            font-size: 13px;
        }}
        
        .alert-warning {{
            border-left-color: #f59e0b;
            background: #fef3c7;
            color: #92400e;
        }}
        
        .alert-danger {{
            border-left-color: #ef4444;
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .alert-info {{
            border-left-color: #2563eb;
            background: #dbeafe;
            color: #1e40af;
        }}
        
        .expandable {{
            cursor: pointer;
            transition: background-color 0.2s ease;
        }}
        
        .expandable:hover {{
            background: #f6f8fa;
        }}
        
        .expandable:hover td {{
            color: #1a202c !important;
        }}
        
        .thread-table tbody tr:hover td {{
            color: #1a202c !important;
        }}
        
        /* Responsive Design */
        @media (max-width: 1200px) {{
            body {{
                padding: 15px;
            }}
            
            .container {{
                max-width: 100%;
                min-width: auto;
                padding: 20px;
            }}
            
            .thread-table {{
                font-size: 11px;
            }}
            
            .thread-table th,
            .thread-table td {{
                padding: 6px 8px;
                max-width: 150px;
            }}
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .container {{
                padding: 15px;
                border-radius: 0;
            }}
            
            .header h1 {{
                font-size: 18px;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
                gap: 8px;
            }}
            
            .thread-table {{
                font-size: 10px;
                table-layout: auto;
            }}
            
            .thread-table th,
            .thread-table td {{
                padding: 4px 6px;
                max-width: none;
            }}
            
            .thread-table th:nth-child(1),
            .thread-table td:nth-child(1),
            .thread-table th:nth-child(2),
            .thread-table td:nth-child(2),
            .thread-table th:nth-child(3),
            .thread-table td:nth-child(3),
            .thread-table th:nth-child(4),
            .thread-table td:nth-child(4),
            .thread-table th:nth-child(5),
            .thread-table td:nth-child(5),
            .thread-table th:nth-child(6),
            .thread-table td:nth-child(6) {{
                width: auto;
            }}
        }}
        """
    
    @staticmethod
    def generate_enhanced_css(theme="industrial"):
        """Generate complete enhanced CSS with all design principles"""
        base_css = FrontendDesignStyling.generate_base_css(theme)
        typography = FrontendDesignStyling.get_typography()
        
        return f"""
        {typography}
        {base_css}
        """
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convert hex color to RGB values"""
        hex_color = hex_color.lstrip('#')
        return ', '.join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))
    
    @staticmethod
    def get_theme_info():
        """Get information about available themes"""
        return FrontendDesignStyling.get_color_schemes()