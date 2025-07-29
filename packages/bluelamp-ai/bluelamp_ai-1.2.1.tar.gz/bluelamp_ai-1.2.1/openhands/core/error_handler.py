"""
Enhanced error handling for OpenHands to prevent forced termination.
"""
import logging
import os
import traceback
from typing import Any, Callable, Optional

from openhands.core.exceptions import LLMMalformedActionError
from openhands.core.logger import openhands_logger as logger


class ErrorHandler:
    """Enhanced error handler to prevent system crashes."""
    
    def __init__(self, continue_on_error: bool | None = None, max_retries: int | None = None):
        # Check environment variables for configuration
        self.continue_on_error = (
            continue_on_error 
            if continue_on_error is not None 
            else os.getenv('OPENHANDS_CONTINUE_ON_ERROR', 'true').lower() == 'true'
        )
        self.max_retries = (
            max_retries 
            if max_retries is not None 
            else int(os.getenv('OPENHANDS_MAX_RETRIES', '3'))
        )
        self.error_count = 0
        
    def handle_path_error(self, error: Exception, attempted_path: str) -> bool:
        """
        Handle path-related errors gracefully.
        
        Args:
            error: The exception that occurred
            attempted_path: The path that caused the error
            
        Returns:
            bool: True if error was handled and execution should continue
        """
        logger.warning(f"Path access error for {attempted_path}: {str(error)}")
        
        if isinstance(error, LLMMalformedActionError):
            # Extract the working directory from the error
            if "You can only work with files in" in str(error):
                allowed_path = str(error).split("You can only work with files in ")[-1].rstrip(".")
                logger.info(f"Restricting operations to allowed path: {allowed_path}")
                return True
                
        self.error_count += 1
        
        if self.continue_on_error and self.error_count <= self.max_retries:
            logger.info(f"Continuing execution despite error (attempt {self.error_count}/{self.max_retries})")
            return True
        
        return False
    
    def wrap_function(self, func: Callable) -> Callable:
        """
        Wrap a function with error handling.
        
        Args:
            func: Function to wrap
            
        Returns:
            Wrapped function with error handling
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except LLMMalformedActionError as e:
                if "Invalid path" in str(e):
                    if self.handle_path_error(e, str(e)):
                        logger.info("Path error handled, continuing execution")
                        return None
                raise e
            except Exception as e:
                logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                logger.debug(traceback.format_exc())
                if self.continue_on_error:
                    return None
                raise e
        
        return wrapper
    
    def reset_error_count(self):
        """Reset the error counter."""
        self.error_count = 0


# Global error handler instance
global_error_handler = ErrorHandler()


def handle_malformed_action_error(error: LLMMalformedActionError) -> Optional[str]:
    """
    Handle LLMMalformedActionError specifically for path issues.
    
    Args:
        error: The malformed action error
        
    Returns:
        Optional error message or None if handled
    """
    error_msg = str(error)
    
    # Check if it's a path restriction error
    if "Invalid path" in error_msg and "You can only work with files in" in error_msg:
        # Extract the allowed path
        parts = error_msg.split("You can only work with files in ")
        if len(parts) > 1:
            allowed_path = parts[1].rstrip(".")
            logger.warning(f"Path restriction detected. Working directory limited to: {allowed_path}")
            
            # Return a helpful message instead of crashing
            return f"Path access restricted. Please use paths within: {allowed_path}"
    
    return None


def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Function result or None if error occurred
    """
    try:
        return func(*args, **kwargs)
    except LLMMalformedActionError as e:
        handled_msg = handle_malformed_action_error(e)
        if handled_msg:
            logger.info(handled_msg)
            return None
        raise e
    except Exception as e:
        logger.error(f"Error in safe_execute: {str(e)}")
        logger.debug(traceback.format_exc())
        return None