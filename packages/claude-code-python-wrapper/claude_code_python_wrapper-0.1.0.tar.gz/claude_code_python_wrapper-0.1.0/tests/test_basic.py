#!/usr/bin/env python3
"""Basic test script for Claude CLI wrapper"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import ClaudeCLI

def main():
    print("=== Basic Claude CLI Wrapper Test ===\n")
    
    try:
        # Initialize wrapper
        claude = ClaudeCLI(command="claudee")
        
        # Test queries
        queries = [
            "What is 2+2?",
            "What is the capital of France?",
            "Write a haiku about coding"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"Test {i}: {query}")
            response = claude.query(query)
            
            if response.return_code == 0:
                print(f"✓ Success: {response.output}")
            else:
                print(f"✗ Failed (code {response.return_code}): {response.error}")
            print("-" * 50 + "\n")
        
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure 'claudee' command is available in your PATH")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())