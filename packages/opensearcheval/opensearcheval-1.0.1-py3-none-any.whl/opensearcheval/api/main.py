from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional
import asyncio
import logging
from pydantic import BaseModel, Field
import os
import sys
import time

# Import from project
from opensearcheval.core.agent import AgentManager, SearchEvaluationAgent, ABTestAgent, UserBehaviorAgent
from opensearcheval.core.metrics import (
    mean_reciprocal_rank, precision_at_k, ndcg_at_k, 
    click_through_rate, time_to_first_click, abandoned_search_rate, 
    llm_judge_score, average_dwell_time
)
from opensearcheval.core.config import get_settings
from opensearcheval.core.experiment import ExperimentManager, ExperimentType, ExperimentStatus
from opensearcheval.ml.llm_judge import LLMJudge, evaluate_search_results

# Initialize FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.APP_NAME,
    description="A comprehensive search evaluation platform with agent architecture",
    version=settings.APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the agent manager and experiment manager
agent_manager = AgentManager()
experiment_manager = ExperimentManager()

# Models for API requests and responses
class SearchResult(BaseModel):
    doc_id: str
    title: str
    snippet: str
    url: Optional[str] = None
    score: Optional[float] = None

class UserInteraction(BaseModel):
    type: str  # "search", "click", "scroll", etc.
    timestamp: float
    query: Optional[str] = None
    doc_id: Optional[str] = None
    position: Optional[int] = None
    dwell_time: Optional[float] = None

class SearchEvaluationRequest(BaseModel):
    id: str
    query: str
    results: List[SearchResult]
    user_interactions: Optional[List[UserInteraction]] = []
    relevance_judgments: Optional[Dict[str, int]] = {}
    llm_judgments: Optional[Dict[str, float]] = {}

class SearchEvaluationResponse(BaseModel):
    id: str
    metrics: Dict[str, float]
    status: str = "success"

class ExperimentGroup(BaseModel):
    group_id: str
    metrics: Dict[str, List[float]]
    sample_size: int

class ABTestRequest(BaseModel):
    experiment_id: str
    control_group: ExperimentGroup
    treatment_group: ExperimentGroup
    confidence_level: float = 0.95

class ABTestResponse(BaseModel):
    experiment_id: str
    results: Dict[str, Any]
    status: str = "success"

class CreateExperimentRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    experiment_type: ExperimentType = ExperimentType.A_B
    owner: Optional[str] = "admin"
    metrics: Optional[List[str]] = None
    traffic_split: Optional[Dict[str, float]] = None
    confidence_level: Optional[float] = 0.95

class ExperimentResponse(BaseModel):
    id: str
    name: str
    description: str
    experiment_type: ExperimentType
    status: ExperimentStatus
    created_at: str
    updated_at: str
    started_at: Optional[str] = None
    ended_at: Optional[str] = None

class LLMJudgeRequest(BaseModel):
    query: str
    documents: List[Dict[str, Any]]
    evaluation_criteria: Optional[List[str]] = None

# Startup event to initialize agents
@app.on_event("startup")
async def startup_event():
    # Initialize search evaluation agent
    search_metrics = [
        mean_reciprocal_rank,
        lambda q, r, u: precision_at_k(q, r, u, k=10),
        lambda q, r, u: ndcg_at_k(q, r, u, k=10),
        click_through_rate,
        time_to_first_click,
        abandoned_search_rate,
        average_dwell_time
    ]
    
    search_eval_agent = SearchEvaluationAgent(
        name="search_evaluator",
        config={"metrics_k": 10},
        metrics=search_metrics
    )
    agent_manager.register_agent(search_eval_agent)
    
    # Initialize A/B test agent
    from opensearcheval.utils.stats import t_test, mann_whitney_u_test, bootstrap_test
    
    ab_test_agent = ABTestAgent(
        name="ab_tester",
        config={"confidence_level": 0.95},
        statistical_tests=[t_test, mann_whitney_u_test, bootstrap_test]
    )
    agent_manager.register_agent(ab_test_agent)
    
    # Initialize user behavior agent
    user_behavior_agent = UserBehaviorAgent(
        name="user_behavior_analyzer",
        config={}
    )
    agent_manager.register_agent(user_behavior_agent)
    
    # Initialize LLM judge
    llm_judge = LLMJudge(
        model_name=settings.LLM_MODEL, 
        config={
            "temperature": 0.1,
            "endpoint": settings.LLM_ENDPOINT,
            "api_key": settings.LLM_API_KEY
        }
    )
    
    # Start all agents
    await agent_manager.start_all()
    logger.info("All agents started successfully")
    
    # Create some default experiments
    experiment_manager.create_experiment(
        name="Default A/B Test",
        description="Default experiment for testing search quality",
        metrics=["mean_reciprocal_rank", "click_through_rate", "time_to_first_click"]
    )
    
    logger.info("Application startup complete")

# Shutdown event to clean up resources
@app.on_event("shutdown")
def shutdown_event():
    agent_manager.stop_all()
    logger.info("All agents stopped")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "version": settings.APP_VERSION,
        "agents": list(agent_manager.agents.keys()),
        "experiments": len(experiment_manager.experiments)
    }

# Search evaluation endpoint
@app.post("/api/v1/evaluate", response_model=SearchEvaluationResponse)
async def evaluate_search(request: SearchEvaluationRequest, background_tasks: BackgroundTasks):
    try:
        # Convert Pydantic models to dictionaries
        eval_data = request.dict()
        
        # Dispatch evaluation task to the agent
        await agent_manager.dispatch_task("search_evaluator", eval_data)
        
        # For demo purposes, calculate some metrics synchronously
        quick_metrics = {
            "mrr": mean_reciprocal_rank(
                request.query, 
                [r.dict() for r in request.results], 
                request.relevance_judgments or {}
            ),
            "ctr": click_through_rate(
                request.query, 
                [r.dict() for r in request.results], 
                [i.dict() for i in request.user_interactions]
            )
        }
        
        return SearchEvaluationResponse(
            id=request.id,
            metrics=quick_metrics,
            status="processing"
        )
    
    except Exception as e:
        logger.error(f"Error evaluating search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error evaluating search: {str(e)}")

# A/B test analysis endpoint
@app.post("/api/v1/analyze-ab-test", response_model=ABTestResponse)
async def analyze_ab_test(request: ABTestRequest):
    try:
        # Convert request to dictionary
        test_data = request.dict()
        
        # Dispatch analysis task to the agent
        await agent_manager.dispatch_task("ab_tester", test_data)
        
        # For demo purposes, return a placeholder response
        # In a real system, you might want to make this async and return results later
        return ABTestResponse(
            experiment_id=request.experiment_id,
            results={"status": "processing"},
            status="accepted"
        )
    
    except Exception as e:
        logger.error(f"Error analyzing A/B test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing A/B test: {str(e)}")

# Get evaluation results endpoint
@app.get("/api/v1/evaluation-results/{evaluation_id}", response_model=SearchEvaluationResponse)
async def get_evaluation_results(evaluation_id: str):
    try:
        # Get results from the agent
        search_eval_agent = agent_manager.agents.get("search_evaluator")
        if not search_eval_agent:
            raise HTTPException(status_code=404, detail="Search evaluation agent not found")
        
        results = search_eval_agent.results.get(evaluation_id)
        if not results:
            raise HTTPException(status_code=404, detail=f"No results found for evaluation ID: {evaluation_id}")
        
        return SearchEvaluationResponse(
            id=evaluation_id,
            metrics=results,
            status="complete"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving evaluation results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving evaluation results: {str(e)}")

# Get A/B test results endpoint
@app.get("/api/v1/ab-test-results/{experiment_id}")
async def get_ab_test_results(experiment_id: str):
    try:
        # Get results from the agent
        ab_test_agent = agent_manager.agents.get("ab_tester")
        if not ab_test_agent:
            raise HTTPException(status_code=404, detail="A/B test agent not found")
        
        results = ab_test_agent.experiment_results.get(experiment_id)
        if not results:
            raise HTTPException(status_code=404, detail=f"No results found for experiment ID: {experiment_id}")
        
        return ABTestResponse(
            experiment_id=experiment_id,
            results=results,
            status="complete"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving A/B test results: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving A/B test results: {str(e)}")

# LLM Judge endpoint
@app.post("/api/v1/llm-judge")
async def llm_judge_evaluation(request: LLMJudgeRequest):
    try:
        # Default evaluation criteria if none provided
        if not request.evaluation_criteria:
            request.evaluation_criteria = ["relevance", "factuality", "completeness"]
        
        # Evaluate the search results using LLM
        judgments = await evaluate_search_results(
            request.query, 
            request.documents, 
            request.evaluation_criteria
        )
        
        # Calculate average score
        avg_score = 0
        if judgments:
            total = 0
            count = 0
            for j in judgments:
                if "overall_score" in j:
                    total += j["overall_score"]
                    count += 1
            if count > 0:
                avg_score = total / count
        
        return {
            "query": request.query,
            "judgments": judgments,
            "average_score": avg_score
        }
    
    except Exception as e:
        logger.error(f"Error in LLM judge evaluation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in LLM judge evaluation: {str(e)}")

# Experiment endpoints
@app.post("/api/v1/experiments", response_model=ExperimentResponse)
async def create_experiment(request: CreateExperimentRequest):
    try:
        experiment = experiment_manager.create_experiment(
            name=request.name,
            description=request.description,
            experiment_type=request.experiment_type,
            owner=request.owner,
            metrics=request.metrics,
            traffic_split=request.traffic_split,
            confidence_level=request.confidence_level
        )
        
        return ExperimentResponse(**experiment.to_dict())
    
    except Exception as e:
        logger.error(f"Error creating experiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating experiment: {str(e)}")

@app.get("/api/v1/experiments", response_model=List[ExperimentResponse])
async def list_experiments(
    status: Optional[ExperimentStatus] = None,
    owner: Optional[str] = None
):
    try:
        experiments = experiment_manager.list_experiments(status=status, owner=owner)
        return [ExperimentResponse(**exp.to_dict()) for exp in experiments]
    
    except Exception as e:
        logger.error(f"Error listing experiments: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing experiments: {str(e)}")

@app.get("/api/v1/experiments/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(experiment_id: str):
    try:
        experiment = experiment_manager.get_experiment(experiment_id)
        if not experiment:
            raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
        
        return ExperimentResponse(**experiment.to_dict())
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting experiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting experiment: {str(e)}")

@app.post("/api/v1/experiments/{experiment_id}/start")
async def start_experiment(experiment_id: str):
    try:
        experiment = experiment_manager.get_experiment(experiment_id)
        if not experiment:
            raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
        
        experiment.start()
        return {"status": "success", "message": f"Experiment {experiment_id} started"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting experiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting experiment: {str(e)}")

@app.post("/api/v1/experiments/{experiment_id}/stop")
async def stop_experiment(experiment_id: str):
    try:
        experiment = experiment_manager.get_experiment(experiment_id)
        if not experiment:
            raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
        
        experiment.complete()
        return {"status": "success", "message": f"Experiment {experiment_id} stopped"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping experiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error stopping experiment: {str(e)}")

@app.delete("/api/v1/experiments/{experiment_id}")
async def delete_experiment(experiment_id: str):
    try:
        success = experiment_manager.delete_experiment(experiment_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
        
        return {"status": "success", "message": f"Experiment {experiment_id} deleted"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting experiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting experiment: {str(e)}")

# User behavior analysis endpoint
@app.post("/api/v1/analyze-user-behavior")
async def analyze_user_behavior(
    session_id: str,
    user_id: Optional[str] = None,
    interactions: List[Dict[str, Any]] = []
):
    try:
        data = {
            "session_id": session_id,
            "user_id": user_id or f"anonymous_{int(time.time())}",
            "interactions": interactions
        }
        
        # Dispatch to user behavior agent
        await agent_manager.dispatch_task("user_behavior_analyzer", data)
        
        return {
            "status": "processing",
            "message": f"User behavior analysis for session {session_id} in progress"
        }
    
    except Exception as e:
        logger.error(f"Error analyzing user behavior: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing user behavior: {str(e)}")

@app.get("/api/v1/user-behavior/{session_id}")
async def get_user_behavior_analysis(session_id: str):
    try:
        user_behavior_agent = agent_manager.agents.get("user_behavior_analyzer")
        if not user_behavior_agent:
            raise HTTPException(status_code=404, detail="User behavior agent not found")
        
        analysis = user_behavior_agent.behavior_patterns.get(session_id)
        if not analysis:
            raise HTTPException(status_code=404, detail=f"No analysis found for session ID: {session_id}")
        
        return analysis
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user behavior analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user behavior analysis: {str(e)}")