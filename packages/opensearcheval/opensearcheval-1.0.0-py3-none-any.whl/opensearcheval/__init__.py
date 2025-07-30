"""
OpenSearchEval: Ultimate Search Evaluation Platform

A comprehensive platform for evaluating search quality, conducting A/B tests,
and analyzing user behavior with agent architecture and MLX integration.

Author: Nik Jois
Email: nikjois@llamasearch.ai
"""

__version__ = "1.0.0"
__author__ = "Nik Jois"
__email__ = "nikjois@llamasearch.ai"
__license__ = "MIT"
__description__ = "A comprehensive search evaluation platform with agent architecture"
__url__ = "https://github.com/llamasearchai/OpenSearchEval"

# Core imports
from opensearcheval.core.config import get_settings
from opensearcheval.core.experiment import ExperimentManager, Experiment, ExperimentType, ExperimentStatus
from opensearcheval.core.agent import AgentManager, SearchEvaluationAgent, ABTestAgent, UserBehaviorAgent
from opensearcheval.core.metrics import (
    mean_reciprocal_rank, 
    precision_at_k, 
    ndcg_at_k, 
    click_through_rate,
    time_to_first_click,
    abandoned_search_rate,
    llm_judge_score,
    average_dwell_time
)

# ML imports
from opensearcheval.ml.llm_judge import LLMJudge, evaluate_search_results
from opensearcheval.ml.embeddings import EmbeddingModel, MLXEmbeddingModel, ApiEmbeddingModel, create_embedding_model
from opensearcheval.ml.models import SearchRankingModel, ClickThroughRatePredictor, extract_features, train_ctr_model

# Utility imports
from opensearcheval.utils.stats import t_test, mann_whitney_u_test, bootstrap_test, power_analysis
from opensearcheval.utils.visualization import (
    metrics_time_series, 
    ab_test_results_plot, 
    user_behavior_heatmap, 
    metric_comparison_radar,
    figure_to_base64,
    save_figure
)

# Make key classes and functions available at package level
__all__ = [
    # Core classes
    'AgentManager',
    'SearchEvaluationAgent', 
    'ABTestAgent',
    'UserBehaviorAgent',
    'ExperimentManager',
    'Experiment',
    'ExperimentType',
    'ExperimentStatus',
    'get_settings',
    
    # Metrics
    'mean_reciprocal_rank',
    'precision_at_k',
    'ndcg_at_k',
    'click_through_rate',
    'time_to_first_click',
    'abandoned_search_rate',
    'llm_judge_score',
    'average_dwell_time',
    
    # ML components
    'LLMJudge',
    'evaluate_search_results',
    'EmbeddingModel',
    'MLXEmbeddingModel',
    'ApiEmbeddingModel',
    'create_embedding_model',
    'SearchRankingModel',
    'ClickThroughRatePredictor',
    'extract_features',
    'train_ctr_model',
    
    # Utilities
    't_test',
    'mann_whitney_u_test',
    'bootstrap_test',
    'power_analysis',
    'metrics_time_series',
    'ab_test_results_plot',
    'user_behavior_heatmap',
    'metric_comparison_radar',
    'figure_to_base64',
    'save_figure',
    
    # Package info
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    '__description__',
    '__url__'
] 