"""
Data models for the learning system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


@dataclass
class Fix:
    """Represents a fix that was accepted or rejected."""
    timestamp: str
    issue_type: str
    original: str
    fixed: str
    file_type: str
    file_path: Optional[str] = None
    confidence_impact: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'issue_type': self.issue_type,
            'original': self.original,
            'fixed': self.fixed,
            'file_type': self.file_type,
            'file_path': self.file_path,
            'confidence_impact': self.confidence_impact
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fix':
        return cls(**data)


@dataclass
class Pattern:
    """Represents a learned code pattern."""
    pattern_type: str
    pattern_name: str
    examples: List[str] = field(default_factory=list)
    confidence: float = 0.5
    usage_count: int = 0
    last_seen: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'pattern_type': self.pattern_type,
            'pattern_name': self.pattern_name,
            'examples': self.examples,
            'confidence': self.confidence,
            'usage_count': self.usage_count,
            'last_seen': self.last_seen
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pattern':
        return cls(**data)


@dataclass
class Convention:
    """Represents coding conventions."""
    naming: Dict[str, List[str]] = field(default_factory=dict)
    formatting: Dict[str, Any] = field(default_factory=dict)
    imports: Dict[str, List[str]] = field(default_factory=dict)
    error_handling: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'naming': self.naming,
            'formatting': self.formatting,
            'imports': self.imports,
            'error_handling': self.error_handling
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Convention':
        return cls(**data)


@dataclass
class Learning:
    """Main learning data structure."""
    version: str = "1.0"
    repository_id: str = ""
    last_updated: str = ""
    conventions: Convention = field(default_factory=Convention)
    patterns: Dict[str, List[Pattern]] = field(default_factory=dict)
    fixes: Dict[str, List[Fix]] = field(default_factory=lambda: {'accepted': [], 'rejected': []})
    statistics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'version': self.version,
            'repository_id': self.repository_id,
            'last_updated': self.last_updated,
            'conventions': self.conventions.to_dict(),
            'patterns': {
                k: [p.to_dict() for p in v]
                for k, v in self.patterns.items()
            },
            'fixes': {
                'accepted': [f.to_dict() for f in self.fixes['accepted']],
                'rejected': [f.to_dict() for f in self.fixes['rejected']]
            },
            'statistics': self.statistics
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Learning':
        learning = cls()
        learning.version = data.get('version', '1.0')
        learning.repository_id = data.get('repository_id', '')
        learning.last_updated = data.get('last_updated', '')
        
        if 'conventions' in data:
            learning.conventions = Convention.from_dict(data['conventions'])
        
        if 'patterns' in data:
            learning.patterns = {
                k: [Pattern.from_dict(p) for p in v]
                for k, v in data['patterns'].items()
            }
        
        if 'fixes' in data:
            learning.fixes = {
                'accepted': [Fix.from_dict(f) for f in data['fixes'].get('accepted', [])],
                'rejected': [Fix.from_dict(f) for f in data['fixes'].get('rejected', [])]
            }
        
        learning.statistics = data.get('statistics', {})
        return learning
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Learning':
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))