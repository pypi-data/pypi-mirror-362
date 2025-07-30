#!/usr/bin/env python3
"""Code analyzer using Claude CLI wrapper"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_cli import ClaudeCLI, ClaudeOptions
from pathlib import Path

class CodeAnalyzer:
    """Analyze code files using Claude"""
    
    def __init__(self):
        self.claude = ClaudeCLI(command="claudee")
    
    def analyze_code_quality(self, code: str, language: str = "python") -> dict:
        """Analyze code quality and suggest improvements"""
        prompt = f"""Analyze this {language} code and provide:
1. Code quality score (1-10)
2. Potential issues
3. Improvement suggestions

Code:
```{language}
{code}
```"""
        
        response = self.claude.query(prompt)
        
        return {
            "analysis": response.output,
            "success": response.return_code == 0
        }
    
    def generate_tests(self, code: str, language: str = "python") -> str:
        """Generate unit tests for code"""
        prompt = f"""Generate unit tests for this {language} code:

```{language}
{code}
```

Provide complete, runnable test code."""
        
        response = self.claude.query(prompt)
        return response.output if response.return_code == 0 else f"Error: {response.error}"
    
    def explain_code(self, code: str) -> str:
        """Explain what the code does"""
        prompt = f"""Explain what this code does in simple terms:

```
{code}
```"""
        
        response = self.claude.query(prompt)
        return response.output if response.return_code == 0 else f"Error: {response.error}"

def main():
    analyzer = CodeAnalyzer()
    
    # Example code to analyze
    sample_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
'''
    
    print("=== Code Analyzer Demo ===\n")
    
    # 1. Analyze code quality
    print("1. Code Quality Analysis")
    print("-" * 50)
    result = analyzer.analyze_code_quality(sample_code)
    if result["success"]:
        print(result["analysis"])
    else:
        print("Analysis failed")
    
    print("\n\n2. Code Explanation")
    print("-" * 50)
    explanation = analyzer.explain_code(sample_code)
    print(explanation)
    
    print("\n\n3. Generate Unit Tests")
    print("-" * 50)
    tests = analyzer.generate_tests(sample_code)
    print(tests)

if __name__ == "__main__":
    main()