#!/usr/bin/env python3
"""
Command-line interface for MarsDevs Code Reviewer.
"""

import sys
import argparse
import subprocess
import os
import shutil
from pathlib import Path
from .reviewer import main as reviewer_main


def install_hook(force=False):
    """Install the pre-commit hook in the current Git repository."""
    if not os.path.exists('.git'):
        print("Error: Not in a Git repository. Please run from your project root.")
        return False
    
    hook_path = Path('.git/hooks/pre-commit')
    
    # Check if hook already exists
    if hook_path.exists() and not force:
        response = input("Pre-commit hook already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            return False
    
    # Create the hook content
    hook_content = '''#!/usr/bin/env python3
# MarsDevs Code Reviewer Pre-commit Hook

import sys
import os

# Add the marsdevs_reviewer package to Python path if needed
try:
    from marsdevs_reviewer import main
except ImportError:
    print("Error: marsdevs_reviewer package not found.")
    print("Please install it with: pip install marsdevs-reviewer")
    sys.exit(1)

# Run the reviewer
if __name__ == "__main__":
    main()
'''
    
    # Write the hook file
    hook_path.parent.mkdir(exist_ok=True)
    with open(hook_path, 'w') as f:
        f.write(hook_content)
    
    # Make it executable
    hook_path.chmod(0o755)
    
    print("✅ MarsDevs Code Reviewer pre-commit hook installed successfully!")
    print("\nUsage:")
    print("1. Make sure ANTHROPIC_API_KEY is set:")
    print("   export ANTHROPIC_API_KEY='your-api-key'")
    print("")
    print("2. The hook will automatically run when you commit:")
    print("   git add <files>")
    print("   git commit -m 'your message'")
    print("")
    print("3. To bypass the hook (use sparingly):")
    print("   git commit --no-verify -m 'your message'")
    
    return True


def uninstall_hook():
    """Uninstall the pre-commit hook."""
    hook_path = Path('.git/hooks/pre-commit')
    
    if not hook_path.exists():
        print("No pre-commit hook found.")
        return False
    
    # Check if it's our hook
    try:
        with open(hook_path, 'r') as f:
            content = f.read()
            if 'MarsDevs Code Reviewer' not in content:
                print("The existing pre-commit hook is not a MarsDevs hook.")
                response = input("Remove it anyway? (y/N): ")
                if response.lower() != 'y':
                    print("Uninstall cancelled.")
                    return False
    except Exception:
        pass
    
    # Remove the hook
    os.remove(hook_path)
    print("✅ Pre-commit hook removed successfully!")
    
    return True


def clear_cache():
    """Clear the review cache."""
    cache_dir = os.path.expanduser("~/.cache/marsdevs-reviewer")
    
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print(f"✅ Cache cleared: {cache_dir}")
    else:
        print("No cache found.")
    
    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MarsDevs Code Reviewer - AI-powered code review for Git commits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install pre-commit hook
  marsdevs-reviewer install
  
  # Run review manually
  marsdevs-reviewer review
  
  # Uninstall hook
  marsdevs-reviewer uninstall
  
  # Clear cache
  marsdevs-reviewer clear-cache
  
Environment Variables:
  ANTHROPIC_API_KEY - Your Anthropic API key (required)
        """
    )
    
    parser.add_argument(
        'command',
        choices=['install', 'uninstall', 'review', 'clear-cache'],
        help='Command to run'
    )
    
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force overwrite existing hooks'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    if args.command == 'install':
        success = install_hook(force=args.force)
        sys.exit(0 if success else 1)
    
    elif args.command == 'uninstall':
        success = uninstall_hook()
        sys.exit(0 if success else 1)
    
    elif args.command == 'review':
        # Check API key
        if not os.environ.get('ANTHROPIC_API_KEY'):
            print("Error: ANTHROPIC_API_KEY environment variable not set")
            print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
            sys.exit(1)
        
        # Run the reviewer
        reviewer_main()
    
    elif args.command == 'clear-cache':
        success = clear_cache()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()