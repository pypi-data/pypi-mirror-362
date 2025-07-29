"""CraftX.py Shell Executor Module

Shell command execution utilities.
"""

import subprocess
import sys
from typing import Dict, List, Optional, Tuple

class ShellExecutor:
    """Execute shell commands safely."""
    
    def __init__(self, timeout: int = 30):
        """Initialize the shell executor.
        
        Args:
            timeout: Command timeout in seconds
        """
        self.timeout = timeout
        self.last_result: Optional[Dict] = None
    
    def execute(self, command: str, shell: bool = True, capture_output: bool = True) -> Dict:
        """Execute a shell command.
        
        Args:
            command: Command to execute
            shell: Use shell for execution
            capture_output: Capture stdout/stderr
            
        Returns:
            Execution result dictionary
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture_output,
                text=True,
                timeout=self.timeout
            )
            
            execution_result = {
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout if capture_output else "",
                "stderr": result.stderr if capture_output else "",
                "success": result.returncode == 0
            }
            
            self.last_result = execution_result
            return execution_result
            
        except subprocess.TimeoutExpired:
            error_result = {
                "command": command,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {self.timeout} seconds",
                "success": False
            }
            self.last_result = error_result
            return error_result
            
        except Exception as e:
            error_result = {
                "command": command,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }
            self.last_result = error_result
            return error_result
    
    def get_last_result(self) -> Optional[Dict]:
        """Get the last execution result.
        
        Returns:
            Last execution result or None
        """
        return self.last_result
    
    def is_command_available(self, command: str) -> bool:
        """Check if a command is available.
        
        Args:
            command: Command to check
            
        Returns:
            True if command is available
        """
        try:
            if sys.platform == "win32":
                check_cmd = f"where {command}"
            else:
                check_cmd = f"which {command}"
            
            result = self.execute(check_cmd)
            return result["success"]
        except:
            return False
