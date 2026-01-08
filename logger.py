import logging
from typing import Optional
from pck67_pkg import TrackingClient

class TrackingHandler(logging.Handler):
    """Custom logging handler that logs to TrackingClient"""
    
    def __init__(self, client: TrackingClient, run_id: int):
        super().__init__()
        self.client = client
        self.run_id = run_id
        self.step_counter = 0
    
    def emit(self, record):
        """Send log record to tracking client"""
        try:
            log_entry = self.format(record)
            self.step_counter += 1
            self.client.log_message(self.run_id, log_entry, step=self.step_counter)
        except Exception:
            self.handleError(record)


def setup_tracking_logger(
    client: TrackingClient,
    run_id: int,
    name: str = "tracking",
    level: int = logging.INFO,
    console_output: bool = True
) -> logging.Logger:
    """
    Setup a logger that logs to both console and tracking client
    
    Args:
        client: TrackingClient instance
        run_id: Run ID to log to
        name: Logger name
        level: Logging level (default: INFO)
        console_output: Whether to also log to console (default: True)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Add tracking handler
    tracking_handler = TrackingHandler(client, run_id)
    tracking_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    tracking_handler.setFormatter(tracking_formatter)
    logger.addHandler(tracking_handler)
    
    # Optionally add console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger