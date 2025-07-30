#!/usr/bin/env python3
"""
MarsDevs Code Reviewer - Pre-commit hook that uses AI to review staged changes
against repository coding conventions and offer fixes for violations.
"""

import subprocess
import sys
import os
import json
import requests
import shutil
import glob
import hashlib
import time
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# Import debug utilities if available
try:
    from .debug import (
        logger, debug_mode, profile_time, log_api_request,
        log_api_response, debug_git_state, debug_conventions,
        create_debug_report
    )
except ImportError:
    # Fallback if debug module not available
    import logging
    logger = logging.getLogger(__name__)
    debug_mode = lambda: False
    profile_time = lambda f: f
    log_api_request = lambda *args, **kwargs: None
    log_api_response = lambda *args, **kwargs: None
    debug_git_state = lambda: None
    debug_conventions = lambda *args, **kwargs: None
    create_debug_report = lambda e=None: str(e)

# Import learning system
try:
    from .learning import LearningManager, ConventionExtractor, PatternMatcher
    LEARNING_ENABLED = True
except ImportError:
    logger.warning("Learning system not available")
    LEARNING_ENABLED = False


@profile_time
def get_staged_diff() -> str:
    """Get the diff of only staged changes."""
    logger.debug("Getting staged diff")
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--unified=5'],
            capture_output=True,
            text=True,
            check=True
        )
        logger.debug(f"Diff size: {len(result.stdout)} chars")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting staged diff: {e}")
        print(f"Error getting staged diff: {e}")
        sys.exit(1)


def get_staged_files() -> List[str]:
    """Get list of staged files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}")
        sys.exit(1)


def get_file_extension(filepath: str) -> str:
    """Get file extension."""
    return Path(filepath).suffix.lower()


def find_similar_files(staged_files: List[str], limit: int = 5) -> Dict[str, List[str]]:
    """Find similar files in the repository for each staged file to learn conventions."""
    similar_files = {}

    for staged_file in staged_files:
        ext = get_file_extension(staged_file)
        if not ext:
            continue

        # Get directory of the staged file
        file_dir = os.path.dirname(staged_file)

        # Search for similar files in the same directory and parent directories
        search_paths = [
            file_dir,
            os.path.dirname(file_dir) if file_dir else '.',
            '.'
        ]

        found_files = set()
        for search_path in search_paths:
            if not search_path:
                continue

            # Find files with same extension
            pattern = os.path.join(search_path, f"**/*{ext}")
            try:
                matches = glob.glob(pattern, recursive=True)
                # Exclude the staged file itself and test files
                for match in matches:
                    if (match != staged_file and
                        not match.startswith('.') and
                        'test' not in match.lower() and
                        '__pycache__' not in match):
                        found_files.add(match)

                if len(found_files) >= limit:
                    break
            except Exception:
                continue

        # Sort by proximity to staged file
        similar_files[staged_file] = sorted(list(found_files))[:limit]

    return similar_files


def analyze_coding_conventions(similar_files: Dict[str, List[str]]) -> str:
    """Analyze coding conventions from similar files in the repository."""
    conventions = []

    for staged_file, reference_files in similar_files.items():
        if not reference_files:
            continue

        # Read a sample of reference files
        samples = []
        for ref_file in reference_files[:3]:  # Limit to 3 files per staged file
            try:
                with open(ref_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Limit content size
                    if len(content) > 5000:
                        content = content[:5000] + "\n... (truncated)"
                    samples.append(f"File: {ref_file}\n{content}")
            except Exception:
                continue

        if samples:
            conventions.append(f"Reference files for {staged_file}:\n" + "\n---\n".join(samples))

    return "\n\n".join(conventions) if conventions else ""


def get_project_config_files() -> Dict[str, str]:
    """Find and read project configuration files that define coding standards."""
    config_files = {
        '.editorconfig': 'EditorConfig settings',
        '.eslintrc': 'ESLint configuration',
        '.eslintrc.json': 'ESLint configuration',
        '.eslintrc.js': 'ESLint configuration',
        '.prettier': 'Prettier configuration',
        '.prettierrc': 'Prettier configuration',
        'pyproject.toml': 'Python project configuration',
        'setup.cfg': 'Python setup configuration',
        '.flake8': 'Flake8 configuration',
        '.pylintrc': 'Pylint configuration',
        'tslint.json': 'TSLint configuration',
        '.rubocop.yml': 'Rubocop configuration',
        'package.json': 'Package.json (check for linting scripts)',
        'Makefile': 'Makefile (check for linting/formatting targets)',
        '.clang-format': 'Clang format configuration',
        'rustfmt.toml': 'Rust format configuration'
    }

    found_configs = {}
    for config_file, description in config_files.items():
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Limit content size
                    if len(content) > 2000:
                        content = content[:2000] + "\n... (truncated)"
                    found_configs[config_file] = f"{description}:\n{content}"
            except Exception:
                continue

    return found_configs


def review_code_with_conventions(diff: str, files: List[str], conventions_context: str) -> Dict[str, any]:
    """Send code diff to AI for review against repository conventions."""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    headers = {
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }

    prompt = f"""You are a code reviewer. Your primary task is to ensure that the new code follows the existing coding conventions and practices of this repository.

IMPORTANT: Only review the ADDED or MODIFIED lines in the diff (lines starting with '+' that aren't just file markers). Do not review unchanged code or deleted lines.

First, analyze the repository's coding conventions from the provided context, then review ONLY the staged changes for:

1. **Coding Convention Violations**: Does the new code follow the same patterns, naming conventions, formatting, and style as the existing code?
2. **Consistency Issues**: Are the changes consistent with how similar functionality is implemented elsewhere in the codebase?
3. **Project-Specific Patterns**: Does the code follow project-specific patterns (e.g., error handling, logging, API design)?
4. **Code Quality Issues**: Only if they violate established patterns in the codebase
5. **Critical Bugs**: Only flag obvious errors (null pointers, syntax errors, security issues)

DO NOT flag:
- Style preferences not evident in the existing code
- Generic best practices not followed by the existing codebase
- Minor improvements unless they violate clear project conventions

Repository Context and Conventions:
{conventions_context}

For each issue found in the NEWLY ADDED/MODIFIED code:
- Reference the specific convention being violated
- Show an example from the existing codebase
- Provide a fix that matches the project's style

Format your response as JSON with this structure:
{{
    "has_issues": true/false,
    "severity": "critical/high/medium/low",
    "issues": [
        {{
            "file": "filename",
            "line_start": start_line_number,
            "line_end": end_line_number,
            "type": "convention/consistency/pattern/bug",
            "convention_violated": "Specific convention from the codebase",
            "example_from_codebase": "How it's done in existing code",
            "description": "Clear description of the violation",
            "current_code": "The violating code snippet",
            "fixed_code": "Code fixed to match conventions",
            "explanation": "Why this fix matches project conventions"
        }}
    ],
    "summary": "Overall assessment focusing on convention adherence"
}}

Files being changed: {', '.join(files)}

Git diff to review (only review + lines that are not file markers):
{diff}
"""

    data = {
        'model': 'claude-3-5-sonnet-20241022',
        'max_tokens': 4096,
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'temperature': 0
    }

    # Log API request in debug mode
    log_api_request('https://api.anthropic.com/v1/messages', headers, data)
    
    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data,
            timeout=60  # Increased timeout for convention analysis
        )
        response.raise_for_status()
        
        # Log API response in debug mode
        log_api_response(response)

        # Extract the content from Claude's response
        result = response.json()
        content = result['content'][0]['text']

        # Parse the JSON response
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If Claude didn't return valid JSON, create a structured response
            return {
                "has_issues": False,
                "severity": "low",
                "issues": [],
                "summary": content
            }

    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}")
        # In case of API error, allow the commit but warn
        return {
            "has_issues": False,
            "severity": "low",
            "issues": [],
            "summary": "Could not reach Claude API for review"
        }


def apply_fix(filepath: str, issue: Dict[str, any]) -> bool:
    """Apply a single fix to a file."""
    try:
        logger.debug(f"Applying fix to {filepath}")
        logger.debug(f"Issue type: {issue.get('type')}")
        logger.debug(f"Current code: '{issue.get('current_code', '')}'")
        logger.debug(f"Fixed code: '{issue.get('fixed_code', '')}'")
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' does not exist")
            # Try to resolve relative path
            if not os.path.isabs(filepath):
                abs_path = os.path.abspath(filepath)
                print(f"  - Trying absolute path: {abs_path}")
                if os.path.exists(abs_path):
                    filepath = abs_path
                else:
                    return False
            else:
                return False
        
        # Read the current file content
        with open(filepath, 'r') as f:
            content = f.read()

        # Apply the fix by replacing the current code with fixed code
        current_code = issue.get('current_code', '')
        fixed_code = issue.get('fixed_code', '')

        if current_code and fixed_code and current_code in content:
            # Create a backup
            backup_path = f"{filepath}.backup"
            shutil.copy2(filepath, backup_path)

            # Replace the code
            new_content = content.replace(current_code, fixed_code)

            # Write the fixed content
            with open(filepath, 'w') as f:
                f.write(new_content)

            # Stage the changes
            subprocess.run(['git', 'add', filepath], check=True)

            # Remove backup
            os.remove(backup_path)
            return True
        else:
            print(f"Could not find the exact code to replace in {filepath}")
            if not current_code:
                print("  - No current_code provided in issue")
            elif not fixed_code:
                print("  - No fixed_code provided in issue")
            else:
                print(f"  - Looking for: '{current_code}'")
                print(f"  - Code exists in file: {current_code in content}")
                # Show similar lines for debugging
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if current_code.strip() in line:
                        print(f"  - Similar line {i}: '{line}'")
            return False

    except Exception as e:
        print(f"Error applying fix to {filepath}: {e}")
        # Restore from backup if it exists
        if 'backup_path' in locals() and os.path.exists(backup_path):
            shutil.move(backup_path, filepath)
        return False


def interactive_fix_prompt(issue: Dict[str, any]) -> str:
    """Present an issue and its fix to the user for approval."""
    print("\n" + "-"*60)
    print(f"ISSUE: {issue['type'].upper()}")
    print(f"File: {issue['file']}")
    print(f"Lines: {issue.get('line_start', '?')}-{issue.get('line_end', '?')}")

    if issue.get('convention_violated'):
        print(f"\nConvention Violated: {issue['convention_violated']}")

    if issue.get('example_from_codebase'):
        print("\nExample from Codebase:")
        print(issue['example_from_codebase'])

    print(f"\nDescription: {issue['description']}")
    print(f"Explanation: {issue.get('explanation', 'N/A')}")

    print("\n--- Current Code ---")
    print(issue.get('current_code', 'N/A'))

    print("\n--- Suggested Fix ---")
    print(issue.get('fixed_code', 'N/A'))

    print("-"*60)

    while True:
        response = input("\nApply this fix? (y)es / (n)o / (s)kip all / (q)uit: ").lower().strip()
        if response in ['y', 'n', 's', 'q']:
            return response
        print("Invalid input. Please enter y, n, s, or q.")


def format_review_output(review: Dict[str, any], fixes_applied: List[int]) -> Tuple[bool, str]:
    """Format the review output for display."""
    output = []
    output.append("\n" + "="*60)
    output.append("MARSDEVS CODE CONVENTION REVIEW")
    output.append("="*60 + "\n")

    if not review.get('has_issues', False):
        output.append("✅ No convention violations found. Code follows project standards!")
        output.append(f"\nSummary: {review.get('summary', 'Code follows repository conventions.')}")
        return True, '\n'.join(output)

    total_issues = len(review.get('issues', []))
    fixed_issues = len(fixes_applied)

    # Count learned vs API issues
    learned_count = sum(1 for issue in review.get('issues', []) if issue.get('learned', False))
    api_count = total_issues - learned_count
    
    output.append(f"Found {total_issues} convention issue(s)")
    if learned_count > 0:
        output.append(f"  - {learned_count} from learned patterns ✨")
        output.append(f"  - {api_count} from AI analysis")
    output.append(f"Fixed: {fixed_issues} issue(s)")
    output.append(f"Severity: {review.get('severity', 'unknown').upper()}\n")

    for i, issue in enumerate(review.get('issues', []), 1):
        status = "✅ FIXED" if i in fixes_applied else "❌ NOT FIXED"
        learned_tag = " [LEARNED]" if issue.get('learned', False) else ""
        output.append(f"{i}. [{status}] {issue['type'].upper()}{learned_tag}")
        output.append(f"   File: {issue['file']}")
        if issue.get('line_start'):
            output.append(f"   Lines: {issue['line_start']}-{issue.get('line_end', issue['line_start'])}")
        if issue.get('convention_violated'):
            output.append(f"   Convention: {issue['convention_violated']}")
        output.append(f"   Issue: {issue['description']}")
        if issue.get('confidence') and issue.get('learned'):
            output.append(f"   Confidence: {issue['confidence']:.0%}")
        if i not in fixes_applied:
            output.append(f"   Fix: {issue.get('explanation', 'Match repository conventions')}\n")

    output.append(f"\nSummary: {review.get('summary', 'Please fix convention violations.')}")
    output.append("\n" + "="*60)

    # Determine if we should block based on unfixed critical issues
    severity = review.get('severity', 'low')
    if severity in ['critical', 'high'] and fixed_issues < total_issues:
        output.append("\n🚫 COMMIT BLOCKED: Critical convention violations remain unfixed.")
        return False, '\n'.join(output)
    elif fixed_issues < total_issues:
        output.append("\n⚠️  WARNING: Some convention violations remain. Commit allowed.")
        return True, '\n'.join(output)
    else:
        output.append("\n✅ All convention violations fixed! Ready to commit.")
        return True, '\n'.join(output)


def get_cache_key(diff: str, conventions: str) -> str:
    """Generate a cache key for the review."""
    content = f"{diff}\n{conventions}"
    return hashlib.md5(content.encode()).hexdigest()


def load_cached_review(cache_key: str) -> Optional[Dict[str, any]]:
    """Load cached review if available and recent."""
    cache_dir = os.path.expanduser("~/.cache/marsdevs-reviewer")
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")

    if os.path.exists(cache_file):
        # Check if cache is less than 1 hour old
        if os.path.getmtime(cache_file) > (time.time() - 3600):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def save_cached_review(cache_key: str, review: Dict[str, any]):
    """Save review to cache."""
    cache_dir = os.path.expanduser("~/.cache/marsdevs-reviewer")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")

    try:
        with open(cache_file, 'w') as f:
            json.dump(review, f)
    except Exception:
        pass  # Caching is optional


def main():
    """Main pre-commit hook logic."""
    try:
        print("Running MarsDevs Code Reviewer...")
        logger.info("Starting MarsDevs Code Reviewer")
        
        # Initialize learning system if available
        learning_manager = None
        pattern_matcher = None
        if LEARNING_ENABLED:
            try:
                learning_manager = LearningManager()
                pattern_matcher = PatternMatcher(learning_manager)
                logger.info("Learning system initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize learning system: {e}")
                
        # Debug git state if enabled
        debug_git_state()

        # Get staged changes
        diff = get_staged_diff()
        files = get_staged_files()

        if not diff or not files:
            logger.info("No staged changes to review")
            print("No staged changes to review.")
            sys.exit(0)

        # Skip review for certain file types
        skip_extensions = {'.md', '.txt', '.json', '.yml', '.yaml', '.lock', '.jpg', '.png', '.gif', '.svg'}
        files_to_review = [f for f in files if not any(f.endswith(ext) for ext in skip_extensions)]

        if not files_to_review:
            logger.info("No code files to review")
            print("No code files to review (only documentation/config changes).")
            sys.exit(0)

        print("\n📋 Analyzing repository coding conventions...")
        logger.info(f"Analyzing conventions for {len(files_to_review)} files")

        # Check for learned patterns first
        learned_issues = []
        api_needed = True
        
        if pattern_matcher:
            logger.info("Checking learned patterns...")
            learned_issues = pattern_matcher.find_issues_with_learned_patterns(diff, files_to_review)
            
            if learned_issues:
                print(f"✨ Found {len(learned_issues)} issues using learned patterns!")
                # If we have high confidence learned issues, we might skip API
                high_confidence_issues = [i for i in learned_issues if i.get('confidence', 0) >= 0.8]
                if high_confidence_issues and len(high_confidence_issues) == len(learned_issues):
                    api_needed = False
                    logger.info(f"Skipping API call - all {len(learned_issues)} issues resolved with learned patterns")

        # Extract conventions if learning is enabled
        if learning_manager and not learning_manager.learning_data:
            try:
                extractor = ConventionExtractor()
                # Use all files in repo for initial learning
                all_files = find_similar_files(files_to_review)
                all_files_flat = []
                for file_list in all_files.values():
                    all_files_flat.extend(file_list)
                
                extracted_conventions = extractor.extract_from_files(all_files_flat[:20])  # Limit to 20 files
                learning_manager.learning_data.conventions = extracted_conventions
                learning_manager.save_learning()
                logger.info("Extracted initial conventions from codebase")
            except Exception as e:
                logger.warning(f"Failed to extract conventions: {e}")

        # Find similar files to learn conventions
        similar_files = find_similar_files(files_to_review)

        # Get configuration files
        config_files = get_project_config_files()

        # Build conventions context
        conventions_parts = []

        if config_files:
            conventions_parts.append("=== Configuration Files ===")
            for config_file, content in config_files.items():
                conventions_parts.append(f"\n{content}")

        if similar_files:
            conventions_parts.append("\n=== Code Examples from Repository ===")
            code_samples = analyze_coding_conventions(similar_files)
            if code_samples:
                conventions_parts.append(code_samples)

        conventions_context = "\n\n".join(conventions_parts) if conventions_parts else "No specific conventions found. Will review for general code quality."
        
        # Debug conventions if enabled
        debug_conventions(conventions_context, similar_files)

        # If we found all issues with learned patterns, create review from them
        if not api_needed and learned_issues:
            review = {
                'has_issues': True,
                'severity': 'medium',
                'issues': learned_issues,
                'summary': f'Found {len(learned_issues)} issues based on learned repository patterns.'
            }
            # Update statistics
            if learning_manager:
                learning_manager.update_statistics(api_called=False)
        else:
            # Check cache
            cache_key = get_cache_key(diff, conventions_context[:1000])  # Use first 1000 chars for cache key
            cached_review = load_cached_review(cache_key)

            if cached_review:
                logger.info("Using cached review results")
                print("Using cached review results...")
                review = cached_review
            else:
                print("🔍 Reviewing staged changes against repository conventions...")
                logger.info("Sending review request to AI")
                # Review with AI
                review = review_code_with_conventions(diff, files_to_review, conventions_context)
                # Save to cache
                save_cached_review(cache_key, review)
                
                # Merge learned issues with API issues
                if learned_issues:
                    review['issues'] = learned_issues + review.get('issues', [])
                    review['has_issues'] = True
                
                # Update statistics
                if learning_manager:
                    learning_manager.update_statistics(api_called=True)

        # If no issues, allow commit
        if not review.get('has_issues', False):
            should_allow, output = format_review_output(review, [])
            print(output)
            sys.exit(0)

        # Present issues and offer fixes
        print(f"\n🔍 Found {len(review.get('issues', []))} convention issue(s) to review...\n")

        fixes_applied = []
        skip_all = False

        for i, issue in enumerate(review.get('issues', []), 1):
            if skip_all:
                break

            # Show the issue and get user decision
            response = interactive_fix_prompt(issue)

            if response == 'y':
                print("Applying fix...")
                if apply_fix(issue['file'], issue):
                    fixes_applied.append(i)
                    print("✅ Fix applied successfully!")
                    
                    # Update learning system with accepted fix
                    if learning_manager and not issue.get('learned', False):
                        try:
                            learning_manager.update_from_accepted_fix(
                                issue_type=issue.get('type', 'convention'),
                                original=issue.get('current_code', ''),
                                fixed=issue.get('fixed_code', ''),
                                file_path=issue['file']
                            )
                            logger.info("Updated learning from accepted fix")
                        except Exception as e:
                            logger.warning(f"Failed to update learning: {e}")
                else:
                    print("❌ Failed to apply fix.")
            elif response == 's':
                skip_all = True
                print("Skipping all remaining fixes...")
            elif response == 'q':
                print("\n❌ Review cancelled. Commit aborted.")
                sys.exit(1)
            else:  # 'n'
                print("Fix skipped.")
                
                # Update learning system with rejected fix
                if learning_manager and not issue.get('learned', False):
                    try:
                        learning_manager.update_from_rejected_fix(
                            issue_type=issue.get('type', 'convention'),
                            original=issue.get('current_code', ''),
                            fixed=issue.get('fixed_code', ''),
                            file_path=issue['file']
                        )
                        logger.info("Updated learning from rejected fix")
                    except Exception as e:
                        logger.warning(f"Failed to update learning: {e}")

        # Re-stage all modified files to ensure consistency
        if fixes_applied:
            print("\nRe-staging modified files...")
            for file in files_to_review:
                subprocess.run(['git', 'add', file], capture_output=True)

        # Format and display final results
        should_allow, output = format_review_output(review, fixes_applied)
        print(output)
        
        # Display learning statistics if available
        learned_count = sum(1 for issue in review.get('issues', []) if issue.get('learned', False))
        if learning_manager and learned_count > 0:
            try:
                stats = learning_manager.get_statistics()
                print("\n📊 Learning Statistics:")
                print(f"   API calls saved: {stats['api_calls_saved']} ({stats['api_reduction_rate']:.0f}%)")
                print(f"   Total patterns learned: {stats['total_patterns']}")
                print(f"   High confidence patterns: {stats['high_confidence_patterns']}")
            except Exception as e:
                logger.debug(f"Failed to display stats: {e}")

        # Exit with appropriate code
        sys.exit(0 if should_allow else 1)
        
    except KeyboardInterrupt:
        logger.info("Review interrupted by user")
        print("\n\nReview interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ An error occurred during review: {e}")
        
        if debug_mode():
            print("\n" + create_debug_report(e))
            print("\nPlease check the logs for more details.")
        else:
            print("\nRun with MARSDEVS_DEBUG=1 for more details.")
        
        # In case of error, allow commit to avoid blocking development
        print("\n⚠️  Due to the error, the commit will be allowed to proceed.")
        sys.exit(0)


if __name__ == "__main__":
    main()