"""
Convention Extractor for analyzing codebase patterns.
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from ..debug import logger
from .models import Convention, Pattern


class ConventionExtractor:
    """Extracts coding conventions from existing codebase."""
    
    # Common naming patterns
    NAMING_PATTERNS = {
        'snake_case': re.compile(r'^[a-z][a-z0-9_]*$'),
        'camelCase': re.compile(r'^[a-z][a-zA-Z0-9]*$'),
        'PascalCase': re.compile(r'^[A-Z][a-zA-Z0-9]*$'),
        'UPPER_SNAKE_CASE': re.compile(r'^[A-Z][A-Z0-9_]*$'),
        'kebab-case': re.compile(r'^[a-z][a-z0-9-]*$'),
    }
    
    # Language-specific patterns
    LANGUAGE_PATTERNS = {
        '.py': {
            'function': re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('),
            'class': re.compile(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[\(:]'),
            'variable': re.compile(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*='),
            'constant': re.compile(r'^([A-Z][A-Z0-9_]*)\s*='),
            'import': re.compile(r'^(?:from\s+[\w.]+\s+)?import\s+(.+)'),
        },
        '.js': {
            'function': re.compile(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(|const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*(?:async\s*)?\('),
            'class': re.compile(r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*[{\s]'),
            'variable': re.compile(r'(?:let|const|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*='),
            'import': re.compile(r'^import\s+.*from\s+[\'"](.+)[\'"]'),
        },
        '.ts': {
            'function': re.compile(r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:<[^>]+>)?\s*\(|const\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?::\s*[^=]+)?\s*=\s*(?:async\s*)?\('),
            'class': re.compile(r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:<[^>]+>)?\s*[{\s]'),
            'interface': re.compile(r'interface\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:<[^>]+>)?\s*[{\s]'),
            'variable': re.compile(r'(?:let|const|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?::\s*[^=]+)?\s*='),
            'import': re.compile(r'^import\s+.*from\s+[\'"](.+)[\'"]'),
        },
    }
    
    def __init__(self):
        self.conventions = Convention()
        self.patterns = defaultdict(list)
        
    def extract_from_files(self, files: List[str]) -> Convention:
        """Extract conventions from given files."""
        naming_stats = defaultdict(lambda: defaultdict(Counter))
        formatting_stats = defaultdict(Counter)
        import_patterns = defaultdict(set)
        
        for file_path in files:
            if not os.path.exists(file_path):
                continue
                
            ext = Path(file_path).suffix.lower()
            if ext not in self.LANGUAGE_PATTERNS:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract naming conventions
                self._extract_naming(content, ext, naming_stats)
                
                # Extract formatting conventions
                self._extract_formatting(content, ext, formatting_stats)
                
                # Extract import patterns
                self._extract_imports(content, ext, import_patterns)
                
            except Exception as e:
                logger.debug(f"Error extracting from {file_path}: {e}")
                
        # Analyze and set conventions
        self._analyze_naming_stats(naming_stats)
        self._analyze_formatting_stats(formatting_stats)
        self._analyze_import_patterns(import_patterns)
        
        return self.conventions
    
    def _extract_naming(self, content: str, ext: str, stats: Dict):
        """Extract naming conventions from content."""
        patterns = self.LANGUAGE_PATTERNS.get(ext, {})
        
        for element_type, pattern in patterns.items():
            if element_type == 'import':
                continue
                
            matches = pattern.findall(content)
            for match in matches:
                # Handle tuple results from regex groups
                name = match[0] if isinstance(match, tuple) else match
                if not name:
                    continue
                    
                # Identify naming pattern
                for pattern_name, pattern_regex in self.NAMING_PATTERNS.items():
                    if pattern_regex.match(name):
                        stats[ext][element_type][pattern_name] += 1
                        break
    
    def _extract_formatting(self, content: str, ext: str, stats: Dict):
        """Extract formatting conventions from content."""
        lines = content.split('\n')
        
        # Indentation detection
        indent_counts = {'spaces_2': 0, 'spaces_4': 0, 'tabs': 0}
        for line in lines:
            if line.startswith('    '):
                indent_counts['spaces_4'] += 1
            elif line.startswith('  ') and not line.startswith('    '):
                indent_counts['spaces_2'] += 1
            elif line.startswith('\t'):
                indent_counts['tabs'] += 1
        
        # Find dominant indentation
        if indent_counts['spaces_4'] > indent_counts['spaces_2'] and indent_counts['spaces_4'] > indent_counts['tabs']:
            stats[ext]['indent'] = 'spaces_4'
        elif indent_counts['spaces_2'] > indent_counts['tabs']:
            stats[ext]['indent'] = 'spaces_2'
        elif indent_counts['tabs'] > 0:
            stats[ext]['indent'] = 'tabs'
        
        # Line length analysis
        line_lengths = [len(line) for line in lines if line.strip()]
        if line_lengths:
            # Use 90th percentile as max line length
            sorted_lengths = sorted(line_lengths)
            percentile_90 = sorted_lengths[int(len(sorted_lengths) * 0.9)]
            if percentile_90 <= 80:
                stats[ext]['line_length'] = 80
            elif percentile_90 <= 100:
                stats[ext]['line_length'] = 100
            elif percentile_90 <= 120:
                stats[ext]['line_length'] = 120
            else:
                stats[ext]['line_length'] = 150
        
        # Quote style for JS/TS
        if ext in ['.js', '.ts']:
            single_quotes = len(re.findall(r"'[^']*'", content))
            double_quotes = len(re.findall(r'"[^"]*"', content))
            if single_quotes > double_quotes * 1.5:
                stats[ext]['quotes'] = 'single'
            else:
                stats[ext]['quotes'] = 'double'
    
    def _extract_imports(self, content: str, ext: str, import_patterns: Dict):
        """Extract import patterns from content."""
        patterns = self.LANGUAGE_PATTERNS.get(ext, {})
        if 'import' not in patterns:
            return
            
        import_regex = patterns['import']
        matches = import_regex.findall(content)
        
        for match in matches:
            import_patterns[ext].add(match)
    
    def _analyze_naming_stats(self, stats: Dict):
        """Analyze naming statistics and set conventions."""
        for ext, elements in stats.items():
            ext_conventions = {}
            
            for element_type, pattern_counts in elements.items():
                if pattern_counts:
                    # Get most common pattern
                    most_common = pattern_counts.most_common(1)[0][0]
                    if element_type not in ext_conventions:
                        ext_conventions[element_type] = []
                    ext_conventions[element_type].append(most_common)
            
            # Store conventions by file type
            for element_type, patterns in ext_conventions.items():
                key = f"{element_type}_{ext}"
                self.conventions.naming[key] = patterns
    
    def _analyze_formatting_stats(self, stats: Dict):
        """Analyze formatting statistics and set conventions."""
        for ext, format_info in stats.items():
            if isinstance(format_info, dict):
                for key, value in format_info.items():
                    self.conventions.formatting[f"{key}_{ext}"] = value
            elif hasattr(format_info, 'most_common'):
                # Counter object
                if format_info:
                    most_common = format_info.most_common(1)[0][0]
                    self.conventions.formatting[f"style_{ext}"] = most_common
    
    def _analyze_import_patterns(self, import_patterns: Dict):
        """Analyze import patterns."""
        for ext, imports in import_patterns.items():
            if imports:
                # Group imports by type
                relative_imports = [imp for imp in imports if imp.startswith('.')]
                absolute_imports = [imp for imp in imports if not imp.startswith('.')]
                
                import_style = []
                if relative_imports:
                    import_style.append('relative')
                if absolute_imports:
                    import_style.append('absolute')
                
                self.conventions.imports[f"style_{ext}"] = import_style
    
    def extract_patterns_from_fix(self, issue_type: str, original: str, 
                                 fixed: str, file_type: str) -> Pattern:
        """Extract pattern from a fix example."""
        pattern = Pattern(
            pattern_type=issue_type,
            pattern_name=f"{issue_type}_{file_type}",
            examples=[fixed],
            confidence=0.5,
            usage_count=1
        )
        
        # Analyze the transformation
        if issue_type == 'naming_convention':
            # Detect naming pattern change
            for name, regex in self.NAMING_PATTERNS.items():
                if regex.match(fixed):
                    pattern.pattern_name = f"convert_to_{name}"
                    break
        
        return pattern
    
    def get_file_conventions(self, file_path: str) -> Dict[str, any]:
        """Get conventions specific to a file type."""
        ext = Path(file_path).suffix.lower()
        
        file_conventions = {
            'naming': {},
            'formatting': {},
            'imports': {}
        }
        
        # Extract file-specific conventions
        for key, value in self.conventions.naming.items():
            if key.endswith(ext):
                element_type = key.replace(ext, '').rstrip('_')
                file_conventions['naming'][element_type] = value
        
        for key, value in self.conventions.formatting.items():
            if key.endswith(ext):
                format_type = key.replace(ext, '').rstrip('_')
                file_conventions['formatting'][format_type] = value
        
        for key, value in self.conventions.imports.items():
            if key.endswith(ext):
                import_type = key.replace(ext, '').rstrip('_')
                file_conventions['imports'][import_type] = value
        
        return file_conventions