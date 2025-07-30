"""
Visualizer module for ASCII chart output.
"""

import os
import csv
import io

def ascii_bar_chart(data, value_key, label_key='ext', width=40, title=None):
    """
    Print an ASCII bar chart for the given data.
    data: list of dicts or tuples
    value_key: key for the value to visualize (e.g., 'total_lines')
    label_key: key for the label (e.g., file extension)
    width: max width of the bar
    title: optional chart title
    """
    if title:
        print(f"\n{title}")
    if not data:
        print("No data to display.")
        return
    max_value = max(item[value_key] for item in data)
    total = sum(item[value_key] for item in data)
    for item in data:
        label = str(item[label_key]).ljust(8)
        value = item[value_key]
        bar_len = int((value / max_value) * width) if max_value else 0
        bar = '█' * bar_len
        percent = (value / total) * 100 if total else 0
        print(f"{label} | {bar} {value} ({percent:.1f}%)")

def print_comment_density(data, label_key='ext'):
    """
    Print comment density as a percentage bar chart.
    """
    print("\nComment Density:")
    for item in data:
        label = str(item[label_key]).ljust(8)
        density = item.get('comment_density', 0)
        percent = int(density * 100)
        bar = '█' * (percent // 2)
        print(f"{label} | {bar} {percent}%")

def ascii_pie_chart(data, value_key, label_key='ext', title=None):
    """
    Print an ASCII pie chart for language distribution.
    """
    if title:
        print(f"\n{title}")
    total = sum(item[value_key] for item in data)
    for item in data:
        label = str(item[label_key]).ljust(8)
        value = item[value_key]
        percent = (value / total) * 100 if total else 0
        pie = '●' * int(percent // 5)
        print(f"{label} | {pie} {percent:.1f}%")

def ascii_complexity_heatmap(file_details, title=None):
    """
    Print an ASCII heatmap for file/function complexity.
    file_details: list of per-file stats (from analyzer.get_file_details())
    """
    if title:
        print(f"\n{title}")
    if not file_details:
        print("No data to display.")
        return
    # Define thresholds (can be tuned)
    low = 1.5
    high = 3.0
    print(f"{'File':40} | {'Complexity':10} | Heatmap")
    print('-'*65)
    for f in file_details:
        cplx = f.get('complexity', 0)
        if cplx < low:
            symbol = '░'
        elif cplx < high:
            symbol = '▒'
        else:
            symbol = '▓'
        bar = symbol * min(int(cplx * 2), 40)
        print(f"{f['path'][:40]:40} | {cplx:10.2f} | {bar}")

def print_ascii_tree(root_path, max_depth=5, prefix=""):
    """
    Print an ASCII tree view of the directory structure.
    root_path: directory to print
    max_depth: maximum depth to display
    prefix: internal use for recursion
    """
    if max_depth < 0:
        return
    entries = []
    try:
        entries = sorted(os.listdir(root_path))
    except Exception:
        return
    entries = [e for e in entries if not e.startswith('.')]
    for idx, entry in enumerate(entries):
        path = os.path.join(root_path, entry)
        connector = "└── " if idx == len(entries) - 1 else "├── "
        print(prefix + connector + entry)
        if os.path.isdir(path):
            extension = "    " if idx == len(entries) - 1 else "│   "
            print_ascii_tree(path, max_depth-1, prefix + extension)

def html_report(data, title='Code Statistics'):
    """
    Export statistics as an HTML table.
    """
    html = [f'<h2>{title}</h2>', '<table border="1">']
    if data:
        headers = data[0].keys()
        html.append('<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>')
        for item in data:
            html.append('<tr>' + ''.join(f'<td>{item[h]}</td>' for h in headers) + '</tr>')
    html.append('</table>')
    return '\n'.join(html)

def markdown_report(data, title='Code Statistics'):
    """
    Export statistics as a Markdown table.
    """
    md = [f'## {title}\n']
    if data:
        headers = list(data[0].keys())
        md.append('|' + '|'.join(headers) + '|')
        md.append('|' + '|'.join(['---'] * len(headers)) + '|')
        for item in data:
            md.append('|' + '|'.join(str(item[h]) for h in headers) + '|')
    return '\n'.join(md)

def generate_markdown_summary(stats, health_report, hotspots=None):
    """
    Generate a markdown project summary from stats, health report, and hotspots.
    """
    lines = []
    lines.append('# Project Code Summary')
    lines.append('')
    lines.append('## Overall Statistics')
    lines.append('| Extension | Files | Lines | Comments | Functions | TODOs |')
    lines.append('|-----------|-------|-------|----------|-----------|-------|')
    for ext, info in stats.items():
        lines.append(f"| {ext} | {info['file_count']} | {info['total_lines']} | {info['comment_lines']} | {info['function_count']} | {info.get('todo_count', 0)} |")
    lines.append('')
    if health_report:
        lines.append('## Project Health')
        lines.append(f"- **Health Score:** {health_report['score']} / 100")
        lines.append(f"- **Average Comment Density:** {health_report['avg_comment_density']:.2%}")
        lines.append(f"- **Average Function Complexity:** {health_report['avg_complexity']:.2f}")
        lines.append(f"- **TODO/FIXME Count:** {health_report['todo_count']}")
        lines.append(f"- **Naming Violations:** {health_report['naming_violations']}")
        lines.append(f"- **Duplicate Code Blocks:** {health_report['duplicate_blocks']}")
        lines.append(f"- **Large Files:** {health_report['large_files']}")
        lines.append(f"- **Large Functions:** {health_report['large_functions']}")
        if health_report['suggestions']:
            lines.append('### Suggestions:')
            for s in health_report['suggestions']:
                lines.append(f"- {s}")
    if hotspots:
        lines.append('')
        lines.append('## Git Hotspots (Most Frequently Changed Files)')
        lines.append('| File | Commits |')
        lines.append('|------|---------|')
        for path, count in hotspots:
            lines.append(f"| {path} | {count} |")
    return '\n'.join(lines)

def print_table(rows, headers=None, title=None):
    """
    Print a list of dicts as a pretty aligned table.
    """
    if not rows:
        print("No data to display.")
        return
    if headers is None:
        headers = list(rows[0].keys())
    col_widths = [max(len(str(h)), max(len(str(row.get(h, ''))) for row in rows)) for h in headers]
    if title:
        print(f"\n{title}")
    # Print header
    header_line = ' | '.join(str(h).ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print('-+-'.join('-'*w for w in col_widths))
    # Print rows
    for row in rows:
        print(' | '.join(str(row.get(h, '')).ljust(w) for h, w in zip(headers, col_widths)))

def csv_report(data, headers=None):
    """
    Export statistics as a CSV string.
    data: list of dicts
    headers: optional list of column names
    """
    if not data:
        return ''
    if headers is None:
        headers = list(data[0].keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for row in data:
        writer.writerow({h: row.get(h, '') for h in headers})
    return output.getvalue() 