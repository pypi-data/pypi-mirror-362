# Inspect4j 
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

**Student**: Liru Qu  
**EPCC Supervisor**: Steven Carlysle-Davies

## Overview

`Inspect4j` is a comprehensive static code analysis framework designed to automatically extract metadata, documentation, and structural information from Java code repositories. Built upon the robust `Javalang` parser, the tool provides detailed insights into Java codebases, making it invaluable for software analysis, documentation generation, and code understanding.

## Features

Given a Java project folder, `Inspect4j` will:

- **Code Structure Analysis**:
  - Extract all classes, interfaces, JavaDoc comments and enums with their complete metadata
  - Analyze methods, constructors, and fields including their signatures and modifiers
  - Support nested and anonymous classes, lambda expressions, and local classes
  - Track inheritance hierarchies and interface implementations

- **Dependency Analysis**:
  - Identify all import statements and their types (internal/external)
  - Process wildcard imports and static imports
  - Extract Java project dependencies from Maven (pom.xml) and Gradle (build.gradle) files
  - Classify dependencies by scope and build tool

- **Method Call Analysis**:
  - Extract complete method call lists with proper type resolution
  - Handle method overloading and chain calls accurately
  - Support cross-file method resolution through imports
  - Track constructor calls and super method invocations

- **Annotations Support**:
  - Extract all annotations at class, method, field, and parameter levels
  - Preserve annotation parameters and values

- **Project Metadata**:
  - Extract project directory tree and file hierarchy
  - Detect and analyze software licenses
  - Extract README files and project documentation
  - Retrieve GitHub metadata when available (if a .git folder is in the repository)

- **Advanced Features**:
  - Generate Abstract Syntax Trees (AST) in JSON format
  - Extract source code snippets for each analyzed element
  - Support both single file and directory-wide analysis
  - Generate HTML reports for better visualization

All metadata is extracted and stored as structured JSON files for easy integration with other tools.

## Background

`Inspect4j` draws inspiration from [`Inspect4py`](https://github.com/SoftwareUnderstanding/inspect4py), a successful static analysis framework for Python projects. While maintaining similar command-line interfaces and overall architecture for consistency, `Inspect4j` is built from the ground up to handle Java's unique language features:

- **Parser Differences**: Uses `Javalang` instead of Python's native `ast` library
- **Language-Specific Features**: Handles Java packages, imports, interfaces, annotations, nested structures and method overloading
- **Build System Integration**: Supports Maven and Gradle dependency extraction
- **Type System**: Accounts for Java's static typing and inheritance model

This design ensures that `Inspect4j` and `Inspect4py` can potentially be integrated into a unified multi-language analysis suite while maintaining language-specific accuracy.

## Requirements

- **Python**: 3.8+ (recommended: Python 3.9+)
- **Java Source Code**: Local Java files (.java) on your filesystem
- **Dependencies**: See `requirements.txt` for exact package versions

### Key Dependencies
```
javalang>=0.13.0
click>=8.0.0
pathlib
json2html
requests
gitpython
beautifulsoup4
```

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://git.ecdf.ed.ac.uk/msc-24-25/inspect4j.git
cd inspect4j
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Using pip
```bash
pip install inspect4j
```

## Usage

### Command Line Interface

The tool can analyze individual Java files or entire directory structures:

```bash
inspect4j -i --input_path <FILE.java | DIRECTORY> [OPTIONS]
```

### Basic Examples

**Analyze a single Java file:**
```bash
inspect4j -i MyClass.java
```

**Analyze an entire Java project:**
```bash
inspect4j -i /path/to/java/project -o analysis_results
```

**Generate comprehensive analysis with all features:**
```bash
inspect4j -i ./my-java-project \
    -o ./output \
    -r \
    -html \
    -cl \
    -dt \
    -ast \
    -sc \
    -ld \
    -rm \
    -md
```

### Command Line Options

```
Options:
  -i, --input_path TEXT           Input path of the Java file or directory to
                                  inspect. [required]
  -o, --output_dir TEXT           Output directory path to store results. If
                                  the directory does not exist, the tool will
                                  create it. [default: output_dir]
  -ignore_dir, --ignore_dir_pattern TEXT
                                  Ignore directories starting with a certain
                                  pattern. Can be used multiple times.
                                  [default: .git, target, build, bin]
  -ignore_file, --ignore_file_pattern TEXT
                                  Ignore files starting with a certain pattern.
                                  Can be used multiple times. [default: ., _]
  -r, --requirements              Extract Java project dependencies (Maven/Gradle).
  -html, --html_output            Generate HTML visualization of results.
  -cl, --call_list                Generate method call list analysis.
  -dt, --directory_tree           Extract project directory tree structure.
  -ast, --abstract_syntax_tree    Generate Abstract Syntax Tree in JSON format.
  -sc, --source_code              Include source code in AST nodes.
  -ld, --license_detection        Detect project license automatically.
  -rm, --readme                   Extract all README files in the repository.
  -md, --metadata                 Extract GitHub metadata (requires .git folder).
  --help                          Show help message and exit.
```

## Output Structure

The tool generates structured output in the specified directory:

```
output_dir/
├── directory_info.json          # Repository-level analysis
├── call_graph.json             # Method call relationships
├── call_graph.html             # Interactive call graph visualization
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   └── json_files/
│                       ├── MyClass.json      # Individual class analysis
│                       └── MyInterface.json  # Interface analysis
└── license_info.json           # License detection results
```

### JSON Output Format

Each analyzed Java file produces a detailed JSON structure containing:

```json
{
  "file": {
    "path": "/path/to/MyClass.java",
    "fileNameBase": "MyClass",
    "extension": "java"
  },
  "package": {
    "name": "com.example.myproject"
  },
  "dependencies": [...],           // Import statements
  "classes": {
    "MyClass": {
      "name": "MyClass",
      "modifiers": ["public"],
      "extends": "BaseClass",
      "implements": ["MyInterface"],
      "methods": {...},            // Method details
      "fields": {...},             // Field information
      "calls": [...],              // Method call list
      "doc": {...}                 // JavaDoc information
    }
  },
  "interfaces": {...},             // Interface definitions
  "enums": {...}                   // Enum definitions
}
```

## Testing

The project includes comprehensive test cases:

```bash
# Run basic functionality unit tests
cd inspect4j
python Test/test_java_inspector.py

# Test directory analysis
python -m inspect4j.main -i Test/test_repos/Mines -o mines_analysis -r -cl -dt
```

## Project Structure

```
inspect4j/
├── inspect4j/
│   ├── __init__.py
│   ├── main.py                  # CLI entry point
│   ├── java_inspector.py        # Core analysis engine
│   ├── java_utils.py           # Utility functions
│   ├── structure_tree.py       # Directory tree extraction
│   └── licenses/               # License templates
├── Test/
│   ├── test_repos/             # Test Java projects
│   ├── test_files/             # Test files for unit tests
│   └── test_java_inspector.py  # Unit tests
├── requirements.txt
├── setup.py
├── README.md
└── LICENSE
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

*This project is part of an MSc dissertation at the University of Edinburgh's EPCC (Edinburgh Parallel Computing Centre).*