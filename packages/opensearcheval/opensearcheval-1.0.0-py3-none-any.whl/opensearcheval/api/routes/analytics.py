from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
import time

from opensearcheval.core.agent import AgentManager

router = APIRouter(prefix="/api/v1", tags=["analytics"])

# Get AgentManager instance
def get_agent_manager():
    # In a real app, this might be initialized in a dependency injection container
    from opensearcheval.api.main import agent_manager
    return agent_manager

@router.post("/analyze-user-behavior")
async def analyze_user_behavior(
    session_id: str,
    user_id: Optional[str] = None,
    interactions: List[Dict[str, Any]] = [],
    agent_manager: AgentManager = Depends(get_agent_manager)
):
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

@router.get("/user-behavior/{session_id}")
async def get_user_behavior_analysis(
    session_id: str,
    agent_manager: AgentManager = Depends(get_agent_manager)
):
    user_behavior_agent = agent_manager.agents.get("user_behavior_analyzer")
    if not user_behavior_agent:
        raise HTTPException(status_code=404, detail="User behavior agent not found")
    
    analysis = user_behavior_agent.behavior_patterns.get(session_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"No analysis found for session ID: {session_id}")
    
    return analysis