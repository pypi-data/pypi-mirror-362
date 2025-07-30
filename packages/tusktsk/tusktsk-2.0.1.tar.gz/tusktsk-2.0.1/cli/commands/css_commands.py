#!/usr/bin/env python3
"""
TuskLang Python CLI - CSS Commands
==================================
CSS utilities and operations
"""

import re
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..utils import output_formatter, error_handler, config_loader


def handle_css_command(args, cli):
    """Handle CSS commands"""
    if args.css_command == 'expand':
        return handle_expand_command(args, cli)
    elif args.css_command == 'map':
        return handle_map_command(args, cli)
    else:
        output_formatter.print_error("Unknown CSS command")
        return 1


def handle_expand_command(args, cli):
    """Handle CSS expand command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Read CSS file
        with open(file_path, 'r') as f:
            css_content = f.read()
        
        # Expand CSS shorthand properties
        expanded_css = expand_css_shorthand(css_content)
        
        # Create output file
        output_file = file_path.with_suffix('.expanded.css')
        with open(output_file, 'w') as f:
            f.write(expanded_css)
        
        # Get statistics
        original_lines = len(css_content.split('\n'))
        expanded_lines = len(expanded_css.split('\n'))
        original_size = len(css_content)
        expanded_size = len(expanded_css)
        
        # Prepare result
        result = {
            'input_file': str(file_path),
            'output_file': str(output_file),
            'original_lines': original_lines,
            'expanded_lines': expanded_lines,
            'original_size': original_size,
            'expanded_size': expanded_size,
            'expansion_ratio': round((expanded_lines / original_lines) * 100, 2),
            'success': True
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"🔍 Expanded: {args.file} → {output_file.name}")
            print(f"   Original lines: {original_lines}")
            print(f"   Expanded lines: {expanded_lines}")
            print(f"   Expansion ratio: {result['expansion_ratio']}%")
            print(f"   Original size: {original_size} bytes")
            print(f"   Expanded size: {expanded_size} bytes")
            
            if cli.verbose:
                print(f"\n📋 Expanded CSS Preview:")
                print("=" * 50)
                print(expanded_css[:500] + "..." if len(expanded_css) > 500 else expanded_css)
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"CSS expand error: {str(e)}")
        return 1


def expand_css_shorthand(css_content: str) -> str:
    """Expand CSS shorthand properties to longhand"""
    
    # CSS shorthand patterns
    shorthand_patterns = {
        # Margin
        r'margin:\s*([^;]+);': expand_margin,
        # Padding
        r'padding:\s*([^;]+);': expand_padding,
        # Border
        r'border:\s*([^;]+);': expand_border,
        # Background
        r'background:\s*([^;]+);': expand_background,
        # Font
        r'font:\s*([^;]+);': expand_font,
        # Border-radius
        r'border-radius:\s*([^;]+);': expand_border_radius,
        # Transition
        r'transition:\s*([^;]+);': expand_transition,
        # Animation
        r'animation:\s*([^;]+);': expand_animation,
        # Flex
        r'flex:\s*([^;]+);': expand_flex,
        # Grid
        r'grid:\s*([^;]+);': expand_grid
    }
    
    expanded_css = css_content
    
    for pattern, expand_func in shorthand_patterns.items():
        expanded_css = re.sub(pattern, expand_func, expanded_css, flags=re.IGNORECASE)
    
    return expanded_css


def expand_margin(match) -> str:
    """Expand margin shorthand"""
    values = match.group(1).strip().split()
    
    if len(values) == 1:
        return f"margin-top: {values[0]};\nmargin-right: {values[0]};\nmargin-bottom: {values[0]};\nmargin-left: {values[0]};"
    elif len(values) == 2:
        return f"margin-top: {values[0]};\nmargin-right: {values[1]};\nmargin-bottom: {values[0]};\nmargin-left: {values[1]};"
    elif len(values) == 3:
        return f"margin-top: {values[0]};\nmargin-right: {values[1]};\nmargin-bottom: {values[2]};\nmargin-left: {values[1]};"
    elif len(values) == 4:
        return f"margin-top: {values[0]};\nmargin-right: {values[1]};\nmargin-bottom: {values[2]};\nmargin-left: {values[3]};"
    
    return match.group(0)


def expand_padding(match) -> str:
    """Expand padding shorthand"""
    values = match.group(1).strip().split()
    
    if len(values) == 1:
        return f"padding-top: {values[0]};\npadding-right: {values[0]};\npadding-bottom: {values[0]};\npadding-left: {values[0]};"
    elif len(values) == 2:
        return f"padding-top: {values[0]};\npadding-right: {values[1]};\npadding-bottom: {values[0]};\npadding-left: {values[1]};"
    elif len(values) == 3:
        return f"padding-top: {values[0]};\npadding-right: {values[1]};\npadding-bottom: {values[2]};\npadding-left: {values[1]};"
    elif len(values) == 4:
        return f"padding-top: {values[0]};\npadding-right: {values[1]};\npadding-bottom: {values[2]};\npadding-left: {values[3]};"
    
    return match.group(0)


def expand_border(match) -> str:
    """Expand border shorthand"""
    value = match.group(1).strip()
    
    # Simple border expansion
    return f"border-width: {value};\nborder-style: solid;\nborder-color: currentColor;"


def expand_background(match) -> str:
    """Expand background shorthand"""
    value = match.group(1).strip()
    
    # Basic background expansion
    return f"background-color: {value};\nbackground-image: none;\nbackground-repeat: repeat;\nbackground-attachment: scroll;\nbackground-position: 0% 0%;"


def expand_font(match) -> str:
    """Expand font shorthand"""
    value = match.group(1).strip()
    
    # Basic font expansion
    return f"font-style: normal;\nfont-variant: normal;\nfont-weight: normal;\nfont-size: {value};\nline-height: normal;\nfont-family: inherit;"


def expand_border_radius(match) -> str:
    """Expand border-radius shorthand"""
    values = match.group(1).strip().split()
    
    if len(values) == 1:
        return f"border-top-left-radius: {values[0]};\nborder-top-right-radius: {values[0]};\nborder-bottom-right-radius: {values[0]};\nborder-bottom-left-radius: {values[0]};"
    elif len(values) == 2:
        return f"border-top-left-radius: {values[0]};\nborder-top-right-radius: {values[1]};\nborder-bottom-right-radius: {values[0]};\nborder-bottom-left-radius: {values[1]};"
    elif len(values) == 3:
        return f"border-top-left-radius: {values[0]};\nborder-top-right-radius: {values[1]};\nborder-bottom-right-radius: {values[2]};\nborder-bottom-left-radius: {values[1]};"
    elif len(values) == 4:
        return f"border-top-left-radius: {values[0]};\nborder-top-right-radius: {values[1]};\nborder-bottom-right-radius: {values[2]};\nborder-bottom-left-radius: {values[3]};"
    
    return match.group(0)


def expand_transition(match) -> str:
    """Expand transition shorthand"""
    value = match.group(1).strip()
    
    # Basic transition expansion
    return f"transition-property: all;\ntransition-duration: {value};\ntransition-timing-function: ease;\ntransition-delay: 0s;"


def expand_animation(match) -> str:
    """Expand animation shorthand"""
    value = match.group(1).strip()
    
    # Basic animation expansion
    return f"animation-name: none;\nanimation-duration: {value};\nanimation-timing-function: ease;\nanimation-delay: 0s;\nanimation-iteration-count: 1;\nanimation-direction: normal;\nanimation-fill-mode: none;\nanimation-play-state: running;"


def expand_flex(match) -> str:
    """Expand flex shorthand"""
    value = match.group(1).strip()
    
    # Basic flex expansion
    return f"flex-grow: {value};\nflex-shrink: 1;\nflex-basis: 0%;"


def expand_grid(match) -> str:
    """Expand grid shorthand"""
    value = match.group(1).strip()
    
    # Basic grid expansion
    return f"grid-template-areas: none;\ngrid-template-rows: none;\ngrid-template-columns: none;\ngrid-auto-rows: auto;\ngrid-auto-columns: auto;\ngrid-auto-flow: row;\ngrid-area: auto;\ngrid-row-start: auto;\ngrid-row-end: auto;\ngrid-column-start: auto;\ngrid-column-end: auto;"


def handle_map_command(args, cli):
    """Handle CSS map command"""
    file_path = Path(args.file)
    if not file_path.exists():
        output_formatter.print_error(f"File not found: {args.file}")
        return 1
    
    try:
        # Read CSS file
        with open(file_path, 'r') as f:
            css_content = f.read()
        
        # Generate source map
        source_map = generate_css_source_map(css_content, str(file_path))
        
        # Create source map file
        map_file = file_path.with_suffix('.css.map')
        with open(map_file, 'w') as f:
            json.dump(source_map, f, indent=2)
        
        # Add source map comment to CSS
        css_with_map = css_content + f"\n/*# sourceMappingURL={map_file.name} */"
        
        # Write updated CSS
        with open(file_path, 'w') as f:
            f.write(css_with_map)
        
        # Get statistics
        css_lines = len(css_content.split('\n'))
        map_size = len(json.dumps(source_map))
        
        # Prepare result
        result = {
            'css_file': str(file_path),
            'map_file': str(map_file),
            'css_lines': css_lines,
            'map_size': map_size,
            'mappings_count': len(source_map.get('mappings', '')),
            'sources': source_map.get('sources', []),
            'success': True
        }
        
        if cli.json_output:
            output_formatter.print_json(result)
        else:
            print(f"🗺️  Generated source map: {map_file.name}")
            print(f"   CSS lines: {css_lines}")
            print(f"   Map size: {map_size} bytes")
            print(f"   Mappings: {result['mappings_count']}")
            print(f"   Sources: {len(result['sources'])}")
            
            if cli.verbose:
                print(f"\n📋 Source Map Preview:")
                print(json.dumps(source_map, indent=2)[:500] + "..." if len(json.dumps(source_map)) > 500 else json.dumps(source_map, indent=2))
        
        return 0
        
    except Exception as e:
        output_formatter.print_error(f"CSS map error: {str(e)}")
        return 1


def generate_css_source_map(css_content: str, file_path: str) -> Dict[str, Any]:
    """Generate CSS source map"""
    
    # Parse CSS to extract line and column information
    lines = css_content.split('\n')
    mappings = []
    current_line = 0
    current_column = 0
    
    for line_num, line in enumerate(lines):
        # Simple mapping - each character maps to the same position
        for char_num, char in enumerate(line):
            if char.strip():  # Only map non-whitespace characters
                mappings.append(f"{current_column},{current_line},{line_num},{char_num}")
            current_column += 1
        current_line += len(line) + 1  # +1 for newline
        current_column = 0
    
    # Create source map structure
    source_map = {
        "version": 3,
        "file": Path(file_path).name,
        "sourceRoot": "",
        "sources": [file_path],
        "names": [],
        "mappings": ";".join(mappings)
    }
    
    return source_map 