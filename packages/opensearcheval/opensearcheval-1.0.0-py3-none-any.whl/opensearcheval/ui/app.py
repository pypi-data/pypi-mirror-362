from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import logging
import httpx
import asyncio
import argparse
from functools import wraps
from datetime import datetime
import json

from opensearcheval.core.config import get_settings

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)

# API base URL
API_BASE_URL = f"http://{settings.API_HOST}:{settings.API_PORT}"

# Helper function to make async HTTP requests work in Flask
def async_request(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return wrapper

# Routes
@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard page"""
    return render_template('dashboard.html')

@app.route('/experiments')
def experiments_list():
    """Render the experiments list page"""
    return render_template('experiments/list.html')

@app.route('/experiments/new')
def new_experiment():
    """Render the new experiment form"""
    return render_template('experiments/new.html')

@app.route('/experiments/<experiment_id>')
def view_experiment(experiment_id):
    """Render the experiment details page"""
    return render_template('experiments/detail.html', experiment_id=experiment_id)

@app.route('/analytics')
def analytics():
    """Render the analytics page"""
    return render_template('analytics.html')

@app.route('/llm-judge')
def llm_judge():
    """Render the LLM judge page"""
    return render_template('llm_judge.html')

@app.route('/documentation')
def documentation():
    """Render the API documentation page"""
    return render_template('documentation.html')

# API Proxy endpoints
@app.route('/api/<path:endpoint>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@async_request
async def api_proxy(endpoint):
    """Proxy requests to the API server"""
    url = f"{API_BASE_URL}/api/{endpoint}"
    
    try:
        async with httpx.AsyncClient() as client:
            if request.method == 'GET':
                response = await client.get(url, params=request.args)
            elif request.method == 'POST':
                response = await client.post(url, json=request.json)
            elif request.method == 'PUT':
                response = await client.put(url, json=request.json)
            elif request.method == 'DELETE':
                response = await client.delete(url)
            
            # Return the API response
            return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.error(f"API proxy error for {endpoint}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Main entry point
def main():
    parser = argparse.ArgumentParser(description="OpenSearchEval UI Server")
    parser.add_argument('--host', type=str, default=settings.UI_HOST, help='Host to run the UI server on')
    parser.add_argument('--port', type=int, default=settings.UI_PORT, help='Port to run the UI server on')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    logger.info(f"Starting UI server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()