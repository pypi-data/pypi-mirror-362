#!/usr/bin/env python3
"""Async test script for Claude CLI wrapper"""

import asyncio
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import AsyncClaudeCLI

async def main():
    print("=== Async Claude CLI Wrapper Test ===\n")
    
    claude = AsyncClaudeCLI(command="claudee")
    
    # Test 1: Single async query
    print("Test 1: Single async query")
    response = await claude.query("What is Python?")
    print(f"Response: {response.output}\n")
    
    # Test 2: Concurrent queries
    print("Test 2: Running 3 queries concurrently...")
    start_time = time.time()
    
    queries = [
        "What is machine learning?",
        "What is deep learning?", 
        "What is neural network?"
    ]
    
    # Run all queries concurrently
    tasks = [claude.query(q) for q in queries]
    responses = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Completed in {end_time - start_time:.2f} seconds\n")
    
    for query, response in zip(queries, responses):
        print(f"Query: {query}")
        print(f"Response: {response.output[:100]}...")
        print("-" * 50)
    
    # Test 3: Batch processing with semaphore
    print("\n\nTest 3: Batch processing with concurrency limit")
    
    # Create 5 tasks but limit to 2 concurrent
    questions = [
        "What is 1+1?",
        "What is 2+2?",
        "What is 3+3?",
        "What is 4+4?",
        "What is 5+5?"
    ]
    
    semaphore = asyncio.Semaphore(2)  # Limit to 2 concurrent requests
    
    async def query_with_semaphore(question):
        async with semaphore:
            print(f"  → Processing: {question}")
            response = await claude.query(question)
            print(f"  ← Answer: {response.output}")
            return response
    
    start_time = time.time()
    results = await asyncio.gather(*[query_with_semaphore(q) for q in questions])
    end_time = time.time()
    
    print(f"\nProcessed {len(results)} queries in {end_time - start_time:.2f} seconds")
    print(f"All queries successful: {all(r.return_code == 0 for r in results)}")

if __name__ == "__main__":
    asyncio.run(main())