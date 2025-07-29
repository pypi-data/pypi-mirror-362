```
    ╔════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                ║
    ║       █████╗ ██████╗  ██████╗██╗  ██╗██╗████████╗███████╗ ██████╗████████╗     ║
    ║      ██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝     ║
    ║      ███████║██████╔╝██║     ███████║██║   ██║   █████╗  ██║        ██║        ║
    ║      ██╔══██║██╔══██╗██║     ██╔══██║██║   ██║   ██╔══╝  ██║        ██║        ║
    ║      ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║   ███████╗╚██████╗   ██║        ║
    ║      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝        ║
    ║                                                                                ║
    ║                           CLI File structure builder                           ║
    ║                                    v 1.0.0                                     ║
    ╚════════════════════════════════════════════════════════════════════════════════╝
```

Architect is a command-line tool for creating file structures from text representations and scanning existing directories to generate structured outputs.

## Features

- **Create structures** from textual representations (ASCII tree, indented text)
- **Scan directories** and export in multiple formats
- **Interactive mode** with step-by-step wizards
- **Multiple output formats**: ASCII tree, JSON, YAML, XML, Markdown
- **Flexible input support**: spaces, tabs, ASCII tree characters
- **Smart filtering** with customizable ignore patterns
- **Dry-run mode** for safe testing

## Installation

### Option 1: From Source (Recommended)

```bash
cd ~ && git clone https://github.com/mhdgning131/architect.git .architect
cd .architect
sudo chmod +x install.sh
./install.sh
```

After installation, you can use `architect` command globally:

```bash
architect --help
architect scan .
```

## Quick Start

### Create a file structure

```bash
# From a file
architect create -f structure.txt

# From stdin
echo "project/
├── src/
│   └── main.py
└── README.md" | architect create
```

### Scan an existing directory

```bash
# Basic scan
architect scan /path/to/directory

# With options
architect scan . --format json --show-size --max-depth 3
```

### Interactive mode

```bash
architect --interactive
```

## Usage Examples

### Creating Structures

**Input format example:**
```
project/
├── src/
│   ├── components/
│   │   └── Button.js
│   └── utils/
│       └── helpers.js
├── public/
│   └── index.html
└── package.json
```

**Commands:**
```bash
# Create with dry-run
architect create -f structure.txt --dry-run

# Create in specific directory
architect create -f structure.txt -o ./my-project
```

### Scanning Directories

```bash
# Different output formats
architect scan . --format json --output structure.json
architect scan . --format yaml --pretty
architect scan . --format markdown --show-size

# With filtering
architect scan . --ignore "*.log" --ignore "node_modules" --max-depth 2
```

## Output Formats

| Format | Description |
|--------|-------------|
| `tree` | ASCII tree with connecting lines (default) |
| `simple` | Simple indented tree |
| `json` | Structured JSON format |
| `yaml` | YAML format (requires PyYAML) |
| `xml` | XML format |
| `markdown` | Markdown with emoji icons |

## Command Reference

### Create Command
```bash
architect create [OPTIONS]

Options:
  -f, --file PATH     Input file with structure
  -o, --output DIR    Output directory (default: .)
  --dry-run          Simulate without creating files
  -v, --verbose      Detailed parsing output
```

### Scan Command
```bash
architect scan [DIRECTORY] [OPTIONS]

Options:
  --format FORMAT     Output format (tree, simple, json, yaml, xml, markdown)
  -o, --output FILE   Save to file
  --max-depth INT     Maximum scan depth
  --show-size         Show file sizes
  --ignore PATTERN    Patterns to ignore (repeatable)
  --pretty            Pretty print JSON/XML
```
