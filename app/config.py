import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Get environment variables with validation
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Log missing variables (but don't fail on startup)
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set - AI features will not work")
if not DATABASE_URL:
    logger.warning("DATABASE_URL not set - database features may not work") 