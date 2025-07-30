"""
CLI entry point for codestate.
"""
import sys
import argparse
import json
import os
from .analyzer import Analyzer
from .visualizer import ascii_bar_chart, print_comment_density, html_report, markdown_report, ascii_pie_chart, print_ascii_tree, ascii_complexity_heatmap, generate_markdown_summary, print_table, csv_report

def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='CodeState: Codebase statistics CLI tool')
    parser.add_argument('directory', nargs='?', default='.', help='Target directory to analyze')
    parser.add_argument('--json', action='store_true', help='Export result as JSON')
    parser.add_argument('--html', action='store_true', help='Export result as HTML table')
    parser.add_argument('--md', action='store_true', help='Export result as Markdown table')
    parser.add_argument('--details', action='store_true', help='Show detailed statistics')
    parser.add_argument('--exclude', nargs='*', default=None, help='Directories to exclude (space separated)')
    parser.add_argument('--ext', nargs='*', default=None, help='File extensions to include (e.g. --ext .py .js)')
    parser.add_argument('--dup', action='store_true', help='Show duplicate code blocks (5+ lines)')
    parser.add_argument('--maxmin', action='store_true', help='Show file with most/least lines')
    parser.add_argument('--authors', action='store_true', help='Show git main author and last modifier for each file')
    parser.add_argument('--langdist', action='store_true', help='Show language (file extension) distribution as ASCII pie chart')
    parser.add_argument('--naming', action='store_true', help='Check function/class naming conventions (PEP8, PascalCase)')
    parser.add_argument('--tree', action='store_true', help='Show ASCII tree view of project structure')
    parser.add_argument('--apidoc', action='store_true', help='Show API/function/class docstring summaries')
    parser.add_argument('--warnsize', nargs='*', type=int, help='Warn for large files/functions (optionally specify file and function line thresholds, default 300/50)')
    parser.add_argument('--regex', nargs='+', help='User-defined regex rules for custom code checks (space separated, enclose in quotes)')
    parser.add_argument('--output', '-o', type=str, help='Output file for HTML/Markdown/JSON export')
    parser.add_argument('--hotspot', action='store_true', help='Show most frequently changed files (git hotspots)')
    parser.add_argument('--health', action='store_true', help='Show project health score and suggestions')
    parser.add_argument('--groupdir', action='store_true', help='Show grouped statistics by top-level directory')
    parser.add_argument('--groupext', action='store_true', help='Show grouped statistics by file extension')
    parser.add_argument('--complexitymap', action='store_true', help='Show ASCII heatmap of file complexity')
    parser.add_argument('--deadcode', action='store_true', help='Show unused (dead) functions/classes in Python files')
    parser.add_argument('--ci', action='store_true', help='CI/CD mode: exit non-zero if major issues found')
    parser.add_argument('--summary', action='store_true', help='Generate a markdown project summary (print or --output)')
    parser.add_argument('--typestats', action='store_true', help='Show function parameter/type annotation statistics (Python)')
    parser.add_argument('--security', action='store_true', help='Scan for common insecure patterns and secrets')
    parser.add_argument('--csv', action='store_true', help='Export summary statistics as CSV')
    parser.add_argument('--details-csv', action='store_true', help='Export per-file details as CSV')
    parser.add_argument('--groupdir-csv', action='store_true', help='Export grouped-by-directory stats as CSV')
    parser.add_argument('--groupext-csv', action='store_true', help='Export grouped-by-extension stats as CSV')
    parser.add_argument('--version', action='store_true', help='Show codestate version and exit')
    parser.add_argument('--list-extensions', action='store_true', help='List all file extensions found in the project')
    parser.add_argument('--size', action='store_true', help="Show each file's size in bytes as a table")
    args = parser.parse_args()

    # Analyze codebase
    regex_rules = args.regex if args.regex else None
    analyzer = Analyzer(args.directory, file_types=args.ext, exclude_dirs=args.exclude)
    stats = analyzer.analyze(regex_rules=regex_rules)

    # Prepare data for visualization
    data = []
    for ext, info in stats.items():
        item = {'ext': ext}
        item.update(info)
        data.append(item)

    if args.version:
        print('codestate version 0.1.7')
        sys.exit(0)
    if args.list_extensions:
        # Scan all files and print unique extensions
        exts = set()
        for file_path in analyzer._iter_files(args.directory):
            if file_path.suffix:
                exts.add(file_path.suffix)
        print('File extensions found in project:')
        for ext in sorted(exts):
            print(ext)
        sys.exit(0)

    if args.tree:
        print('Project structure:')
        print_ascii_tree(args.directory)

    if args.html:
        result = html_report(data, title='Code Statistics')
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f'HTML report written to {abs_path}')
        else:
            print(result)
    elif args.md:
        result = markdown_report(data, title='Code Statistics')
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f'Markdown report written to {abs_path}')
        else:
            print(result)
    elif args.json:
        result = json.dumps(data, indent=2, ensure_ascii=False)
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f'JSON report written to {abs_path}')
        else:
            print(result)

    if args.size:
        file_details = analyzer.get_file_details_with_size()
        headers = ["path", "ext", "size", "total_lines", "comment_lines", "function_count"]
        print_table(file_details, headers=headers, title="File Sizes and Stats")
        return

    # Only show default bar chart if no arguments (just 'codestate')
    if len(sys.argv) == 1:
        ascii_bar_chart(data, value_key='total_lines', label_key='ext', title='Lines of Code per File Type')
        print_comment_density(data, label_key='ext')

    if args.langdist:
        ascii_pie_chart(data, value_key='file_count', label_key='ext', title='Language Distribution (by file count)')
    if args.details:
        print("\nFile Details:")
        file_details = analyzer.get_file_details()
        if file_details:
            headers = ["path", "ext", "total_lines", "comment_lines", "function_count", "complexity", "function_avg_length", "todo_count", "blank_lines", "comment_only_lines", "code_lines"]
            print_table(file_details, headers=headers, title=None)
        else:
            print("No file details available.")
    if args.dup:
        dups = analyzer.get_duplicates()
        print(f"\nDuplicate code blocks (block size >= 5 lines, found {len(dups)} groups):")
        for group in dups:
            print("---")
            for path, line, block in group:
                print(f"File: {path}, Start line: {line}")
                print(block)
    if args.maxmin:
        mm = analyzer.get_max_min_stats()
        print("\nFile with most lines:")
        print(mm['max_file'])
        print("File with least lines:")
        print(mm['min_file'])
    if args.authors:
        authors = analyzer.get_git_authors()
        if authors is None:
            print("No .git directory found or not a git repo.")
        else:
            print("\nGit authorship info:")
            for path, info in authors.items():
                print(f"{path}: main_author={info['main_author']}, last_author={info['last_author']}")
    if args.naming:
        violations = analyzer.get_naming_violations()
        if not violations:
            print('All function/class names follow conventions!')
        else:
            print('\nNaming convention violations:')
            for v in violations:
                print(f"{v['type']} '{v['name']}' in {v['file']} (line {v['line']}): should be {v['rule']}")
    if args.apidoc:
        api_docs = analyzer.get_api_doc_summaries()
        if not api_docs:
            print('No API docstrings found.')
        else:
            print('\nAPI/function/class docstring summaries:')
            for d in api_docs:
                print(f"{d['type']} '{d['name']}' in {d['file']} (line {d['line']}):\n{d['docstring']}\n")
    if args.warnsize is not None:
        threshold_file = args.warnsize[0] if len(args.warnsize) > 0 else 300
        threshold_func = args.warnsize[1] if len(args.warnsize) > 1 else 50
        warnings = analyzer.get_large_warnings(threshold_file, threshold_func)
        if not warnings['files'] and not warnings['functions']:
            print(f'No files or functions exceed the thresholds ({threshold_file} lines for files, {threshold_func} for functions).')
        else:
            if warnings['files']:
                print(f'\nLarge files (>{threshold_file} lines):')
                for w in warnings['files']:
                    print(f"{w['file']} - {w['lines']} lines")
            if warnings['functions']:
                print(f'\nLarge functions (>{threshold_func} lines):')
                for w in warnings['functions']:
                    print(f"{w['function']} in {w['file']} (line {w['line']}) - {w['lines']} lines")
    if regex_rules:
        matches = analyzer.get_regex_matches()
        if not matches:
            print('No matches found for custom regex rules.')
        else:
            print('\nCustom regex matches:')
            for m in matches:
                print(f"{m['file']} (line {m['line']}): [{m['rule']}] {m['content']}")
    if args.hotspot:
        hotspots = analyzer.get_git_hotspots(top_n=10)
        if not hotspots:
            print('No git hotspot data found (not a git repo or no commits).')
        else:
            print('\nGit Hotspots (most frequently changed files):')
            for path, count in hotspots:
                print(f'{path}: {count} commits')
    if args.health:
        report = analyzer.get_health_report()
        if not report:
            print('No health report available.')
        else:
            print(f"\nProject Health Score: {report['score']} / 100")
            print(f"Average comment density: {report['avg_comment_density']:.2%}")
            print(f"Average function complexity: {report['avg_complexity']:.2f}")
            print(f"TODO/FIXME count: {report['todo_count']}")
            print(f"Naming violations: {report['naming_violations']}")
            print(f"Duplicate code blocks: {report['duplicate_blocks']}")
            print(f"Large files: {report['large_files']}")
            print(f"Large functions: {report['large_functions']}")
            if report['suggestions']:
                print("\nSuggestions:")
                for s in report['suggestions']:
                    print(f"- {s}")
            else:
                print("\nNo major issues detected. Great job!")
    if args.complexitymap:
        ascii_complexity_heatmap(analyzer.get_file_details(), title='File Complexity Heatmap')
    if args.deadcode:
        unused = analyzer.get_unused_defs()
        if not unused:
            print('No unused (dead) functions/classes found.')
        else:
            print('\nUnused (dead) functions/classes:')
            for d in unused:
                print(f"{d['type']} '{d['name']}' in {d['file']} (line {d['line']})")
    if args.typestats:
        stats = analyzer.get_api_param_type_stats()
        print('\nFunction Parameter/Type Annotation Statistics:')
        print(f"Total functions: {stats.get('total_functions', 0)}")
        print(f"Total parameters: {stats.get('total_parameters', 0)}")
        print(f"Annotated parameters: {stats.get('annotated_parameters', 0)}")
        print(f"Annotated returns: {stats.get('annotated_returns', 0)}")
        print(f"Parameter annotation coverage: {stats.get('param_annotation_coverage', 0):.2%}")
        print(f"Return annotation coverage: {stats.get('return_annotation_coverage', 0):.2%}")
    if args.groupdir:
        grouped = analyzer.get_grouped_stats(by='dir')
        print('\nGrouped statistics by top-level directory:')
        rows = []
        for d, stats in grouped.items():
            row = {'dir': d}
            row.update(stats)
            rows.append(row)
        print_table(rows, headers=["dir", "file_count", "total_lines", "comment_lines", "function_count"])
    if args.groupext:
        grouped = analyzer.get_grouped_stats(by='ext')
        print('\nGrouped statistics by file extension:')
        rows = []
        for ext, stats in grouped.items():
            row = {'ext': ext}
            row.update(stats)
            rows.append(row)
        print_table(rows, headers=["ext", "file_count", "total_lines", "comment_lines", "function_count"])

    if args.csv:
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_report(data))
            print(f'CSV report written to {abs_path}')
        else:
            print(csv_report(data))
    if args.details_csv:
        file_details = analyzer.get_file_details()
        headers = ["path", "ext", "total_lines", "comment_lines", "function_count", "complexity", "function_avg_length", "todo_count", "blank_lines", "comment_only_lines", "code_lines"]
        csv_str = csv_report(file_details, headers=headers)
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_str)
            print(f'Details CSV written to {abs_path}')
        else:
            print(csv_str)
    if args.groupdir_csv:
        grouped = analyzer.get_grouped_stats(by='dir')
        rows = []
        for d, stats in grouped.items():
            row = {'dir': d}
            row.update(stats)
            rows.append(row)
        csv_str = csv_report(rows, headers=["dir", "file_count", "total_lines", "comment_lines", "function_count"])
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_str)
            print(f'Grouped-by-directory CSV written to {abs_path}')
        else:
            print(csv_str)
    if args.groupext_csv:
        grouped = analyzer.get_grouped_stats(by='ext')
        rows = []
        for ext, stats in grouped.items():
            row = {'ext': ext}
            row.update(stats)
            rows.append(row)
        csv_str = csv_report(rows, headers=["ext", "file_count", "total_lines", "comment_lines", "function_count"])
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_str)
            print(f'Grouped-by-extension CSV written to {abs_path}')
        else:
            print(csv_str)

    if args.ci:
        # Criteria: health score < 80, or any naming violations, large files/functions, or dead code
        report = analyzer.get_health_report()
        naming_violations = analyzer.get_naming_violations()
        large_warn = analyzer.get_large_warnings()
        deadcode = analyzer.get_unused_defs()
        fail = False
        reasons = []
        if report and report['score'] < 80:
            fail = True
            reasons.append(f"Health score too low: {report['score']}")
        if naming_violations:
            fail = True
            reasons.append(f"Naming violations: {len(naming_violations)}")
        if large_warn['files'] or large_warn['functions']:
            fail = True
            reasons.append(f"Large files: {len(large_warn['files'])}, Large functions: {len(large_warn['functions'])}")
        if deadcode:
            fail = True
            reasons.append(f"Dead code: {len(deadcode)} unused functions/classes")
        if fail:
            print("\nCI/CD check failed due to:")
            for r in reasons:
                print(f"- {r}")
            sys.exit(1)
        else:
            print("\nCI/CD check passed. No major issues detected.")
            sys.exit(0)

    if args.summary:
        hotspots = analyzer.get_git_hotspots(top_n=10)
        summary_md = generate_markdown_summary(stats, analyzer.get_health_report(), hotspots)
        if args.output:
            abs_path = os.path.abspath(args.output)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(summary_md)
            print(f'Markdown project summary written to {abs_path}')
        else:
            print(summary_md)

    if args.security:
        issues = analyzer.get_security_issues()
        if not issues:
            print('No security issues detected.')
        else:
            print('\nSecurity issues detected:')
            for i in issues:
                print(f"{i['file']} (line {i['line']}): {i['desc']}\n    {i['content']}")
                if 'note' in i:
                    print(f"    Note: {i['note']}")

if __name__ == "__main__":
    main() 