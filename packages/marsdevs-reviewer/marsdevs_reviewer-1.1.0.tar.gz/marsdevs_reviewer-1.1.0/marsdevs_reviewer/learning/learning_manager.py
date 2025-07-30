"""
Learning Manager for persistent storage and retrieval of repository-specific conventions.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from ..debug import logger, debug_mode
from .models import Learning, Convention, Pattern, Fix


class LearningManager:
    """Manages loading, saving, and updating of learning data."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).absolute()
        self.learning_dir = self.repo_path / ".marsdevs"
        self.learning_file = self.learning_dir / "learning.json"
        self.conventions_file = self.learning_dir / "conventions.json"
        self.patterns_dir = self.learning_dir / "patterns"
        self.learning_data: Optional[Learning] = None
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure learning directories exist."""
        self.learning_dir.mkdir(exist_ok=True)
        self.patterns_dir.mkdir(exist_ok=True)
        
        # Add .gitignore to not track learning data
        gitignore_path = self.learning_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text("*\n!.gitignore\n")
    
    def _get_repository_id(self) -> str:
        """Generate unique repository ID based on path."""
        return hashlib.md5(str(self.repo_path).encode()).hexdigest()
    
    def load_learning(self) -> Learning:
        """Load existing learning data or create new."""
        if self.learning_data:
            return self.learning_data
            
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r') as f:
                    data = json.load(f)
                self.learning_data = Learning.from_dict(data)
                logger.info(f"Loaded learning data from {self.learning_file}")
            except Exception as e:
                logger.error(f"Error loading learning data: {e}")
                self.learning_data = self._create_new_learning()
        else:
            self.learning_data = self._create_new_learning()
            
        return self.learning_data
    
    def _create_new_learning(self) -> Learning:
        """Create new learning data structure."""
        learning = Learning()
        learning.repository_id = self._get_repository_id()
        learning.last_updated = datetime.now().isoformat()
        learning.statistics = {
            'total_reviews': 0,
            'api_calls_made': 0,
            'api_calls_saved': 0,
            'patterns_learned': 0,
            'fixes_accepted': 0,
            'fixes_rejected': 0
        }
        return learning
    
    def save_learning(self):
        """Save learning data to disk."""
        if not self.learning_data:
            return
            
        self.learning_data.last_updated = datetime.now().isoformat()
        
        try:
            with open(self.learning_file, 'w') as f:
                json.dump(self.learning_data.to_dict(), f, indent=2)
            logger.info(f"Saved learning data to {self.learning_file}")
        except Exception as e:
            logger.error(f"Error saving learning data: {e}")
    
    def update_from_accepted_fix(self, issue_type: str, original: str, 
                                fixed: str, file_path: str):
        """Update learning based on accepted fix."""
        learning = self.load_learning()
        
        # Create fix record
        fix = Fix(
            timestamp=datetime.now().isoformat(),
            issue_type=issue_type,
            original=original,
            fixed=fixed,
            file_type=Path(file_path).suffix,
            file_path=file_path,
            confidence_impact=0.1
        )
        
        learning.fixes['accepted'].append(fix)
        
        # Update pattern confidence
        pattern_key = f"{issue_type}_{Path(file_path).suffix}"
        if pattern_key in learning.patterns:
            for pattern in learning.patterns[pattern_key]:
                if pattern.pattern_name == issue_type:
                    pattern.confidence = min(0.95, pattern.confidence + 0.1)
                    pattern.usage_count += 1
                    pattern.last_seen = datetime.now().isoformat()
                    if fixed not in pattern.examples:
                        pattern.examples.append(fixed)
                        # Keep only last 10 examples
                        pattern.examples = pattern.examples[-10:]
        else:
            # Create new pattern
            new_pattern = Pattern(
                pattern_type=issue_type,
                pattern_name=issue_type,
                examples=[fixed],
                confidence=0.6,  # Start higher for accepted fixes
                usage_count=1,
                last_seen=datetime.now().isoformat()
            )
            if pattern_key not in learning.patterns:
                learning.patterns[pattern_key] = []
            learning.patterns[pattern_key].append(new_pattern)
        
        # Update statistics
        learning.statistics['fixes_accepted'] += 1
        
        self.save_learning()
        logger.info(f"Updated learning from accepted fix: {issue_type}")
    
    def update_from_rejected_fix(self, issue_type: str, original: str, 
                                fixed: str, file_path: str):
        """Update learning based on rejected fix."""
        learning = self.load_learning()
        
        # Create fix record
        fix = Fix(
            timestamp=datetime.now().isoformat(),
            issue_type=issue_type,
            original=original,
            fixed=fixed,
            file_type=Path(file_path).suffix,
            file_path=file_path,
            confidence_impact=-0.2
        )
        
        learning.fixes['rejected'].append(fix)
        
        # Decrease pattern confidence
        pattern_key = f"{issue_type}_{Path(file_path).suffix}"
        if pattern_key in learning.patterns:
            for pattern in learning.patterns[pattern_key]:
                if pattern.pattern_name == issue_type:
                    pattern.confidence = max(0.1, pattern.confidence - 0.2)
                    pattern.last_seen = datetime.now().isoformat()
        
        # Update statistics
        learning.statistics['fixes_rejected'] += 1
        
        self.save_learning()
        logger.info(f"Updated learning from rejected fix: {issue_type}")
    
    def get_learned_fix(self, issue_type: str, code: str, 
                       file_path: str) -> Optional[Tuple[str, float]]:
        """Get learned fix for given issue if confidence is high enough."""
        learning = self.load_learning()
        
        pattern_key = f"{issue_type}_{Path(file_path).suffix}"
        if pattern_key not in learning.patterns:
            return None
        
        for pattern in learning.patterns[pattern_key]:
            if pattern.pattern_name == issue_type and pattern.confidence >= 0.7:
                # Check recent accepted fixes for similar patterns
                recent_fixes = [
                    fix for fix in learning.fixes['accepted'][-20:]
                    if fix.issue_type == issue_type and 
                    fix.file_type == Path(file_path).suffix
                ]
                
                if recent_fixes:
                    # Use the most recent accepted fix pattern
                    latest_fix = recent_fixes[-1]
                    return latest_fix.fixed, pattern.confidence
                elif pattern.examples:
                    # Use the most common example
                    return pattern.examples[-1], pattern.confidence
        
        return None
    
    def update_statistics(self, api_called: bool):
        """Update usage statistics."""
        learning = self.load_learning()
        
        learning.statistics['total_reviews'] += 1
        if api_called:
            learning.statistics['api_calls_made'] += 1
        else:
            learning.statistics['api_calls_saved'] += 1
        
        self.save_learning()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        learning = self.load_learning()
        stats = learning.statistics.copy()
        
        # Calculate additional metrics
        total_patterns = sum(len(patterns) for patterns in learning.patterns.values())
        high_confidence_patterns = sum(
            1 for patterns in learning.patterns.values()
            for p in patterns if p.confidence >= 0.7
        )
        
        stats.update({
            'total_patterns': total_patterns,
            'high_confidence_patterns': high_confidence_patterns,
            'api_reduction_rate': (
                stats['api_calls_saved'] / max(1, stats['total_reviews']) * 100
                if stats['total_reviews'] > 0 else 0
            )
        })
        
        return stats
    
    def clear_learning(self):
        """Clear all learning data."""
        try:
            if self.learning_file.exists():
                self.learning_file.unlink()
            if self.conventions_file.exists():
                self.conventions_file.unlink()
            self.learning_data = None
            logger.info("Cleared learning data")
        except Exception as e:
            logger.error(f"Error clearing learning data: {e}")
    
    def export_conventions(self) -> Dict[str, Any]:
        """Export learned conventions for sharing."""
        learning = self.load_learning()
        
        return {
            'repository_id': learning.repository_id,
            'exported_at': datetime.now().isoformat(),
            'conventions': learning.conventions.to_dict(),
            'high_confidence_patterns': {
                k: [p.to_dict() for p in patterns if p.confidence >= 0.8]
                for k, patterns in learning.patterns.items()
            }
        }
    
    def import_conventions(self, conventions_data: Dict[str, Any]):
        """Import conventions from another repository."""
        learning = self.load_learning()
        
        # Merge conventions
        if 'conventions' in conventions_data:
            imported = Convention.from_dict(conventions_data['conventions'])
            # Merge naming conventions
            for key, values in imported.naming.items():
                if key not in learning.conventions.naming:
                    learning.conventions.naming[key] = values
                else:
                    learning.conventions.naming[key].extend(
                        v for v in values if v not in learning.conventions.naming[key]
                    )
        
        # Import high confidence patterns
        if 'high_confidence_patterns' in conventions_data:
            for key, patterns in conventions_data['high_confidence_patterns'].items():
                if key not in learning.patterns:
                    learning.patterns[key] = []
                
                for p_data in patterns:
                    pattern = Pattern.from_dict(p_data)
                    pattern.confidence *= 0.8  # Reduce confidence for imported patterns
                    learning.patterns[key].append(pattern)
        
        self.save_learning()
        logger.info("Imported conventions successfully")