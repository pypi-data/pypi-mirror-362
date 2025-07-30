"""Asynchronous wrapper for Claude CLI"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, List, Union, AsyncIterator
from pathlib import Path

from .wrapper import ClaudeOptions, ClaudeResponse


class AsyncClaudeCLI:
    """Asynchronous wrapper for Claude CLI"""
    
    def __init__(
        self,
        command: str = "claudee",
        default_options: Optional[ClaudeOptions] = None,
        logger: Optional[logging.Logger] = None
    ):
        self.command = command
        self.default_options = default_options or ClaudeOptions()
        self.logger = logger or logging.getLogger(__name__)
        self._verified = False
    
    async def _verify_cli(self) -> None:
        """Verify that Claude CLI is installed and accessible"""
        if self._verified:
            return
            
        try:
            proc = await asyncio.create_subprocess_exec(
                self.command, "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                raise RuntimeError(f"Claude CLI '{self.command}' not found or not accessible")
            
            self.logger.info(f"Claude CLI version: {stdout.decode().strip()}")
            self._verified = True
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
        
        # Add options
        if opts.max_turns:
            cmd.extend(["--max-turns", str(opts.max_turns)])
        
        if opts.system_prompt:
            cmd.extend(["--system-prompt", opts.system_prompt])
        
        if opts.model:
            cmd.extend(["--model", opts.model])
        
        if opts.temperature is not None:
            cmd.extend(["--temperature", str(opts.temperature)])
        
        if opts.max_tokens:
            cmd.extend(["--max-tokens", str(opts.max_tokens)])
        
        if opts.allowed_tools:
            for tool in opts.allowed_tools:
                cmd.extend(["--allowed-tool", tool])
        
        if opts.permission_mode:
            cmd.extend(["--permission-mode", opts.permission_mode])
        
        # Add extra arguments
        cmd.extend(opts.extra_args)
        
        # Add prompt
        cmd.append(prompt)
        
        return cmd
    
    async def query(
        self,
        prompt: str,
        options: Optional[ClaudeOptions] = None,
        cwd: Optional[Union[str, Path]] = None,
        timeout: Optional[float] = None
    ) -> ClaudeResponse:
        """Execute a query to Claude CLI"""
        await self._verify_cli()
        
        cmd = self._build_command(prompt, options)
        
        # Determine working directory
        work_dir = cwd or (options and options.cwd) or self.default_options.cwd
        if work_dir:
            work_dir = Path(work_dir).resolve()
        
        self.logger.debug(f"Executing command: {' '.join(cmd)}")
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=work_dir
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                self.logger.error(f"Command timed out after {timeout} seconds")
                return ClaudeResponse(
                    output="",
                    return_code=-1,
                    error=f"Command timed out after {timeout} seconds",
                    metadata={"command": cmd, "timeout": timeout}
                )
            
            response = ClaudeResponse(
                output=stdout.decode(),
                return_code=proc.returncode,
                error=stderr.decode() if proc.returncode != 0 else None,
                metadata={
                    "command": cmd,
                    "cwd": str(work_dir) if work_dir else None
                }
            )
            
            if proc.returncode != 0:
                self.logger.error(f"Claude CLI error: {stderr.decode()}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return ClaudeResponse(
                output="",
                return_code=-1,
                error=str(e),
                metadata={"command": cmd}
            )
    
    async def query_json(
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
        
        response = await self.query(prompt, opts, cwd, timeout)
        
        if response.return_code != 0:
            raise RuntimeError(f"Claude CLI error: {response.error}")
        
        try:
            return json.loads(response.output)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    async def stream_query(
        self,
        prompt: str,
        options: Optional[ClaudeOptions] = None,
        cwd: Optional[Union[str, Path]] = None
    ) -> AsyncIterator[str]:
        """Stream output from Claude CLI"""
        await self._verify_cli()
        
        # Add streaming flag
        opts = options or ClaudeOptions()
        if "--stream" not in opts.extra_args:
            opts.extra_args = opts.extra_args + ["--stream"]
        
        cmd = self._build_command(prompt, opts)
        
        # Determine working directory
        work_dir = cwd or opts.cwd or self.default_options.cwd
        if work_dir:
            work_dir = Path(work_dir).resolve()
        
        self.logger.debug(f"Streaming command: {' '.join(cmd)}")
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=work_dir
        )
        
        try:
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                yield line.decode().rstrip()
        finally:
            await proc.wait()
            if proc.returncode != 0:
                stderr = await proc.stderr.read()
                self.logger.error(f"Stream error: {stderr.decode()}")
    
    async def interactive_session(
        self,
        initial_prompt: Optional[str] = None,
        options: Optional[ClaudeOptions] = None,
        cwd: Optional[Union[str, Path]] = None
    ) -> "InteractiveSession":
        """Start an interactive Claude CLI session"""
        await self._verify_cli()
        
        cmd = [self.command, "--interactive"]
        
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
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=work_dir
        )
        
        return InteractiveSession(proc, self.logger)


class InteractiveSession:
    """Handle an interactive Claude CLI session"""
    
    def __init__(self, process: asyncio.subprocess.Process, logger: logging.Logger):
        self.process = process
        self.logger = logger
        self._closed = False
    
    async def send(self, message: str) -> str:
        """Send a message and get response"""
        if self._closed:
            raise RuntimeError("Session is closed")
        
        # Send message
        self.process.stdin.write(message + "\n")
        await self.process.stdin.drain()
        
        # Read response
        response_lines = []
        while True:
            line = await self.process.stdout.readline()
            if not line:
                break
            line = line.decode().rstrip()
            response_lines.append(line)
            # Check for end of response marker
            if line == "---" or line.startswith("> "):
                break
        
        return "\n".join(response_lines)
    
    async def close(self) -> None:
        """Close the interactive session"""
        if not self._closed:
            self.process.stdin.close()
            await self.process.wait()
            self._closed = True
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()