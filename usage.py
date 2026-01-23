import pandas as pd
import numpy as np
import logging
from logger import auto_track_module

# Automatically set up tracking for this module using shared team/project
logger = auto_track_module(
    module_name="usage_example",
    team_name="Unilogger Team",
    project_name="Unilogger Project",
    run_name="Usage Example Run",
    config={"task": "experiment_demo"}
)
#write your code here 
# Test different logging levels
logger.debug("Debug: Starting the experiment setup...")
logger.info("Info: Starting from Jan 23 2026...")
logger.warning("Warning: This is a test run with multiple log levels")
logger.error("Error: Sample error message for testing")
logger.critical("Critical: Sample critical message for testing")

print("Usage example completed with automatic tracking!")