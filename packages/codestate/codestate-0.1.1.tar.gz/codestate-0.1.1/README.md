# CodeState CLI

[![Code Size](https://img.shields.io/github/languages/code-size/HenryLok0/CodeState?style=flat-square&logo=github)](https://github.com/HenryLok0/CodeState)
![PyPI - Version](https://img.shields.io/pypi/v/CodeState)

[![MIT License](https://img.shields.io/github/license/HenryLok0/CodeState?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/HenryLok0/CodeState?style=flat-square)](https://github.com/HenryLok0/CodeState/stargazers)

A CLI tool that analyzes your local codebase and generates detailed statistics, such as lines of code per file type, function complexity, comment density, and more. It visualizes the data as ASCII charts or exports to JSON, HTML, or Markdown for further use. This tool is designed for developers who want quick insights into their project's structure without relying on external services.

## Installation

```bash
pip install codestate
```

Or for local development:

```bash
pip install .
```

## Usage

```bash
codestate [directory] [options]
```

### Options
- `directory`         Target directory to analyze (default: current directory)
- `--exclude`         Directories to exclude (space separated, e.g. --exclude .git venv node_modules)
- `--ext`             File extensions to include (e.g. --ext .py .js)
- `--json`            Export result as JSON
- `--html`            Export result as HTML table
- `--md`              Export result as Markdown table
- `--details`         Show detailed statistics for each file
- `--dup`             Show duplicate code blocks (5+ lines)
- `--maxmin`          Show file with most/least lines
- `--authors`         Show git main author and last modifier for each file
- `--langdist`        Show language (file extension) distribution as ASCII pie chart

## Features
- Count lines of code per file type
- Analyze function/method complexity
- Calculate comment density
- Show average function length
- Detect and count TODO/FIXME comments
- Exclude specific directories from analysis
- Multithreaded for fast analysis of large projects
- Visualize results as ASCII bar charts in the terminal
- Export results as JSON, HTML, or Markdown tables
- Show per-file detailed statistics with `--details`
- Detect duplicate code blocks across files (`--dup`)
- Show file with most/least lines (`--maxmin`)
- Show git main author and last modifier for each file (`--authors`)
- Show language distribution as ASCII pie chart (`--langdist`)

## Examples

Analyze the current directory (excluding .git, venv, node_modules by default):
```bash
codestate
```

Analyze a specific directory and exclude build and dist folders:
```bash
codestate myproject --exclude build dist
```

Only analyze Python and JavaScript files:
```bash
codestate --ext .py .js
```

Export results as JSON:
```bash
codestate --json
```

Export results as HTML:
```bash
codestate --html
```

Export results as Markdown:
```bash
codestate --md
```

Show detailed statistics for each file:
```bash
codestate --details
```

Show duplicate code blocks (5+ lines):
```bash
codestate --dup
```

Show file with most/least lines:
```bash
codestate --maxmin
```

Show git main author and last modifier for each file:
```bash
codestate --authors
```

Show language distribution as ASCII pie chart:
```bash
codestate --langdist
```

## Upcoming Features
- Function/class naming convention check (PEP8, camelCase, snake_case, etc.)
- ASCII tree view of project structure
- API/function docstring summary extraction
- Large file/function warning (over threshold lines)
- User-defined regex rules for custom code checks

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you have questions or need help, please open an issue on GitHub.

Thank you to all contributors and the open-source community for your support.