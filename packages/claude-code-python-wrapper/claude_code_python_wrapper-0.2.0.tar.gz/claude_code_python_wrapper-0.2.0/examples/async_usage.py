#!/usr/bin/env python3
"""Async usage examples for Claude CLI wrapper"""

import asyncio
import logging
from claude_cli import AsyncClaudeCLI, ClaudeOptions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def basic_examples():
    """Basic async usage examples"""
    claude = AsyncClaudeCLI(command="claudee")
    
    print("=== Basic Async Query ===")
    response = await claude.query("What is async/await in Python?")
    print(f"Response: {response.output}")
    print(f"Return code: {response.return_code}")
    
    print("\n=== Concurrent Queries ===")
    # Run multiple queries concurrently
    queries = [
        "What is Python?",
        "What is JavaScript?",
        "What is Rust?"
    ]
    
    tasks = [claude.query(q) for q in queries]
    responses = await asyncio.gather(*tasks)
    
    for query, response in zip(queries, responses):
        print(f"\nQuery: {query}")
        print(f"Response: {response.output[:100]}...")  # First 100 chars


async def streaming_example():
    """Example of streaming responses"""
    claude = AsyncClaudeCLI(command="claudee")
    
    print("\n=== Streaming Example ===")
    print("Streaming response for: 'Count from 1 to 10 slowly'")
    
    async for line in claude.stream_query("Count from 1 to 10 slowly"):
        print(f"Stream: {line}")


async def interactive_example():
    """Example of interactive session"""
    claude = AsyncClaudeCLI(command="claudee")
    
    print("\n=== Interactive Session Example ===")
    
    async with await claude.interactive_session("Hello! I'm ready to chat.") as session:
        # Send a few messages
        messages = [
            "What's 2 + 2?",
            "What's the capital of France?",
            "Tell me a short joke"
        ]
        
        for msg in messages:
            print(f"\nYou: {msg}")
            response = await session.send(msg)
            print(f"Claude: {response}")


async def error_handling_example():
    """Example of error handling"""
    claude = AsyncClaudeCLI(command="claudee")
    
    print("\n=== Error Handling Example ===")
    
    # Timeout example
    try:
        response = await claude.query(
            "Count to 1 million very slowly",
            timeout=2.0  # 2 second timeout
        )
        if response.error:
            print(f"Timeout error: {response.error}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Invalid command example
    try:
        bad_claude = AsyncClaudeCLI(command="nonexistent-command")
        await bad_claude.query("test")
    except RuntimeError as e:
        print(f"Command not found error: {e}")


async def batch_processing_example():
    """Example of batch processing with progress tracking"""
    claude = AsyncClaudeCLI(command="claudee")
    
    print("\n=== Batch Processing Example ===")
    
    # Process multiple files or tasks
    tasks = [
        {"id": 1, "prompt": "Explain list comprehensions in Python"},
        {"id": 2, "prompt": "What are Python decorators?"},
        {"id": 3, "prompt": "Explain async/await in Python"},
        {"id": 4, "prompt": "What are Python generators?"},
        {"id": 5, "prompt": "Explain context managers in Python"}
    ]
    
    async def process_task(task):
        """Process a single task"""
        response = await claude.query(task["prompt"])
        return {
            "id": task["id"],
            "prompt": task["prompt"],
            "response": response.output[:100] + "..." if len(response.output) > 100 else response.output
        }
    
    # Process all tasks concurrently with limit
    semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent requests
    
    async def process_with_semaphore(task):
        async with semaphore:
            return await process_task(task)
    
    results = await asyncio.gather(*[process_with_semaphore(task) for task in tasks])
    
    print("\nBatch Processing Results:")
    for result in results:
        print(f"\nTask {result['id']}: {result['prompt']}")
        print(f"Response: {result['response']}")


async def main():
    """Run all examples"""
    await basic_examples()
    await streaming_example()
    await interactive_example()
    await error_handling_example()
    await batch_processing_example()


if __name__ == "__main__":
    asyncio.run(main())