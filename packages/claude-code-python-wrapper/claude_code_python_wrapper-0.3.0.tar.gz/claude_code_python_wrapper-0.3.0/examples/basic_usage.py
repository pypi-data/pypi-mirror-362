#!/usr/bin/env python3
"""Basic usage examples for Claude CLI wrapper"""

import logging
from claude_cli import ClaudeCLI, ClaudeOptions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    # Initialize wrapper
    claude = ClaudeCLI(command="claudee")
    
    print("=== Basic Query Example ===")
    # Simple query
    response = claude.query("What is Python?")
    print(f"Response: {response.output}")
    print(f"Return code: {response.return_code}")
    
    print("\n=== Query with Options ===")
    # Query with options
    options = ClaudeOptions(
        model="sonnet",  # Available: "sonnet" or "opus"
        print_mode=True,  # Use print mode for non-interactive output
        output_format="text"
    )
    response = claude.query("Write a haiku about programming", options=options)
    print(f"Response: {response.output}")
    
    print("\n=== JSON Response Example ===")
    # Get JSON response
    try:
        json_response = claude.query_json(
            "List 3 Python features in JSON format",
            options=ClaudeOptions(output_format="json", print_mode=True)
        )
        print(f"JSON Response: {json_response}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
    
    print("\n=== Working Directory Example ===")
    # Query with specific working directory
    response = claude.query(
        "List files in current directory",
        cwd="/tmp"
    )
    print(f"Files in /tmp: {response.output}")
    
    print("\n=== Error Handling Example ===")
    # Example with timeout
    response = claude.query(
        "Tell me a very long story",
        timeout=5.0  # 5 second timeout
    )
    if response.error:
        print(f"Error occurred: {response.error}")
    
    print("\n=== Interactive Session Example ===")
    # Start interactive session
    print("Starting interactive session (type 'exit' to quit)...")
    proc = claude.interactive()
    
    try:
        # Send some commands
        proc.stdin.write("Hello Claude!\n")
        proc.stdin.flush()
        
        # Read response (in real usage, you'd handle this more robustly)
        import time
        time.sleep(1)  # Give it time to respond
        
        # Close the session
        proc.terminate()
        proc.wait()
    except Exception as e:
        print(f"Interactive session error: {e}")


if __name__ == "__main__":
    main()