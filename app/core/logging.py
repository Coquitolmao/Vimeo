import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Configure the root logger to output to console with the specified log level.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure basic logging
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set 3rd party loggers to warning to avoid noise
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.info("Logging configured with level: %s", settings.LOG_LEVEL)
