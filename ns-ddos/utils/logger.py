import logging

# Configure logging
logging.basicConfig(filename='ddos_detection.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def log_event(message):
    logging.info(message)
