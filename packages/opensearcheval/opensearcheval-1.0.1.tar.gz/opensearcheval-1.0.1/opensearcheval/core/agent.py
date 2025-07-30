import asyncio
from typing import Dict, List, Any, Callable, Optional
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Agent(ABC):
    """Base agent class for search evaluation tasks."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.tasks = []
        self.running = False
        logger.info(f"Agent {name} initialized with config: {config}")
    
    @abstractmethod
    async def process(self, data: Any) -> Any:
        """Process incoming data"""
        pass
    
    async def run(self):
        """Run the agent"""
        self.running = True
        logger.info(f"Agent {self.name} started")
        while self.running:
            if self.tasks:
                task = self.tasks.pop(0)
                await self.process(task)
            else:
                await asyncio.sleep(0.1)
    
    def stop(self):
        """Stop the agent"""
        self.running = False
        logger.info(f"Agent {self.name} stopped")
    
    def add_task(self, task: Any):
        """Add a task to the agent's queue"""
        self.tasks.append(task)
        logger.debug(f"Task added to {self.name}'s queue: {task}")


class SearchEvaluationAgent(Agent):
    """Agent specialized in search evaluation"""
    
    def __init__(self, name: str, config: Dict[str, Any], 
                 metrics: List[Callable], callback: Optional[Callable] = None):
        super().__init__(name, config)
        self.metrics = metrics
        self.callback = callback
        self.results = {}
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process search evaluation data"""
        query = data.get("query")
        results = data.get("results", [])
        user_interactions = data.get("user_interactions", [])
        relevance_judgments = data.get("relevance_judgments", {})
        
        evaluation = {}
        for metric_func in self.metrics:
            metric_name = metric_func.__name__
            try:
                metric_value = metric_func(query, results, relevance_judgments)
                evaluation[metric_name] = metric_value
            except Exception as e:
                logger.error(f"Error calculating metric {metric_name}: {str(e)}")
                evaluation[metric_name] = 0.0
        
        self.results[data.get("id")] = evaluation
        
        if self.callback:
            await self.callback(data.get("id"), evaluation)
        
        logger.info(f"Processed search evaluation for query: {query}")
        return evaluation


class ABTestAgent(Agent):
    """Agent specialized in A/B test analysis"""
    
    def __init__(self, name: str, config: Dict[str, Any], 
                 statistical_tests: List[Callable]):
        super().__init__(name, config)
        self.statistical_tests = statistical_tests
        self.experiment_results = {}
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process A/B test data"""
        experiment_id = data.get("experiment_id")
        control_group = data.get("control_group", {})
        treatment_group = data.get("treatment_group", {})
        
        analysis_results = {}
        
        # Process each metric separately
        for metric_name in control_group.get("metrics", {}):
            if metric_name not in treatment_group.get("metrics", {}):
                continue
                
            control_values = control_group["metrics"][metric_name]
            treatment_values = treatment_group["metrics"][metric_name]
            
            # Skip if not enough data
            if len(control_values) < 2 or len(treatment_values) < 2:
                analysis_results[metric_name] = {
                    "error": "Not enough data for statistical analysis"
                }
                continue
            
            # Run each statistical test
            metric_results = {}
            for test_func in self.statistical_tests:
                test_name = test_func.__name__
                try:
                    result = test_func(control_values, treatment_values)
                    metric_results[test_name] = result
                except Exception as e:
                    logger.error(f"Error in statistical test {test_name}: {str(e)}")
                    metric_results[test_name] = {"error": str(e)}
            
            analysis_results[metric_name] = metric_results
        
        self.experiment_results[experiment_id] = analysis_results
        
        logger.info(f"Processed A/B test analysis for experiment: {experiment_id}")
        return analysis_results


class UserBehaviorAgent(Agent):
    """Agent specialized in analyzing user behavior patterns"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name, config)
        self.behavior_patterns = {}
        self.user_sessions = {}
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user behavior data"""
        session_id = data.get("session_id")
        user_id = data.get("user_id")
        interactions = data.get("interactions", [])
        
        if not session_id or not interactions:
            logger.warning("Missing session_id or interactions in user behavior data")
            return {"error": "Missing required data"}
        
        # Store session data
        self.user_sessions[session_id] = {
            "user_id": user_id,
            "interactions": interactions,
            "processed_at": asyncio.get_event_loop().time()
        }
        
        # Analyze behavior patterns
        analysis = self._analyze_behavior(session_id, interactions)
        
        # Store the analysis
        self.behavior_patterns[session_id] = analysis
        
        logger.info(f"Processed user behavior for session: {session_id}")
        return analysis
    
    def _analyze_behavior(self, session_id: str, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user behavior patterns from interactions"""
        if not interactions:
            return {"session_id": session_id, "error": "No interactions to analyze"}
        
        # Sort interactions by timestamp
        sorted_interactions = sorted(interactions, key=lambda x: x.get("timestamp", 0))
        
        # Basic metrics
        search_count = sum(1 for i in interactions if i.get("type") == "search")
        click_count = sum(1 for i in interactions if i.get("type") == "click")
        scroll_count = sum(1 for i in interactions if i.get("type") == "scroll")
        
        # Calculate time on site
        if len(sorted_interactions) >= 2:
            first_time = sorted_interactions[0].get("timestamp", 0)
            last_time = sorted_interactions[-1].get("timestamp", 0)
            session_duration = last_time - first_time
        else:
            session_duration = 0
        
        # Click-through rate
        searches_with_clicks = 0
        total_searches = 0
        current_search = None
        
        for interaction in sorted_interactions:
            if interaction.get("type") == "search":
                if current_search is not None:
                    total_searches += 1
                    if current_search["has_clicks"]:
                        searches_with_clicks += 1
                
                current_search = {
                    "query": interaction.get("query"),
                    "has_clicks": False
                }
            
            elif interaction.get("type") == "click" and current_search is not None:
                current_search["has_clicks"] = True
        
        # Don't forget to count the last search
        if current_search is not None:
            total_searches += 1
            if current_search["has_clicks"]:
                searches_with_clicks += 1
        
        search_ctr = searches_with_clicks / total_searches if total_searches > 0 else 0
        
        # Average time between searches
        search_timestamps = [i.get("timestamp", 0) for i in interactions if i.get("type") == "search"]
        if len(search_timestamps) >= 2:
            time_diffs = [t2 - t1 for t1, t2 in zip(search_timestamps[:-1], search_timestamps[1:])]
            avg_time_between_searches = sum(time_diffs) / len(time_diffs)
        else:
            avg_time_between_searches = 0
        
        # User behavior pattern analysis
        behavior_pattern = "unknown"
        if search_count == 0:
            behavior_pattern = "browsing"
        elif click_count == 0:
            behavior_pattern = "scanning"
        elif search_ctr > 0.8:
            behavior_pattern = "engaged"
        elif search_count > 3 and search_ctr < 0.3:
            behavior_pattern = "frustrated"
        elif session_duration > 300:  # 5 minutes
            behavior_pattern = "researching"
        
        return {
            "session_id": session_id,
            "metrics": {
                "search_count": search_count,
                "click_count": click_count,
                "scroll_count": scroll_count,
                "session_duration": session_duration,
                "search_ctr": search_ctr,
                "avg_time_between_searches": avg_time_between_searches
            },
            "behavior_pattern": behavior_pattern,
            "timestamps": {
                "first_interaction": sorted_interactions[0].get("timestamp") if sorted_interactions else None,
                "last_interaction": sorted_interactions[-1].get("timestamp") if sorted_interactions else None
            }
        }


class AgentManager:
    """Manager for coordinating multiple agents"""
    
    def __init__(self):
        self.agents = {}
        self.tasks = asyncio.Queue()
    
    def register_agent(self, agent: Agent):
        """Register an agent with the manager"""
        self.agents[agent.name] = agent
        logger.info(f"Agent {agent.name} registered with manager")
    
    def unregister_agent(self, agent_name: str):
        """Unregister an agent from the manager"""
        if agent_name in self.agents:
            agent = self.agents.pop(agent_name)
            agent.stop()
            logger.info(f"Agent {agent_name} unregistered from manager")
    
    async def start_all(self):
        """Start all registered agents"""
        tasks = []
        for agent in self.agents.values():
            tasks.append(asyncio.create_task(agent.run()))
        logger.info(f"Started {len(tasks)} agents")
        return tasks
    
    def stop_all(self):
        """Stop all registered agents"""
        for agent in self.agents.values():
            agent.stop()
        logger.info("All agents stopped")
    
    async def dispatch_task(self, agent_name: str, task: Any):
        """Dispatch a task to a specific agent"""
        if agent_name in self.agents:
            self.agents[agent_name].add_task(task)
            logger.debug(f"Task dispatched to agent {agent_name}")
            return True
        logger.warning(f"Agent {agent_name} not found for task dispatch")
        return False