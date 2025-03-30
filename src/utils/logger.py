import os
import logging

def setup_logger():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, 'fleet_logs.txt'),
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )

def log(message):
    logging.info(message)