import logging

logging.basicConfig(
    level=logging.INFO,  # Set the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='[%(levelname)s]:[%(asctime)s]:%(message)s',
    handlers=[
        logging.FileHandler('bc_recommendation_assistant.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Create a logger for your script or class
def get_logger(name):
    return logging.getLogger(name)
