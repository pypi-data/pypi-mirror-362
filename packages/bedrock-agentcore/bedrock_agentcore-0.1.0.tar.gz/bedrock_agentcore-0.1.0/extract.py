#!/usr/bin/env python3

import os
import argparse
import re
from pathlib import Path

def extract_to_markdown(source_dir, output_file, verbose=False):
    """
    Extract important files from source_dir to a single markdown file.
    
    Args:
        source_dir (str): Source directory path
        output_file (str): Output markdown file path
        verbose (bool): Whether to print verbose output
    """
    # File extensions to include
    important_extensions = {
        '.py',      # Python files
        '.md',      # Markdown files
        '.ipynb',   # Jupyter notebooks
        '.yaml',    # YAML configuration
        '.yml',     # YAML alternative
        '.toml',    # TOML configuration
        '.j2',      # Jinja2 templates
        '.css',     # CSS files
        '.html',    # HTML files
        '.sh',      # Shell scripts
    }
    
    # Directories to exclude
    exclude_dirs = {
        'wheelhouse',
        '__pycache__',
        '.git',
        '.idea',
        '.vscode',
        'venv',
        '.venv',
        'env',
        '.env',
        'dist',
        'build',
    }

    # Files to exclude by pattern
    exclude_patterns = [
        r'.*\.whl$',      # Wheel files
        r'.*\.pyc$',      # Compiled python
        r'.*\.so$',       # Shared objects
        r'.*\.egg-info$', # Egg info
    ]
    compiled_patterns = [re.compile(pattern) for pattern in exclude_patterns]
    
    # Initialize file content string
    content = f"# Repository Code Review\n\nGenerated on {os.popen('date').read()}\n\n"
    content += "## Table of Contents\n\n"
    
    # Collect files to include
    files_to_include = []
    
    # Walk through the directory structure
    for root, dirs, files in os.walk(source_dir):
        # Skip excluded directories but never skip .github directory
        if '.github' in dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs or d == '.github']
        else:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Process each file
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, source_dir)
            
            # Skip if file matches any exclude pattern
            if any(pattern.match(file) for pattern in compiled_patterns):
                if verbose:
                    print(f"Skipping: {rel_path}")
                continue
            
            # Include file if it has an important extension or is a README or config file
            file_ext = os.path.splitext(file)[1].lower()
            file_lower = file.lower()
            
            # Special handling for GitHub Actions files
            in_github_dir = '.github' in rel_path.split(os.sep)
            
            if (file_ext in important_extensions or
                'readme' in file_lower or
                'config' in file_lower or
                'dockerfile' in file_lower or
                'requirements' in file_lower or
                in_github_dir):  # Include any file in .github directory
                
                files_to_include.append(rel_path)
                if verbose:
                    print(f"Including: {rel_path}")
    
    # Sort files for consistent output
    files_to_include.sort()
    
    # Add table of contents
    for i, file_path in enumerate(files_to_include):
        content += f"{i+1}. [{file_path}](#{file_path.replace('/', '-').replace('.', '-').replace(' ', '-')})\n"
    
    # Add file contents
    for file_path in files_to_include:
        full_path = os.path.join(source_dir, file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Create an anchor from the file path
        anchor_name = file_path.replace('/', '-').replace('.', '-').replace(' ', '-')
        
        content += f"\n\n## {file_path} <a name='{anchor_name}'></a>\n\n"
        
        # Determine language for code block based on file extension
        lang_map = {
            '.py': 'python',
            '.ipynb': 'json',
            '.md': 'markdown',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.toml': 'toml',
            '.j2': 'jinja2',
            '.css': 'css',
            '.html': 'html',
            '.sh': 'bash',
        }
        lang = lang_map.get(file_ext, '')
        
        try:
            # Try to read the file with UTF-8 encoding
            with open(full_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Add content with appropriate code block formatting
            content += f"```{lang}\n{file_content}\n```\n"
            
        except UnicodeDecodeError:
            # Handle binary files or encoding issues
            content += f"*[Binary file or encoding issue - content not displayed]*\n"
        except Exception as e:
            # Handle any other errors
            content += f"*Error reading file: {str(e)}*\n"
    
    # Write the compiled content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    files_count = len(files_to_include)
    print(f"Extraction complete. Included {files_count} files in {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract code files to a single markdown file')
    parser.add_argument('--source_dir', default='.', help='Source directory path (default: current directory)')
    parser.add_argument('--output', default='repository_code.md', help='Output markdown file (default: repository_code.md)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    
    args = parser.parse_args()
    
    # Convert to absolute paths
    source_dir = os.path.abspath(args.source_dir)
    output_file = args.output
    
    # Check if source directory exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist")
        exit(1)
        
    extract_to_markdown(source_dir, output_file, args.verbose)
