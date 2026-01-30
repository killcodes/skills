#!/usr/bin/env python3
"""
JStack Analyzer Skill
Analyzes jstack command output and generates HTML reports
"""

import re
import os
import sys
import argparse
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional

class ThreadInfo:
    def __init__(self, name: str, thread_id: str, daemon: bool, 
                 priority: str, os_prio: str, tid: str, nid: str, 
                 state: str, stack_trace: List[str]):
        self.name = name
        self.thread_id = thread_id
        self.daemon = daemon
        self.priority = priority
        self.os_prio = os_prio
        self.tid = tid
        self.nid = nid
        self.state = state
        self.stack_trace = stack_trace

class JStackAnalyzer:
    def __init__(self, input_file: str):
        self.input_file = input_file
        self.threads: List[ThreadInfo] = []
        self.timestamp = None
        self.jvm_info = None
        
    def parse_jstack_output(self) -> None:
        """Parse jstack output file"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract timestamp and JVM info
        lines = content.split('\n')
        for line in lines[:10]:
            if 'Full thread dump' in line:
                self.jvm_info = line.strip()
            elif re.match(r'\d{4}-\d{2}-\d{2}', line):
                self.timestamp = line.strip()
        
        # Parse thread information
        thread_blocks = self._split_thread_blocks(content)
        
        for block in thread_blocks:
            thread = self._parse_thread_block(block)
            if thread:
                self.threads.append(thread)
    
    def _split_thread_blocks(self, content: str) -> List[str]:
        """Split content into individual thread blocks"""
        # Thread blocks start with " (thread name)
        pattern = r'^"([^"]+)"'
        blocks = []
        current_block = ""
        
        for line in content.split('\n'):
            if re.match(pattern, line) and current_block:
                blocks.append(current_block.strip())
                current_block = line
            else:
                current_block += "\n" + line if current_block else line
        
        if current_block.strip():
            blocks.append(current_block.strip())
        
        return blocks
    
    def _parse_thread_block(self, block: str) -> Optional[ThreadInfo]:
        """Parse a single thread block"""
        lines = block.split('\n')
        if not lines:
            return None
        
        # Parse thread header line
        header_line = lines[0]
        header_pattern = r'^"([^"]+)"\s+#(\d+)\s+(daemon\s+)?prio=(\d+)\s+os_prio=(\d+)\s+tid=0x([0-9a-f]+)\s+nid=(0x[0-9a-f]+)\s+(.+?)(?:\s+\[0x([0-9a-f]+)\])?$'
        
        match = re.match(header_pattern, header_line.strip())
        if not match:
            return None
        
        name, thread_id, daemon_str, priority, os_prio, tid, nid, status, _ = match.groups()
        daemon = daemon_str is not None
        
        # Parse thread state
        state = "UNKNOWN"
        stack_trace = []
        
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('java.lang.Thread.State:'):
                state = line.replace('java.lang.Thread.State:', '').strip()
            elif line.startswith('at ') or line.startswith('- '):
                stack_trace.append(line)
        
        return ThreadInfo(name, thread_id, daemon, priority, os_prio, 
                          tid, nid, state, stack_trace)
    
    def analyze_threads(self) -> Dict:
        """Analyze threads and generate statistics"""
        stats = {
            'total_threads': len(self.threads),
            'daemon_threads': sum(1 for t in self.threads if t.daemon),
            'non_daemon_threads': sum(1 for t in self.threads if not t.daemon),
            'states': Counter(t.state for t in self.threads),
            'thread_groups': defaultdict(list),
            'blocked_threads': [],
            'waiting_threads': [],
            'runnable_threads': [],
            'stack_traces': Counter()
        }
        
        # Group threads by name patterns
        for thread in self.threads:
            # Extract thread group/pattern from name
            group = self._get_thread_group(thread.name)
            stats['thread_groups'][group].append(thread)
            
            # Categorize by state
            if 'BLOCKED' in thread.state:
                stats['blocked_threads'].append(thread)
            elif 'WAITING' in thread.state or 'TIMED_WAITING' in thread.state:
                stats['waiting_threads'].append(thread)
            elif 'RUNNABLE' in thread.state:
                stats['runnable_threads'].append(thread)
            
            # Count stack trace patterns
            if thread.stack_trace:
                key = thread.stack_trace[0] if thread.stack_trace else "empty"
                stats['stack_traces'][key] += 1
        
        return stats
    
    def _get_thread_group(self, thread_name: str) -> str:
        """Categorize thread by name pattern"""
        patterns = {
            'nioEventLoopGroup': 'Netty NIO',
            'grpc': 'gRPC',
            'OkHttp': 'OkHttp',
            'pool-': 'Thread Pool',
            'Keep-Alive': 'HTTP Keep-Alive',
            'Attach Listener': 'JVM Attach',
            'Finalizer': 'JVM Finalizer',
            'Reference Handler': 'JVM Reference',
            'Signal Dispatcher': 'JVM Signal',
            'C2 CompilerThread': 'JIT Compiler',
            'VM Thread': 'JVM VM',
            'Safepoint': 'JVM Safepoint'
        }
        
        for pattern, group in patterns.items():
            if pattern in thread_name:
                return group
        
        return 'Other'
    
    def generate_html_report(self, output_file: str, theme: str = "minimal") -> None:
        """Generate HTML analysis report with frontend-design styling"""
        try:
            from frontend_design_integration import FrontendDesignStyling
        except ImportError:
            print("Error: Frontend design integration not available")
            raise ImportError("Frontend design integration module is required")
            
        stats = self.analyze_threads()
        theme_info = FrontendDesignStyling.get_theme_info()
        selected_theme = theme if theme in theme_info else "industrial"
        theme_description = theme_info[selected_theme]["description"]
        
        # Set card index variables for staggered animations
        card_indices = ""
        for i in range(20):  # Enough for most stat cards
            card_indices += f".stat-card:nth-child({i+1}) {{ --card-index: {i}; }}\n"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 JStack Analysis Report | Thread Forensics</title>
    <style>
        {FrontendDesignStyling.generate_enhanced_css(selected_theme)}
        {card_indices}
        .theme-info {{
            text-align: center;
            margin: 15px 0;
            font-style: italic;
            color: #586069;
            font-size: 13px;
        }}
        .chart-item {{
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .chart-label {{
            min-width: 150px;
            font-weight: 600;
            color: #1a202c;
            font-size: 12px;
        }}
        .chart-bar-wrapper {{
            flex: 1;
            max-width: 400px;
        }}
        .chart-value {{
            min-width: 100px;
            text-align: right;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            color: #2563eb;
            font-size: 12px;
        }}
        .expandable:hover td {{
            color: #1a202c !important;
        }}
        .thread-table tbody tr:hover td {{
            color: #1a202c !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 JStack Analysis Report</h1>
            <div class="theme-info">{theme_description}</div>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            {f'<p><strong>Original Timestamp:</strong> {self.timestamp}</p>' if self.timestamp else ''}
            {f'<p><strong>JVM Info:</strong> {self.jvm_info}</p>' if self.jvm_info else ''}
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Threads</h3>
                <div class="value">{stats['total_threads']}</div>
            </div>
            <div class="stat-card">
                <h3>Daemon Threads</h3>
                <div class="value">{stats['daemon_threads']}</div>
            </div>
            <div class="stat-card">
                <h3>Non-Daemon Threads</h3>
                <div class="value">{stats['non_daemon_threads']}</div>
            </div>
            <div class="stat-card">
                <h3>Blocked Threads</h3>
                <div class="value">{len(stats['blocked_threads'])}</div>
            </div>
        </div>

        <div class="section">
            <h2>📊 Thread State Distribution</h2>
            <div class="chart-container">
"""
        
        # Add state distribution chart
        total = stats['total_threads']
        for state, count in stats['states'].most_common():
            percentage = (count / total) * 100 if total > 0 else 0
            state_class = self._get_state_class(state)
            html_content += f"""
                <div class="chart-item">
                    <div class="chart-label">{state}</div>
                    <div class="chart-bar-wrapper">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {percentage}%;"></div>
                        </div>
                    </div>
                    <div class="chart-value">{count} ({percentage:.1f}%)</div>
                </div>
"""
        
        html_content += """
            </div>
        </div>

        <div class="section">
            <h2>📋 Thread Groups</h2>
            <table class="thread-table">
                <thead>
                    <tr>
                        <th>Thread Group</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for group, threads in sorted(stats['thread_groups'].items(), key=lambda x: len(x[1]), reverse=True):
            percentage = (len(threads) / total) * 100 if total > 0 else 0
            html_content += f"""
                    <tr>
                        <td>{group}</td>
                        <td>{len(threads)}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
"""
        
        html_content += """
                </tbody>
            </table>
        </div>
"""
        
        # Add alerts for potential issues
        if len(stats['blocked_threads']) > 0:
            html_content += f"""
        <div class="alert alert-warning">
            <strong>⚠️ Warning:</strong> Found {len(stats['blocked_threads'])} blocked threads that may indicate contention issues.
        </div>
"""
        
        if len(stats['blocked_threads']) > stats['total_threads'] * 0.1:
            html_content += """
        <div class="alert alert-danger">
            <strong>🚨 Critical:</strong> High percentage of blocked threads detected! This may indicate serious performance issues.
        </div>
"""
        
        # Add detailed thread information
        html_content += f"""
        <div class="section">
            <h2>🧵 Detailed Thread Information</h2>
            <p style="color: var(--neutral); font-style: italic; margin-bottom: 15px; opacity: 0.8;">
                Note: Only showing one representative thread per unique name pattern (regardless of state) to reduce duplication.
            </p>
            <table class="thread-table">
                <thead>
                    <tr>
                        <th>Thread Name</th>
                        <th>ID</th>
                        <th>State</th>
                        <th>Daemon</th>
                        <th>Priority</th>
                        <th>Stack Trace (Top 3)</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Apply deduplication - only show one thread per unique name pattern
        deduplicated_threads = self._deduplicate_threads_by_name_pattern(self.threads)
        
        for thread in sorted(deduplicated_threads, key=lambda t: t.name):
            state_class = self._get_state_class(thread.state)
            daemon_class = 'daemon' if thread.daemon else ''
            
            # Get top 3 stack trace elements
            stack_preview = '<br>'.join(thread.stack_trace[:3]) if thread.stack_trace else 'No stack trace available'
            
            html_content += f"""
                    <tr class="expandable" onclick="this.classList.toggle('show')">
                        <td title="{thread.name}">{thread.name[:50]}{'...' if len(thread.name) > 50 else ''}</td>
                        <td>{thread.thread_id}</td>
                        <td><span class="state-badge {state_class}">{thread.state}</span></td>
                        <td class="{daemon_class}">{'Yes' if thread.daemon else 'No'}</td>
                        <td>{thread.priority}</td>
                        <td><div class="stack-trace">{stack_preview}</div></td>
                    </tr>
"""
        
        html_content += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🔍 Common Stack Trace Patterns</h2>
            <table class="thread-table">
                <thead>
                    <tr>
                        <th>Stack Trace Pattern</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for pattern, count in stats['stack_traces'].most_common(10):
            percentage = (count / total) * 100 if total > 0 else 0
            pattern_display = pattern[:100] + '...' if len(pattern) > 100 else pattern
            html_content += f"""
                    <tr>
                        <td><code>{pattern_display}</code></td>
                        <td>{count}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
"""
        
        html_content += f"""
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>📈 Analysis Summary</h2>
            <div class="alert alert-info">
                <h3>Key Findings:</h3>
                <ul>
                    <li>Total of {stats['total_threads']} threads ({stats['daemon_threads']} daemon, {stats['non_daemon_threads']} non-daemon)</li>
                    <li>{len(stats['runnable_threads'])} threads are currently RUNNABLE</li>
                    <li>{len(stats['waiting_threads'])} threads are in WAITING or TIMED_WAITING state</li>
                    <li>{len(stats['blocked_threads'])} threads are BLOCKED</li>
                    <li>Most common thread state: {stats['states'].most_common(1)[0][0] if stats['states'] else 'N/A'}</li>
                    <li>Largest thread group: {max(stats['thread_groups'].items(), key=lambda x: len(x[1]))[0] if stats['thread_groups'] else 'N/A'}</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Add interactive features
        document.addEventListener('DOMContentLoaded', function() {{
            // Make thread rows expandable to show full details
            const expandableRows = document.querySelectorAll('.expandable');
            expandableRows.forEach(row => {{
                row.style.cursor = 'pointer';
                row.addEventListener('click', function() {{
                    // Toggle expansion logic here if needed
                }});
            }});
        }});
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _deduplicate_threads_by_name_pattern(self, threads: List[ThreadInfo]) -> List[ThreadInfo]:
        """Deduplicate threads by base name pattern only, keeping only one representative per group"""
        seen_groups = set()
        deduplicated_threads = []
        
        for thread in threads:
            # Extract base name pattern (remove numeric suffixes and variations)
            base_name = re.sub(r'-\d+$', '', thread.name)  # Remove suffix like "-1", "-2", etc.
            base_name = re.sub(r'\d+$', '', base_name)     # Remove trailing numbers
            base_name = base_name.strip()
            
            # Create unique key from base name pattern only
            group_key = base_name
            
            if group_key not in seen_groups:
                seen_groups.add(group_key)
                deduplicated_threads.append(thread)
        
        return deduplicated_threads
    
    def _get_state_class(self, state: str) -> str:
        """Get CSS class for thread state"""
        state_lower = state.lower()
        if 'runnable' in state_lower:
            return 'state-runnable'
        elif 'waiting' in state_lower and 'timed' not in state_lower:
            return 'state-waiting'
        elif 'timed_waiting' in state_lower or 'timed waiting' in state_lower:
            return 'state-timed_waiting'
        elif 'blocked' in state_lower:
            return 'state-blocked'
        else:
            return 'state-other'

    def _generate_legacy_html_report(self, output_file: str) -> None:
        """Generate fallback HTML report with legacy styling"""
        # This method can contain the original styling for backward compatibility
        # For now, we'll raise an exception to ensure the new styling is used
        raise ImportError("Frontend design integration is required for HTML generation")

def main():
    parser = argparse.ArgumentParser(description='Analyze jstack output and generate HTML report')
    parser.add_argument('input_file', help='Path to jstack output file')
    parser.add_argument('-o', '--output', default='jstack_report.html', 
                       help='Output HTML file (default: jstack_report.html)')
    parser.add_argument('-t', '--theme', default='minimal', 
                       choices=['minimal', 'modern', 'classic'],
                       help='Design theme for the report (default: minimal)')
    parser.add_argument('--list-themes', action='store_true',
                       help='List available themes and exit')
    
    args = parser.parse_args()
    
    # List themes if requested
    if args.list_themes:
        try:
            from frontend_design_integration import FrontendDesignStyling
            themes = FrontendDesignStyling.get_theme_info()
            print("Available themes:")
            for name, info in themes.items():
                print(f"  {name}: {info['description']}")
        except ImportError:
            print("Error: Theme information not available")
        sys.exit(0)
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    try:
        analyzer = JStackAnalyzer(args.input_file)
        analyzer.parse_jstack_output()
        analyzer.generate_html_report(args.output, args.theme)
        
        print(f"Analysis complete! HTML report generated: {args.output}")
        print(f"Theme: {args.theme}")
        print(f"Analyzed {len(analyzer.threads)} threads")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()