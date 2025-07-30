#!/usr/bin/env python3
"""Advanced usage examples for Claude CLI wrapper"""

import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any
from claude_cli import ClaudeCLI, AsyncClaudeCLI, ClaudeOptions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ClaudeProject:
    """Advanced wrapper for project-based Claude interactions"""
    
    def __init__(self, project_root: Path, command: str = "claudee"):
        self.project_root = Path(project_root).resolve()
        self.claude = ClaudeCLI(command=command)
        self.async_claude = AsyncClaudeCLI(command=command)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file"""
        full_path = self.project_root / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")
        
        prompt = f"Analyze the code in {file_path} and provide insights"
        response = self.claude.query(prompt, cwd=self.project_root)
        
        return {
            "file": str(file_path),
            "analysis": response.output,
            "success": response.return_code == 0
        }
    
    async def analyze_directory_async(self, directory: Path) -> List[Dict[str, Any]]:
        """Analyze all Python files in a directory asynchronously"""
        dir_path = self.project_root / directory
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")
        
        # Find all Python files
        py_files = list(dir_path.glob("**/*.py"))
        
        async def analyze_file_async(file_path: Path) -> Dict[str, Any]:
            relative_path = file_path.relative_to(self.project_root)
            prompt = f"Analyze the code structure and quality of {relative_path}"
            response = await self.async_claude.query(prompt, cwd=self.project_root)
            
            return {
                "file": str(relative_path),
                "analysis": response.output[:200] + "..." if len(response.output) > 200 else response.output,
                "success": response.return_code == 0
            }
        
        # Analyze all files concurrently
        tasks = [analyze_file_async(f) for f in py_files]
        results = await asyncio.gather(*tasks)
        
        return results
    
    def generate_documentation(self, module_path: Path) -> str:
        """Generate documentation for a module"""
        options = ClaudeOptions(
            system_prompt="You are a technical documentation expert. Generate clear, concise documentation.",
            max_tokens=2000
        )
        
        prompt = f"Generate comprehensive documentation for the module at {module_path}"
        response = self.claude.query(prompt, options=options, cwd=self.project_root)
        
        if response.return_code != 0:
            raise RuntimeError(f"Failed to generate documentation: {response.error}")
        
        return response.output
    
    def refactor_code(self, file_path: Path, refactor_type: str) -> str:
        """Suggest refactoring for code"""
        options = ClaudeOptions(
            system_prompt="You are a code refactoring expert. Suggest improvements while maintaining functionality.",
            temperature=0.3  # Lower temperature for more consistent refactoring
        )
        
        refactor_prompts = {
            "performance": "Optimize this code for better performance",
            "readability": "Refactor this code for better readability",
            "patterns": "Apply appropriate design patterns to this code",
            "modern": "Modernize this code using latest Python features"
        }
        
        prompt = f"{refactor_prompts.get(refactor_type, 'Refactor this code')} in {file_path}"
        response = self.claude.query(prompt, options=options, cwd=self.project_root)
        
        return response.output


class ClaudeCodeReviewer:
    """Automated code review using Claude"""
    
    def __init__(self, command: str = "claudee"):
        self.claude = AsyncClaudeCLI(command=command)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def review_changes(self, diff_content: str) -> Dict[str, Any]:
        """Review code changes from a diff"""
        options = ClaudeOptions(
            system_prompt="""You are a senior code reviewer. Review the provided diff and:
1. Identify potential bugs or issues
2. Suggest improvements
3. Check for security vulnerabilities
4. Verify best practices are followed
5. Rate the change (1-10) with justification""",
            temperature=0.2
        )
        
        prompt = f"Review this code diff:\n\n{diff_content}"
        response = await self.claude.query(prompt, options=options)
        
        # Parse structured review (in real usage, you might want Claude to return JSON)
        return {
            "review": response.output,
            "approved": "approved" in response.output.lower(),
            "has_issues": any(word in response.output.lower() for word in ["bug", "issue", "problem", "vulnerability"])
        }
    
    async def review_pull_request(self, pr_files: List[Dict[str, str]]) -> Dict[str, Any]:
        """Review multiple files in a pull request"""
        reviews = []
        
        for file_info in pr_files:
            review = await self.review_changes(file_info["diff"])
            reviews.append({
                "file": file_info["path"],
                "review": review
            })
        
        # Generate summary
        summary_prompt = "Summarize these code reviews and provide an overall assessment"
        all_reviews = "\n\n".join([f"File: {r['file']}\n{r['review']['review']}" for r in reviews])
        
        summary_response = await self.claude.query(f"{summary_prompt}:\n\n{all_reviews}")
        
        return {
            "file_reviews": reviews,
            "summary": summary_response.output,
            "overall_approved": all(r["review"]["approved"] for r in reviews)
        }


async def main():
    """Demonstrate advanced usage"""
    print("=== Project Analysis Example ===")
    
    # Example: Analyze current project
    project = ClaudeProject(".")
    
    # Analyze a specific file
    try:
        analysis = project.analyze_file(Path("claude_cli/wrapper.py"))
        print(f"File analysis: {analysis['analysis'][:200]}...")
    except FileNotFoundError:
        print("File not found")
    
    # Analyze directory
    print("\n=== Directory Analysis ===")
    results = await project.analyze_directory_async(Path("claude_cli"))
    for result in results:
        print(f"\nFile: {result['file']}")
        print(f"Analysis: {result['analysis']}")
    
    # Code review example
    print("\n=== Code Review Example ===")
    reviewer = ClaudeCodeReviewer()
    
    # Mock diff content
    diff_content = """
    @@ -10,6 +10,8 @@ class UserService:
         def get_user(self, user_id):
    -        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
    +        # Fixed SQL injection vulnerability
    +        return self.db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    """
    
    review = await reviewer.review_changes(diff_content)
    print(f"Review approved: {review['approved']}")
    print(f"Has issues: {review['has_issues']}")
    print(f"Review details: {review['review'][:300]}...")


if __name__ == "__main__":
    asyncio.run(main())