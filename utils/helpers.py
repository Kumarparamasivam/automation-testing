# ==========================================
# File Name: helpers.py
# Purpose:
#   Provide generic test data generation, config file parsing, and dictionary utils
# ==========================================

import os
import json
import random
import string
from utils.logger import logger

# ==========================================
# Function Name: load_json_file
# Purpose:
#   Load and parse a JSON configuration file safely
#
# Input:
#   file_path (str): Relative or absolute path to the file
#
# Output:
#   dict: Dictionary containing parsed JSON data, or empty dict on failure
#
# Error Handling:
#   Returns empty dict and logs an error if the file is missing or contains invalid JSON
# ==========================================
def load_json_file(file_path):
    try:
        resolved_path = file_path
        if not os.path.isabs(file_path):
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resolved_path = os.path.join(root_dir, file_path)
            
        if not os.path.exists(resolved_path):
            logger.warning(f"JSON configuration file not found at: {resolved_path}")
            return {}
            
        with open(resolved_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as jde:
        logger.error(f"Invalid JSON format in file {file_path}: {str(jde)}")
        return {}
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {str(e)}")
        return {}

# ==========================================
# Function Name: save_json_file
# Purpose:
#   Save a dictionary back to a JSON configuration file
#
# Input:
#   file_path (str): Path to write the JSON data
#   data (dict): The dictionary structure to serialise
#
# Output:
#   bool: True if write succeeded, False otherwise
#
# Error Handling:
#   Logs exceptions and returns False on error
# ==========================================
def save_json_file(file_path, data):
    try:
        resolved_path = file_path
        if not os.path.isabs(file_path):
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resolved_path = os.path.join(root_dir, file_path)
            
        # Ensure directories exist
        os.makedirs(os.path.dirname(resolved_path), exist_ok=True)
        
        with open(resolved_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error writing JSON file {file_path}: {str(e)}")
        return False

# ==========================================
# Function Name: generate_random_email
# Purpose:
#   Generate a realistic randomized email string for test case isolation
#
# Input:
#   domain (str): Domain suffix for the generated email address
#
# Output:
#   str: Randomly generated email address
#
# Error Handling:
#   None
# ==========================================
def generate_random_email(domain="example.com"):
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"user_{random_str}@{domain}"

# ==========================================
# Function Name: generate_random_string
# Purpose:
#   Generate a string of randomized characters
#
# Input:
#   length (int): Characters count
#
# Output:
#   str: Random string
#
# Error Handling:
#   None
# ==========================================
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
