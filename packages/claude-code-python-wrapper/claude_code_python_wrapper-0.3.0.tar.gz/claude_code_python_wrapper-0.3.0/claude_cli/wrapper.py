"""Synchronous wrapper for Claude CLI"""

import subprocess
import json
import logging
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ClaudeOptions:
    """Options for Claude CLI execution
    
    Available models:
    - 'sonnet': Latest Sonnet model
    - 'opus': Latest Opus model  
    - Full model names like 'claude-sonnet-4-20250514'
    """
    # Working directory for command execution
    cwd: Optional[str] = None
    
    # Model selection (sonnet, opus, or full model name)
    model: Optional[str] = None
    fallback_model: Optional[str] = None
    
    # Tool access control
    allowed_tools: Optional[List[str]] = None
    disallowed_tools: Optional[List[str]] = None
    
    # Output/Input formats 
    output_format: Optional[str] = None  # "text", "json", "stream-json"
    input_format: Optional[str] = None   # "text", "stream-json"
    
    # Session management
    continue_session: bool = False
    resume_session: Optional[str] = None
    
    # Additional directories for tool access
    add_dirs: Optional[List[str]] = None
    
    # MCP configuration
    mcp_config: Optional[str] = None
    strict_mcp_config: bool = False
    
    # Mode options
    print_mode: bool = False
    debug: bool = False
    verbose: Optional[bool] = None
    ide_mode: bool = False
    dangerously_skip_permissions: bool = False
    
    # Additional arguments
    extra_args: List[str] = field(default_factory=list)


@dataclass
class ClaudeResponse:
    """Response from Claude CLI"""
    output: str
    return_code: int
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ClaudeCLI:
    """Synchronous wrapper for Claude CLI"""
    
    def __init__(
        self,
        command: str = "claudee",
        default_options: Optional[ClaudeOptions] = None,
        logger: Optional[logging.Logger] = None
    ):
        self.command = command
        self.default_options = default_options or ClaudeOptions()
        self.logger = logger or logging.getLogger(__name__)
        
        # Verify CLI is available
        self._verify_cli()
    
    def _verify_cli(self) -> None:
        """Verify that Claude CLI is installed and accessible"""
        try:
            result = subprocess.run(
                [self.command, "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                raise RuntimeError(f"Claude CLI '{self.command}' not found or not accessible")
            self.logger.info(f"Claude CLI version: {result.stdout.strip()}")
        except FileNotFoundError:
            raise RuntimeError(f"Claude CLI '{self.command}' not found in PATH")
    
    def _build_command(
        self,
        prompt: str,
        options: Optional[ClaudeOptions] = None
    ) -> List[str]:
        """Build command line arguments"""
        cmd = [self.command]
        
        # Merge options with defaults
        opts = options or self.default_options
        
        # Model selection
        if opts.model:
            cmd.extend(["--model", opts.model])
        
        if opts.fallback_model:
            cmd.extend(["--fallback-model", opts.fallback_model])
        
        # Output/Input formats
        if opts.output_format:
            cmd.extend(["--output-format", opts.output_format])
        
        if opts.input_format:
            cmd.extend(["--input-format", opts.input_format])
        
        # Tool access control
        if opts.allowed_tools:
            cmd.extend(["--allowedTools"] + opts.allowed_tools)
        
        if opts.disallowed_tools:
            cmd.extend(["--disallowedTools"] + opts.disallowed_tools)
        
        # Session management
        if opts.continue_session:
            cmd.append("--continue")
        
        if opts.resume_session:
            if opts.resume_session == "interactive":
                cmd.append("--resume")
            else:
                cmd.extend(["--resume", opts.resume_session])
        
        # Additional directories
        if opts.add_dirs:
            cmd.extend(["--add-dir"] + opts.add_dirs)
        
        # MCP configuration
        if opts.mcp_config:
            cmd.extend(["--mcp-config", opts.mcp_config])
        
        if opts.strict_mcp_config:
            cmd.append("--strict-mcp-config")
        
        # Mode options
        if opts.print_mode:
            cmd.append("--print")
        
        if opts.debug:
            cmd.append("--debug")
        
        if opts.verbose is not None:
            if opts.verbose:
                cmd.append("--verbose")
        
        if opts.ide_mode:
            cmd.append("--ide")
        
        if opts.dangerously_skip_permissions:
            cmd.append("--dangerously-skip-permissions")
        
        # Add extra arguments
        cmd.extend(opts.extra_args)
        
        # Add prompt
        cmd.append(prompt)
        
        return cmd
    
    def query(
        self,
        prompt: str,
        options: Optional[ClaudeOptions] = None,
        cwd: Optional[Union[str, Path]] = None,
        timeout: Optional[float] = None
    ) -> ClaudeResponse:
        """Execute a query to Claude CLI"""
        cmd = self._build_command(prompt, options)
        
        # Determine working directory
        work_dir = cwd or (options and options.cwd) or self.default_options.cwd
        if work_dir:
            work_dir = Path(work_dir).resolve()
        
        self.logger.debug(f"Executing command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=work_dir,
                timeout=timeout,
                check=False
            )
            
            response = ClaudeResponse(
                output=result.stdout,
                return_code=result.returncode,
                error=result.stderr if result.returncode != 0 else None,
                metadata={
                    "command": cmd,
                    "cwd": str(work_dir) if work_dir else None
                }
            )
            
            if result.returncode != 0:
                self.logger.error(f"Claude CLI error: {result.stderr}")
            
            return response
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out after {timeout} seconds")
            return ClaudeResponse(
                output="",
                return_code=-1,
                error=f"Command timed out after {timeout} seconds",
                metadata={"command": cmd, "timeout": timeout}
            )
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return ClaudeResponse(
                output="",
                return_code=-1,
                error=str(e),
                metadata={"command": cmd}
            )
    
    def query_json(
        self,
        prompt: str,
        options: Optional[ClaudeOptions] = None,
        cwd: Optional[Union[str, Path]] = None,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Execute a query and parse JSON response"""
        # Add JSON output flag
        opts = options or ClaudeOptions()
        if "--json" not in opts.extra_args:
            opts.extra_args = opts.extra_args + ["--json"]
        
        response = self.query(prompt, opts, cwd, timeout)
        
        if response.return_code != 0:
            raise RuntimeError(f"Claude CLI error: {response.error}")
        
        try:
            return json.loads(response.output)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    def interactive(
        self,
        initial_prompt: Optional[str] = None,
        options: Optional[ClaudeOptions] = None,
        cwd: Optional[Union[str, Path]] = None
    ) -> subprocess.Popen:
        """Start an interactive Claude CLI session"""
        cmd = [self.command]
        
        # Add interactive flag
        cmd.append("--interactive")
        
        # Apply options
        opts = options or self.default_options
        if opts.model:
            cmd.extend(["--model", opts.model])
        if opts.system_prompt:
            cmd.extend(["--system-prompt", opts.system_prompt])
        
        # Add initial prompt if provided
        if initial_prompt:
            cmd.extend(["--initial-prompt", initial_prompt])
        
        # Determine working directory
        work_dir = cwd or opts.cwd
        if work_dir:
            work_dir = Path(work_dir).resolve()
        
        self.logger.info(f"Starting interactive session: {' '.join(cmd)}")
        
        return subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=work_dir
        )