# ==========================================
# File Name: logger.py
# Purpose:
#   Configure and provide centralized logging setup for the framework
# ==========================================

import os
import logging
from datetime import datetime

# ==========================================
# Function Name: setup_logger
# Purpose:
#   Initialize logging configurations, creating log directories and file handlers
#
# Input:
#   None
#
# Output:
#   logging.Logger: Configured logger instance
#
# Error Handling:
#   Gracefully handles file permissions and directory creation errors
# ==========================================
def setup_logger():
    try:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, "test_execution.log")
        
        logger = logging.getLogger("AutomationFramework")
        
        # Prevent duplicate handlers if logger is already configured
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create file handler
            fh = logging.FileHandler(log_file, encoding='utf-8')
            fh.setLevel(logging.INFO)
            
            # Create console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            # Add handlers to logger
            logger.addHandler(fh)
            logger.addHandler(ch)
            
        return logger
    except Exception as e:
        print(f"Failed to setup logger: {str(e)}")
        # Return a basic fallback stream logger
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("FallbackLogger")

# Get a global instance of logger for standard reuse
logger = setup_logger()
