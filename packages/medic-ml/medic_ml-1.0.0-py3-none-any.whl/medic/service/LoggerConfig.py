import logging
import coloredlogs # type: ignore
from datetime import datetime
import inspect
import os
import threading
import traceback
from functools import wraps
from typing import Callable
from .Utils import get_medic_subdir

log_filename: str|None = None  # Global variable for log filename

def log_exceptions(logger: logging.Logger) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the exception or handle it as needed
                thread_name = threading.current_thread().name
                logger.error(f"Error in thread {thread_name}: {e}\n{traceback.format_exc()}")
                raise # Re-raise the exception to preserve the original
        return wrapper
    return decorator


def set_log_filename(filename: str="medic.log", add_date: bool=True, level=logging.DEBUG) -> logging.Logger:
    """Sets the log filename with an optional date suffix.
    Args:
        filename (str, optional): The base filename for the log. Defaults to "medic.log".
        add_date (bool, optional): If True, adds the current date to the filename. Defaults to True.
    """
    global log_filename

    if add_date:
        date_suffix = datetime.now().strftime("%Y-%m-%d")
        
        if filename.lower().endswith(".log"):
            log_filename = filename.replace(".log", f"_{date_suffix}.log")
        else:
            log_filename = f"{filename}_{date_suffix}.log"
    else:
        log_filename = filename

    # Log file in ~/medic_files/logs directory
    logs_directory = get_medic_subdir("logs")
    log_filename = os.path.join(logs_directory, log_filename)      

    # Add "-----------------------" in the log file to start the current session
    with open(log_filename, 'a') as log_file:
        if threading.current_thread() is threading.main_thread():
            log_file.write(f"\n{'----- New start (' + threading.current_thread().name + ') ':-<80}\n")
        else:
            log_file.write(f"      New thread ({threading.current_thread().name})\n")

    # Root logger
    root_logger = logging.getLogger()
    root_logger.handlers = []  # Clear existing handlers
    root_logger.setLevel(logging.WARNING)  # Only show WARNING level and above
    root_logger.propagate = False

    # Terminal (console) handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)  # Ensure DEBUG level for detailed logs

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Ensure colored logs for terminal
    coloredlogs.install(level=logging.WARNING, logger=root_logger, stream=console_handler.stream)

    # werkzeug logs
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)  # Log level to INFO for console
    
    # Add logs for werkzeug in terminal
    werkzeug_console_handler = logging.StreamHandler()
    werkzeug_console_handler.setLevel(logging.INFO)
    werkzeug_console_handler.setFormatter(formatter)
    werkzeug_logger.addHandler(werkzeug_console_handler)
    werkzeug_logger.propagate = False

    return  init_logger()


def init_logger(module_name: str|None=None, level=logging.DEBUG) -> logging.Logger:
    """"medic.log"

    Args:
        module_name (str | None, optional): The name of the module for the logger. Defaults to None.
        level (int, optional): The logging level. Defaults to logging.DEBUG.
            Levels (from high to low): logging.CRITICAL logging.ERROR
                                       logging.WARNING logging.INFO logging.DEBUG

    Returns:
        logging.Logger: The configured logger instance
    """
    
    global log_filename
                   
    def get_module_name() -> str | None:
        cur_frame = inspect.currentframe()
        if not cur_frame:
            return None
        frame = cur_frame.f_back
        if not frame:
            return None
        module = inspect.getmodule(frame)
        if not module:
            return None
        return module.__name__

    if module_name is None:
        module_name = get_module_name() or "medic"
            
    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    logger.propagate = False
    
    if not logger.handlers:
        # Terminal (console) handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)        
        
        # File handler
        if log_filename is not None:
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)

        # Ensure colored logs for terminal
        coloredlogs.install(level=level, logger=logger, stream=console_handler.stream)

    return logger
