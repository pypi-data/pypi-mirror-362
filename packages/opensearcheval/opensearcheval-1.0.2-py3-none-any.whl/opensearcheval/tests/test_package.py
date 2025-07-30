"""
Test package functionality and imports
"""

import pytest
import opensearcheval as ose


def test_package_imports():
    """Test that the main package imports work correctly"""
    # Test that we can import the main modules
    assert hasattr(ose, '__version__')
    assert hasattr(ose, '__author__')
    assert hasattr(ose, '__email__')
    
    # Test core functionality is available
    assert hasattr(ose, 'ExperimentManager')
    assert hasattr(ose, 'AgentManager')
    assert hasattr(ose, 'mean_reciprocal_rank')
    assert hasattr(ose, 'precision_at_k')
    assert hasattr(ose, 'ndcg_at_k')


def test_basic_metrics(sample_search_results, sample_relevance_judgments):
    """Test basic metric calculations"""
    # Test MRR calculation
    mrr = ose.mean_reciprocal_rank(
        query="python tutorial",
        results=sample_search_results,
        relevance_judgments=sample_relevance_judgments
    )
    assert isinstance(mrr, (int, float))
    assert 0 <= mrr <= 1
    
    # Test precision@k calculation
    precision = ose.precision_at_k(
        query="python tutorial",
        results=sample_search_results,
        relevance_judgments=sample_relevance_judgments,
        k=2
    )
    assert isinstance(precision, (int, float))
    assert 0 <= precision <= 1


def test_experiment_manager():
    """Test experiment manager functionality"""
    manager = ose.ExperimentManager()
    
    # Test creating an experiment
    experiment = manager.create_experiment(
        name="Test Experiment",
        description="Testing experiment creation",
        metrics=["mean_reciprocal_rank", "click_through_rate"]
    )
    
    assert experiment.name == "Test Experiment"
    assert experiment.description == "Testing experiment creation"
    assert "mean_reciprocal_rank" in experiment.metrics
    assert experiment.id in manager.experiments


def test_agent_manager():
    """Test agent manager functionality"""
    manager = ose.AgentManager()
    
    # Test that we can create the manager
    assert isinstance(manager.agents, dict)
    assert len(manager.agents) == 0
    
    # Test creating an agent
    agent = ose.SearchEvaluationAgent(
        name="test_agent",
        config={"test": True},
        metrics=[ose.mean_reciprocal_rank]
    )
    
    # Test registering agent
    manager.register_agent(agent)
    assert "test_agent" in manager.agents
    assert manager.agents["test_agent"] == agent


def test_package_metadata():
    """Test package metadata"""
    assert ose.__version__ == "1.0.0"
    assert ose.__author__ == "Nik Jois"
    assert ose.__email__ == "nikjois@llamasearch.ai"
    assert ose.__license__ == "MIT"
    assert ose.__description__ == "A comprehensive search evaluation platform with agent architecture"


def test_config_loading():
    """Test configuration loading"""
    settings = ose.get_settings()
    
    assert settings.APP_NAME == "OpenSearchEval"
    assert settings.APP_VERSION == "1.0.0"
    assert hasattr(settings, 'API_HOST')
    assert hasattr(settings, 'API_PORT')


if __name__ == "__main__":
    pytest.main([__file__]) 