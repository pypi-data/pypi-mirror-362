from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional

from opensearcheval.core.experiment import ExperimentManager

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

# Get ExperimentManager instance
def get_experiment_manager():
    # In a real app, this might be initialized in a dependency injection container
    from opensearcheval.api.main import experiment_manager
    return experiment_manager

@router.get("/summary")
async def get_dashboard_summary(
    manager: ExperimentManager = Depends(get_experiment_manager)
):
    """Get a summary of system metrics for the dashboard"""
    # List all experiments
    all_experiments = manager.list_experiments()
    running_experiments = [e for e in all_experiments if e.status == "running"]
    completed_experiments = [e for e in all_experiments if e.status == "completed"]
    
    # Prepare summary data
    return {
        "experiments": {
            "total": len(all_experiments),
            "running": len(running_experiments),
            "completed": len(completed_experiments)
        },
        "latest_experiments": [
            {
                "id": e.id,
                "name": e.name,
                "status": e.status,
                "created_at": e.created_at.isoformat()
            } 
            for e in sorted(all_experiments, key=lambda x: x.created_at, reverse=True)[:5]
        ]
    }

@router.get("/metrics-over-time/{experiment_id}")
async def get_metrics_over_time(
    experiment_id: str,
    metric: str,
    manager: ExperimentManager = Depends(get_experiment_manager)
):
    """Get metrics over time for a specific experiment"""
    experiment = manager.get_experiment(experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
    
    # This is a mock implementation - in a real system you'd fetch time series data
    # For now, we'll return some dummy data
    return {
        "experiment_id": experiment_id,
        "metric": metric,
        "timestamps": [
            (experiment.created_at + datetime.timedelta(hours=i)).isoformat()
            for i in range(24)
        ],
        "control_values": [0.5 + (i * 0.01) for i in range(24)],
        "treatment_values": [0.5 + (i * 0.015) for i in range(24)]
    }