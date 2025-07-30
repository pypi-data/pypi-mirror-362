#!/usr/bin/env python3
"""Simple test script for Claude CLI wrapper"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import ClaudeCLI, ClaudeOptions

def main():
    print("=== Testing Claude CLI Wrapper ===\n")
    
    try:
        # Initialize wrapper with claudee command
        print("Initializing ClaudeCLI with command 'claudee'...")
        claude = ClaudeCLI(command="claudee")
        print("✓ Initialization successful\n")
        
        # Test 1: Simple query
        print("Test 1: Simple query")
        print("Sending query: 'Hello! Can you tell me what 2+2 equals?'")
        response = claude.query("Hello! Can you tell me what 2+2 equals?")
        print(f"Response: {response.output}")
        print(f"Return code: {response.return_code}")
        print(f"Error (if any): {response.error}\n")
        
        # Test 2: Query with options
        print("Test 2: Query with options")
        options = ClaudeOptions(
            max_tokens=50,
            temperature=0.5
        )
        print("Sending query with options (max_tokens=50, temperature=0.5)")
        response = claude.query("Write a very short poem about Python", options=options)
        print(f"Response: {response.output}")
        print(f"Return code: {response.return_code}\n")
        
        # Test 3: Query with timeout
        print("Test 3: Query with timeout")
        print("Sending query with 3 second timeout")
        response = claude.query(
            "Count from 1 to 5 slowly", 
            timeout=3.0
        )
        print(f"Response: {response.output}")
        print(f"Return code: {response.return_code}")
        print(f"Error (if any): {response.error}\n")
        
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure 'claudee' command is available in your PATH")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    print("✓ All tests completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())