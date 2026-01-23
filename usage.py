import pandas as pd
import numpy as np
import logging
from pck67_pkg import TrackingClient
from logger import setup_tracking_logger

# Initialize client
try:
    client = TrackingClient(api_key="51ef227e5469c6ca7446edfea41fefd0cab4ee4f20250706100d122b72a0cde5") # add ur api key
    
    # Get or create team named "My Team"
    teams = client.list_teams()
    team_exists = False
    for team in teams:
        if team['name'] == 'My Team':
            team_id = team['id']
            team_exists = True
            break

    if not team_exists:
        team = client.create_team("My Team", "Default team for logistics project")
        team_id = team['id']

    # Get or create project named "Logistics Project"
    projects = client.list_projects(team_id)
    project_exists = False
    for project in projects:
        if project['name'] == 'Logistics Project':
            project_id = project['id']
            project_exists = True
            break

    if not project_exists:
        project = client.create_project(team_id, "Logistics Project", "Project for logistics experiments")
        project_id = project['id']

    # Start a run
    run = client.init_run(
        project_id=project_id,
        name="somehting new ok pal", #this thing right u can change it as per the code name 
        config={"task": "classification"}
    )

    # Setup logger with DEBUG level to capture all log types
    logger = setup_tracking_logger(client, run.id, name="my_logger", level=logging.DEBUG)

    # Test different logging levels
    logger.debug("Debug: Starting the experiment setup...")
    logger.info("Info: Starting from Jan 23 2026...")
    logger.warning("Warning: This is a test run with multiple log levels")
    logger.error("Error: Sample error message for testing")
    logger.critical("Critical: Sample critical message for testing")



except Exception as e:
    print(f"Error connecting to tracking API: {e}")
    print("The tracking server might be temporarily unavailable. Please try again later.")