"""
Test configuration and fixtures for OpenSearchEval tests
"""

import pytest
import asyncio
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os
import tempfile
import json

# Set up async test environment
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Sample data fixtures
@pytest.fixture
def sample_search_results():
    """Sample search results for testing"""
    return [
        {
            "doc_id": "doc1",
            "title": "Python Programming Tutorial",
            "snippet": "Learn Python programming with examples",
            "url": "https://example.com/python-tutorial",
            "score": 0.95
        },
        {
            "doc_id": "doc2", 
            "title": "Machine Learning Guide",
            "snippet": "Complete guide to machine learning",
            "url": "https://example.com/ml-guide",
            "score": 0.87
        },
        {
            "doc_id": "doc3",
            "title": "Data Science Handbook",
            "snippet": "Comprehensive data science handbook",
            "url": "https://example.com/ds-handbook",
            "score": 0.82
        }
    ]

@pytest.fixture
def sample_relevance_judgments():
    """Sample relevance judgments for testing"""
    return {
        "doc1": 2,  # Highly relevant
        "doc2": 1,  # Relevant
        "doc3": 0   # Not relevant
    }

@pytest.fixture
def sample_user_interactions():
    """Sample user interactions for testing"""
    return [
        {
            "type": "search",
            "timestamp": 1000000000,
            "query": "python tutorial",
            "results_count": 10
        },
        {
            "type": "click",
            "timestamp": 1000000005,
            "doc_id": "doc1",
            "position": 0,
            "dwell_time": 120
        },
        {
            "type": "click",
            "timestamp": 1000000015,
            "doc_id": "doc2",
            "position": 1,
            "dwell_time": 45
        }
    ]

@pytest.fixture
def sample_experiment_data():
    """Sample experiment data for testing"""
    return {
        "experiment_id": "exp_001",
        "experiment_name": "Test Experiment",
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-07T23:59:59Z",
        "participants": [
            {
                "participant_id": "user_001",
                "group": "control",
                "sessions": [
                    {
                        "session_id": "session_001",
                        "start_time": "2024-01-01T10:00:00Z",
                        "queries": [
                            {
                                "query": "python tutorial",
                                "timestamp": "2024-01-01T10:00:00Z",
                                "interactions": [
                                    {
                                        "type": "click",
                                        "timestamp": "2024-01-01T10:00:05Z",
                                        "doc_id": "doc1",
                                        "position": 0,
                                        "dwell_time": 120
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing"""
    return {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "scores": {
                            "relevance": 4.5,
                            "factuality": 4.0,
                            "completeness": 3.5
                        },
                        "overall_score": 4.0,
                        "explanation": "The document is highly relevant and factually accurate."
                    })
                }
            }
        ]
    }

@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_csv_file(temp_directory):
    """Create a sample CSV file for testing"""
    csv_path = os.path.join(temp_directory, "test_data.csv")
    
    data = {
        "timestamp": ["2024-01-01 10:00:00", "2024-01-01 10:00:05"],
        "query": ["python tutorial", "machine learning"],
        "user_id": ["user_001", "user_002"],
        "session_id": ["session_001", "session_002"],
        "results_count": [10, 8]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    
    return csv_path

@pytest.fixture
def sample_json_file(temp_directory):
    """Create a sample JSON file for testing"""
    json_path = os.path.join(temp_directory, "test_data.json")
    
    data = [
        {
            "timestamp": 1000000000,
            "query": "python tutorial",
            "user_id": "user_001",
            "session_id": "session_001",
            "results_count": 10
        },
        {
            "timestamp": 1000000005,
            "query": "machine learning",
            "user_id": "user_002",
            "session_id": "session_002",
            "results_count": 8
        }
    ]
    
    with open(json_path, 'w') as f:
        for record in data:
            json.dump(record, f)
            f.write('\n')
    
    return json_path

@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    class MockSettings:
        APP_NAME = "OpenSearchEval"
        APP_VERSION = "1.0.0"
        API_HOST = "127.0.0.1"
        API_PORT = 8000
        LLM_MODEL = "gpt-4-turbo"
        LLM_ENDPOINT = "https://api.openai.com/v1/chat/completions"
        LLM_API_KEY = "test-api-key"
        USE_MLX = False
        DB_TYPE = "sqlite"
        ENVIRONMENT = "test"
        DEBUG = True
        
        @property
        def database_url(self):
            return "sqlite:///:memory:"
    
    return MockSettings()

@pytest.fixture
def mock_agent_manager():
    """Mock agent manager for testing"""
    from opensearcheval.core.agent import AgentManager
    return AgentManager()

@pytest.fixture
def mock_experiment_manager():
    """Mock experiment manager for testing"""
    from opensearcheval.core.experiment import ExperimentManager
    return ExperimentManager()

# Async test helpers
@pytest.fixture
async def async_client():
    """Create an async HTTP client for testing"""
    import httpx
    async with httpx.AsyncClient() as client:
        yield client

# Test data generators
def generate_test_search_results(count: int = 10) -> List[Dict[str, Any]]:
    """Generate test search results"""
    results = []
    for i in range(count):
        results.append({
            "doc_id": f"doc_{i}",
            "title": f"Test Document {i}",
            "snippet": f"This is test document {i}",
            "url": f"https://example.com/doc_{i}",
            "score": 1.0 - (i * 0.1)
        })
    return results

def generate_test_interactions(count: int = 10) -> List[Dict[str, Any]]:
    """Generate test user interactions"""
    interactions = []
    base_time = 1000000000
    
    for i in range(count):
        interactions.append({
            "type": "click" if i % 2 == 0 else "search",
            "timestamp": base_time + (i * 10),
            "doc_id": f"doc_{i % 3}",
            "position": i % 5,
            "dwell_time": 30 + (i * 5)
        })
    
    return interactions

# Test utilities
@pytest.fixture
def create_test_data():
    """Factory function to create test data"""
    def _create_test_data(data_type: str, count: int = 10):
        if data_type == "search_results":
            return generate_test_search_results(count)
        elif data_type == "interactions":
            return generate_test_interactions(count)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    return _create_test_data

# Performance test fixtures
@pytest.fixture
def benchmark_data():
    """Large dataset for performance testing"""
    return {
        "search_results": generate_test_search_results(1000),
        "interactions": generate_test_interactions(1000),
        "relevance_judgments": {f"doc_{i}": i % 3 for i in range(1000)}
    }

# Mock external services
@pytest.fixture
def mock_openai_api(monkeypatch):
    """Mock OpenAI API responses"""
    import httpx
    
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            
            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps({
                                    "scores": {"relevance": 4.0},
                                    "overall_score": 4.0,
                                    "explanation": "Test response"
                                })
                            }
                        }
                    ]
                }
        
        return MockResponse()
    
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

# Database fixtures
@pytest.fixture
def test_db():
    """Create a test database"""
    import sqlite3
    
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        
        # Create test tables
        cursor.execute("""
            CREATE TABLE experiments (
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                created_at TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT,
                metric_name TEXT,
                metric_value REAL,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        yield conn

# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_environment():
    """Automatically clean up test environment"""
    yield
    # Cleanup code here if needed
    pass 