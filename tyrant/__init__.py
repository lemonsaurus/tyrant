import logging

# Set up the logger with our desired format.
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)-7s] %(message)s')

# Discord logger is very noisy. This will shut it up.
logging.getLogger("discord").setLevel(logging.ERROR)
