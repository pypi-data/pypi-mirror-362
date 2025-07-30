import uuid
import enum
from typing import Dict, List, Any, Optional
import datetime
import logging
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)

class ExperimentType(str, enum.Enum):
    A_B = "A_B"
    MULTIVARIATE = "MULTIVARIATE"
    BANDIT = "BANDIT"

class ExperimentStatus(str, enum.Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class Experiment:
    """Represents an A/B test or experiment"""
    
    id: str
    name: str
    description: str
    experiment_type: ExperimentType
    status: ExperimentStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    owner: str
    metrics: List[str]
    traffic_split: Dict[str, float]
    confidence_level: float
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)
    
    def start(self):
        """Start the experiment"""
        if self.status != ExperimentStatus.CREATED and self.status != ExperimentStatus.PAUSED:
            logger.warning(f"Cannot start experiment {self.id} because it is in {self.status} state")
            return
            
        self.status = ExperimentStatus.RUNNING
        self.started_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        logger.info(f"Started experiment: {self.id}")
    
    def pause(self):
        """Pause the experiment"""
        if self.status != ExperimentStatus.RUNNING:
            logger.warning(f"Cannot pause experiment {self.id} because it is in {self.status} state")
            return
            
        self.status = ExperimentStatus.PAUSED
        self.updated_at = datetime.datetime.now()
        logger.info(f"Paused experiment: {self.id}")
    
    def complete(self):
        """Complete the experiment"""
        if self.status != ExperimentStatus.RUNNING and self.status != ExperimentStatus.PAUSED:
            logger.warning(f"Cannot complete experiment {self.id} because it is in {self.status} state")
            return
            
        self.status = ExperimentStatus.COMPLETED
        self.ended_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        logger.info(f"Completed experiment: {self.id}")
    
    def fail(self, reason: str):
        """Mark the experiment as failed"""
        self.status = ExperimentStatus.FAILED
        self.ended_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.results["failure_reason"] = reason
        logger.error(f"Experiment {self.id} failed: {reason}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert experiment to dictionary"""
        result = asdict(self)
        # Convert datetime objects to strings
        for key, value in result.items():
            if isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            elif isinstance(value, enum.Enum):
                result[key] = value.value
        return result


class ExperimentManager:
    """Manages experiments"""
    
    def __init__(self):
        self.experiments = {}
        logger.info("Initialized ExperimentManager")
    
    def create_experiment(self, 
                         name: str, 
                         description: str = "", 
                         experiment_type: ExperimentType = ExperimentType.A_B,
                         owner: str = "admin",
                         metrics: Optional[List[str]] = None,
                         traffic_split: Optional[Dict[str, float]] = None,
                         confidence_level: Optional[float] = None) -> Experiment:
        """Create a new experiment"""
        from opensearcheval.core.config import get_settings
        settings = get_settings()
        
        experiment_id = str(uuid.uuid4())
        now = datetime.datetime.now()
        
        # Set default values
        if metrics is None:
            metrics = ["mean_reciprocal_rank", "click_through_rate", "time_to_first_click"]
        
        if traffic_split is None:
            if experiment_type == ExperimentType.A_B:
                traffic_split = {"control": 0.5, "treatment": 0.5}
            else:
                traffic_split = {"control": 0.33, "treatment_a": 0.33, "treatment_b": 0.34}
        
        if confidence_level is None:
            confidence_level = settings.DEFAULT_EXPERIMENT_CONFIDENCE_LEVEL
        
        experiment = Experiment(
            id=experiment_id,
            name=name,
            description=description,
            experiment_type=experiment_type,
            status=ExperimentStatus.CREATED,
            created_at=now,
            updated_at=now,
            owner=owner,
            metrics=metrics,
            traffic_split=traffic_split,
            confidence_level=confidence_level
        )
        
        self.experiments[experiment_id] = experiment
        logger.info(f"Created experiment: {experiment_id}")
        
        return experiment
    
    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        """Get an experiment by ID"""
        return self.experiments.get(experiment_id)
    
    def list_experiments(self, 
                        status: Optional[ExperimentStatus] = None, 
                        owner: Optional[str] = None) -> List[Experiment]:
        """List experiments, optionally filtered by status or owner"""
        result = list(self.experiments.values())
        
        if status:
            result = [e for e in result if e.status == status]
        
        if owner:
            result = [e for e in result if e.owner == owner]
        
        # Sort by created date, newest first
        result.sort(key=lambda x: x.created_at, reverse=True)
        
        return result
    
    def delete_experiment(self, experiment_id: str) -> bool:
        """Delete an experiment"""
        if experiment_id in self.experiments:
            del self.experiments[experiment_id]
            logger.info(f"Deleted experiment: {experiment_id}")
            return True
        return False
    
    def update_experiment_results(self, experiment_id: str, results: Dict[str, Any]) -> bool:
        """Update the results of an experiment"""
        experiment = self.get_experiment(experiment_id)
        if not experiment:
            logger.warning(f"Cannot update results for unknown experiment: {experiment_id}")
            return False
        
        experiment.results.update(results)
        experiment.updated_at = datetime.datetime.now()
        logger.info(f"Updated results for experiment: {experiment_id}")
        
        return True