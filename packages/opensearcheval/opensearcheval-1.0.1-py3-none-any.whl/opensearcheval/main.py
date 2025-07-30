import uvicorn
import os
import logging
from dotenv import load_dotenv
import argparse
import sys
from pathlib import Path

# Add the project root to the path if running as a script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Load environment variables from .env file
load_dotenv()

from opensearcheval.core.config import get_settings

# Set up logging
settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="OpenSearchEval: Advanced Search Evaluation Platform")
    parser.add_argument('--host', type=str, default=settings.API_HOST, help='Host to run the API server on')
    parser.add_argument('--port', type=int, default=settings.API_PORT, help='Port to run the API server on')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    parser.add_argument('--workers', type=int, default=1, help='Number of worker processes')
    parser.add_argument('--env', type=str, default='dev', choices=['dev', 'test', 'prod'], help='Environment to run in')
    
    args = parser.parse_args()
    
    if args.env == 'prod' and args.reload:
        logger.warning("Auto-reload is enabled in production environment. This is not recommended.")
    
    logger.info(f"Starting OpenSearchEval API on {args.host}:{args.port} in {args.env} environment")
    
    # Run the FastAPI application
    uvicorn.run(
        "opensearcheval.api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()