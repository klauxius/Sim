import sys
import os
from datetime import datetime

class Logger:
    def __init__(self, log_directory='logs'):
        self.terminal = sys.stdout
        self.log_directory = log_directory
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        self.log_file_path = self._get_log_file_path()
        self.log = open(self.log_file_path, "w")

    def _get_log_file_path(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.log_directory, f"simulation_log_{timestamp}.txt")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        self.log.close()

def setup_logger():
    logger = Logger()
    sys.stdout = logger
    return logger