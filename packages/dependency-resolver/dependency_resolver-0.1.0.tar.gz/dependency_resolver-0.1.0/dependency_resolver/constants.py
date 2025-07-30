import os

# Defines where the home directory is - can be overridden
HOME_DIR = os.getenv("RESOLVER_HOME", os.getcwd())


LOG_DIR = os.getenv("RESOLVER_LOG_DIR", os.getcwd())
LOG_TO_FILE=f"{LOG_DIR}/resolver.log"
