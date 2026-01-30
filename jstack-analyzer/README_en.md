# 🔍 JStack Analyzer Skill

JStack Analyzer is a professional Java thread analysis tool that parses jstack command output files and generates detailed HTML analysis reports.

## 📋 Features

- **🔧 Intelligent Parsing**: Automatically parses jstack output files and extracts thread information
- **📊 Visual Reports**: Generates beautiful HTML reports with charts and statistics
- **🎨 Multi-Theme Support**: Offers multiple design themes (minimal, modern, classic)
- **📈 State Analysis**: Detailed analysis of thread state distribution (RUNNABLE, WAITING, BLOCKED, etc.)
- **👥 Thread Grouping**: Smart categorization of threads (Netty NIO, gRPC, OkHttp, Thread Pools, etc.)
- **⚠️ Issue Detection**: Automatically identifies potential thread blocking and performance issues
- **📱 Responsive Design**: Supports viewing on devices with different screen sizes
- **🎯 Deduplication**: Intelligently removes duplicate threads, showing only representative ones

## 🚀 Quick Start

### Requirements

- Python 3.6+
- Standard library dependencies: `re`, `os`, `sys`, `argparse`, `datetime`, `collections`, `pathlib`

### Basic Usage

```bash
# Analyze jstack output file
python jstack-analyzer.py /path/to/jstack_output.txt

# Specify output file name
python jstack-analyzer.py /path/to/jstack_output.txt -o my_report.html

# Choose theme
python jstack-analyzer.py /path/to/jstack_output.txt -t modern

# List all available themes
python jstack-analyzer.py --list-themes
```

### Command Line Arguments

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `input_file` | - | Required | Path to jstack output file |
| `--output` | `-o` | `jstack_report.html` | Output HTML file name |
| `--theme` | `-t` | `minimal` | Design theme |
| `--list-themes` | - | False | List all available themes |

## 🎨 Available Themes

| Theme Name | Description | Characteristics |
|------------|-------------|-----------------|
| `minimal` | Minimal Professional | Clean design with subtle gradients, suitable for enterprise environments |
| `modern` | Modern Fashionable | Green-toned theme with contemporary design style |
| `classic` | Classic Traditional | Monochrome design with purple accents, traditional style |

## 📊 Report Content

The generated HTML report includes the following sections:

### 1. 📈 Statistical Overview
- Total threads count
- Daemon threads count
- Non-daemon threads count
- Blocked threads count

### 2. 📊 Thread State Distribution
- RUNNABLE
- WAITING
- TIMED_WAITING
- BLOCKED
- Visual progress bars showing percentage distribution of each state

### 3. 📋 Thread Group Statistics
Threads grouped by function:
- Netty NIO
- gRPC
- OkHttp
- Thread Pool
- HTTP Keep-Alive
- JVM-related threads (Attach Listener, Finalizer, Reference Handler, etc.)

### 4. 🧵 Detailed Thread Information
Detailed information for each thread:
- Thread name
- Thread ID
- Thread state
- Daemon status
- Priority
- Stack trace (top 3 lines)

### 5. 🔍 Common Stack Patterns
- Most frequently occurring stack traces
- Percentage statistics
- Helps identify hot code spots

### 6. ⚠️ Issue Alerts
- Blocked thread warnings
- High block rate danger alerts
- Performance issue recommendations

## 🛠️ Technical Implementation

### Core Components

1. **ThreadInfo Class**: Encapsulates thread information
2. **JStackAnalyzer Class**: Core analysis engine
3. **FrontendDesignStyling Class**: Frontend styling system

### Analysis Flow

```
Input File → Parse Thread Blocks → Extract Information → Classify Statistics → Generate HTML
```

### Smart Deduplication Algorithm

To avoid displaying too many similar threads in the report, the system:
- Extracts base patterns from thread names
- Removes numeric suffixes and variants
- Shows only one representative thread per pattern

## 📁 File Structure

```
jstack-analyzer/
├── jstack-analyzer.py          # Main entry file
├── scripts/
│   ├── jstack_analyzer.py      # Core analysis logic
│   └── frontend_design_integration.py  # Frontend styling system
└── README.md                   # Documentation file
```

## 🔧 Configuration Options

### Environment Variables

No special environment variable configuration required, runs with Python standard library only.

### Custom Styles

You can customize theme colors by modifying the `get_color_schemes()` method in the `frontend_design_integration.py` file.

## 🐛 Troubleshooting

### Common Issues

1. **File Not Found Error**
   ```
   Error: Input file 'jstack.txt' not found
   ```
   - Check if the file path is correct
   - Ensure the file exists and is readable

2. **Encoding Issues**
   - Ensure jstack output files use UTF-8 encoding
   - Avoid files containing special characters

3. **Insufficient Memory**
   - Large jstack files (>100MB) may require more memory
   - Recommend analyzing on machines with better performance

### Performance Optimization

- System automatically performs thread deduplication when analyzing large files
- Generated HTML files are typically smaller than 5MB
- Supports responsive loading in modern browsers

## 📝 Usage Examples

### Example 1: Basic Analysis
```bash
python jstack-analyzer.py /tmp/app_jstack.txt
```
Generates: `jstack_report.html`

### Example 2: Custom Theme and Output
```bash
python jstack-analyzer.py /tmp/app_jstack.txt -o production_analysis.html -t modern
```
Generates: `production_analysis.html` (modern theme)

### Example 3: View Theme Options
```bash
python jstack-analyzer.py --list-themes
```
Output:
```
Available themes:
  minimal: Minimal - Clean, professional design with subtle gradients
  modern: Modern - Contemporary design with green accents
  classic: Classic - Traditional monochrome design with subtle purple accents
```

## 🤝 Contributing

Issue reports and improvement suggestions are welcome!

### Development Environment Setup

1. Clone the code
2. Ensure Python 3.6+ environment
3. Test with different jstack output files
4. Verify HTML report generation

### Testing

It's recommended to test with jstack outputs from different types of applications:
- Web applications (Tomcat, Spring Boot)
- Microservice applications
- Big data processing applications
- High-concurrency applications

## 📄 License

This project is licensed under the MIT License, see LICENSE file for details.

## 🔗 Related Resources

- [Java Thread Dump Analysis Guide](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/thread002.html)
- [JStack Tool Documentation](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/tooldescr018.html)
- [Java Concurrency Programming Best Practices](https://docs.oracle.com/javase/tutorial/essential/concurrency/)

## 🔄 Version History

- **Version 1.0.0**: Initial release with core functionality
- **Version 1.1.0**: Added multi-theme support and enhanced UI
- **Version 1.2.0**: Improved thread deduplication algorithm and performance

---

**🎯 Tip**: Regularly generating and analyzing thread dumps helps identify and resolve Java application performance issues in a timely manner!