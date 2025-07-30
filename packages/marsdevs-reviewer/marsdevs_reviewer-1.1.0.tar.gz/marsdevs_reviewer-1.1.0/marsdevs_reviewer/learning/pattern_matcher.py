"""
Pattern Matcher for matching code against learned patterns.
"""

import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from difflib import SequenceMatcher
from ..debug import logger
from .models import Pattern, Fix


class PatternMatcher:
    """Matches code against learned patterns and suggests fixes."""
    
    def __init__(self, learning_manager):
        self.learning_manager = learning_manager
        self.learning = learning_manager.load_learning()
    
    def find_issues_with_learned_patterns(self, diff: str, files: List[str]) -> List[Dict]:
        """Find issues in diff using learned patterns."""
        issues = []
        
        # Parse diff to extract changed lines
        changed_sections = self._parse_diff(diff)
        
        for file_path, changes in changed_sections.items():
            if file_path not in files:
                continue
                
            file_ext = Path(file_path).suffix
            
            # Check each changed line against learned patterns
            for line_num, line_content in changes:
                # Skip removed lines
                if line_content.startswith('-'):
                    continue
                    
                # Check against learned patterns
                issue = self._check_line_patterns(
                    line_content.lstrip('+'),
                    file_path,
                    file_ext,
                    line_num
                )
                
                if issue:
                    issues.append(issue)
        
        return issues
    
    def _parse_diff(self, diff: str) -> Dict[str, List[Tuple[int, str]]]:
        """Parse git diff to extract changed lines by file."""
        changed_sections = {}
        current_file = None
        line_number = 0
        
        for line in diff.split('\n'):
            # File header
            if line.startswith('+++'):
                current_file = line.split('+++')[1].strip().lstrip('b/')
                changed_sections[current_file] = []
                continue
            
            # Line number header
            if line.startswith('@@'):
                # Extract line number
                match = re.search(r'\+(\d+)', line)
                if match:
                    line_number = int(match.group(1)) - 1
                continue
            
            # Changed lines
            if current_file and (line.startswith('+') or line.startswith('-')):
                if not line.startswith('+++') and not line.startswith('---'):
                    changed_sections[current_file].append((line_number, line))
            
            # Increment line number for added/context lines
            if line.startswith('+') or not line.startswith('-'):
                line_number += 1
        
        return changed_sections
    
    def _check_line_patterns(self, line: str, file_path: str, 
                           file_ext: str, line_num: int) -> Optional[Dict]:
        """Check a line against learned patterns."""
        
        # Check variable naming patterns
        if issue := self._check_naming_pattern(line, file_ext, 'variable'):
            return {
                'file': file_path,
                'line_start': line_num,
                'line_end': line_num,
                'type': 'convention',
                'convention_violated': issue['convention'],
                'description': issue['description'],
                'current_code': line.strip(),
                'fixed_code': issue['fixed'],
                'confidence': issue['confidence'],
                'learned': True
            }
        
        # Check function naming patterns
        if issue := self._check_naming_pattern(line, file_ext, 'function'):
            return {
                'file': file_path,
                'line_start': line_num,
                'line_end': line_num,
                'type': 'convention',
                'convention_violated': issue['convention'],
                'description': issue['description'],
                'current_code': line.strip(),
                'fixed_code': issue['fixed'],
                'confidence': issue['confidence'],
                'learned': True
            }
        
        # Check common patterns from accepted fixes
        if issue := self._check_accepted_fix_patterns(line, file_ext):
            return {
                'file': file_path,
                'line_start': line_num,
                'line_end': line_num,
                'type': issue['type'],
                'convention_violated': issue['convention'],
                'description': issue['description'],
                'current_code': line.strip(),
                'fixed_code': issue['fixed'],
                'confidence': issue['confidence'],
                'learned': True
            }
        
        return None
    
    def _check_naming_pattern(self, line: str, file_ext: str, 
                            element_type: str) -> Optional[Dict]:
        """Check naming patterns for variables, functions, etc."""
        # Get naming conventions for this file type
        naming_key = f"{element_type}_{file_ext}"
        conventions = self.learning.conventions.naming.get(naming_key, [])
        
        if not conventions:
            return None
        
        # Language-specific patterns
        patterns = {
            '.py': {
                'variable': r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=',
                'function': r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            },
            '.js': {
                'variable': r'(?:let|const|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=',
                'function': r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(',
            },
            '.ts': {
                'variable': r'(?:let|const|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?::\s*[^=]+)?\s*=',
                'function': r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*(?:<[^>]+>)?\s*\(',
            },
        }
        
        if file_ext not in patterns or element_type not in patterns[file_ext]:
            return None
        
        pattern = patterns[file_ext][element_type]
        match = re.search(pattern, line)
        
        if match:
            name = match.group(1)
            expected_pattern = conventions[0]  # Use most common pattern
            
            # Check if name follows expected pattern
            if not self._matches_naming_pattern(name, expected_pattern):
                # Convert to expected pattern
                fixed_name = self._convert_naming(name, expected_pattern)
                fixed_line = line.replace(name, fixed_name)
                
                # Check confidence from historical data
                pattern_key = f"naming_convention_{file_ext}"
                confidence = 0.8  # Default confidence
                
                if pattern_key in self.learning.patterns:
                    for pattern in self.learning.patterns[pattern_key]:
                        if pattern.confidence > confidence:
                            confidence = pattern.confidence
                
                return {
                    'convention': f"Use {expected_pattern} for {element_type} names",
                    'description': f"{element_type.capitalize()} '{name}' should use {expected_pattern}",
                    'fixed': fixed_line.strip(),
                    'confidence': confidence,
                    'type': 'naming_convention'
                }
        
        return None
    
    def _check_accepted_fix_patterns(self, line: str, file_ext: str) -> Optional[Dict]:
        """Check against patterns from previously accepted fixes."""
        # Get recent accepted fixes for this file type
        recent_fixes = [
            fix for fix in self.learning.fixes['accepted'][-50:]
            if fix.file_type == file_ext
        ]
        
        for fix in recent_fixes:
            # Check if line contains similar pattern to original
            similarity = SequenceMatcher(None, line.strip(), fix.original).ratio()
            
            if similarity > 0.8:  # High similarity to a previous issue
                # Apply similar transformation
                fixed_line = line.replace(fix.original, fix.fixed)
                
                # Get confidence from patterns
                pattern_key = f"{fix.issue_type}_{file_ext}"
                confidence = 0.7  # Default
                
                if pattern_key in self.learning.patterns:
                    for pattern in self.learning.patterns[pattern_key]:
                        if pattern.pattern_name == fix.issue_type:
                            confidence = pattern.confidence
                            break
                
                if confidence >= 0.7:  # Only suggest if confidence is high
                    return {
                        'type': fix.issue_type,
                        'convention': f"Follow project pattern for {fix.issue_type}",
                        'description': f"Similar to previously fixed: {fix.original} → {fix.fixed}",
                        'fixed': fixed_line.strip(),
                        'confidence': confidence
                    }
        
        return None
    
    def _matches_naming_pattern(self, name: str, pattern: str) -> bool:
        """Check if name matches the expected naming pattern."""
        patterns = {
            'snake_case': r'^[a-z][a-z0-9_]*$',
            'camelCase': r'^[a-z][a-zA-Z0-9]*$',
            'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',
            'UPPER_SNAKE_CASE': r'^[A-Z][A-Z0-9_]*$',
        }
        
        if pattern in patterns:
            return bool(re.match(patterns[pattern], name))
        
        return True  # Unknown pattern, assume it matches
    
    def _convert_naming(self, name: str, target_pattern: str) -> str:
        """Convert name to target naming pattern."""
        # First, split the name into words
        words = self._split_name_into_words(name)
        
        if target_pattern == 'snake_case':
            return '_'.join(word.lower() for word in words)
        elif target_pattern == 'camelCase':
            return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        elif target_pattern == 'PascalCase':
            return ''.join(word.capitalize() for word in words)
        elif target_pattern == 'UPPER_SNAKE_CASE':
            return '_'.join(word.upper() for word in words)
        
        return name  # Unknown pattern, return as is
    
    def _split_name_into_words(self, name: str) -> List[str]:
        """Split a name into component words."""
        # Handle snake_case
        if '_' in name:
            return name.split('_')
        
        # Handle camelCase and PascalCase
        words = []
        current_word = []
        
        for i, char in enumerate(name):
            if i > 0 and char.isupper() and name[i-1].islower():
                words.append(''.join(current_word))
                current_word = [char]
            else:
                current_word.append(char)
        
        if current_word:
            words.append(''.join(current_word))
        
        return [w for w in words if w]
    
    def should_use_learned_pattern(self, issue_type: str, file_ext: str) -> bool:
        """Check if we should use learned pattern instead of API."""
        pattern_key = f"{issue_type}_{file_ext}"
        
        if pattern_key in self.learning.patterns:
            # Check if we have high confidence patterns
            high_confidence_patterns = [
                p for p in self.learning.patterns[pattern_key]
                if p.confidence >= 0.7
            ]
            
            # Use learned pattern if we have high confidence and recent usage
            if high_confidence_patterns:
                most_recent = max(
                    high_confidence_patterns,
                    key=lambda p: p.last_seen or ''
                )
                return most_recent.usage_count >= 3
        
        return False
    
    def get_pattern_statistics(self) -> Dict[str, any]:
        """Get statistics about learned patterns."""
        stats = {
            'total_patterns': 0,
            'high_confidence_patterns': 0,
            'patterns_by_type': {},
            'most_used_patterns': []
        }
        
        for pattern_type, patterns in self.learning.patterns.items():
            stats['total_patterns'] += len(patterns)
            stats['patterns_by_type'][pattern_type] = len(patterns)
            
            for pattern in patterns:
                if pattern.confidence >= 0.7:
                    stats['high_confidence_patterns'] += 1
                
                stats['most_used_patterns'].append({
                    'name': pattern.pattern_name,
                    'type': pattern_type,
                    'usage': pattern.usage_count,
                    'confidence': pattern.confidence
                })
        
        # Sort by usage
        stats['most_used_patterns'].sort(
            key=lambda p: p['usage'],
            reverse=True
        )
        stats['most_used_patterns'] = stats['most_used_patterns'][:10]
        
        return stats