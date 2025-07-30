import logging
from typing import Dict, List, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class SQLConnector:
    """Connector for SQL databases"""
    
    def __init__(self, connection_string: str):
        """
        Initialize the SQL connector
        
        Args:
            connection_string: SQLAlchemy connection string
        """
        self.connection_string = connection_string
        try:
            self.engine = create_engine(connection_string)
            logger.info(f"Initialized SQL connector with engine: {self.engine.name}")
        except Exception as e:
            logger.error(f"Error initializing SQL connector: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a DataFrame
        
        Args:
            query: SQL query string
            params: Parameters for the query
            
        Returns:
            DataFrame with query results
        """
        try:
            if params is None:
                params = {}
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                df = pd.DataFrame(result.fetchall())
                if result.keys():
                    df.columns = result.keys()
                
                logger.info(f"Executed query, returned {len(df)} rows")
                return df
        except SQLAlchemyError as e:
            logger.error(f"SQL error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def load_search_logs(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load search logs from the database
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with search logs
        """
        query = """
        SELECT 
            query_id,
            query_text,
            user_id,
            session_id,
            timestamp,
            num_results,
            result_ids
        FROM search_logs
        WHERE DATE(timestamp) BETWEEN :start_date AND :end_date
        ORDER BY timestamp DESC
        """
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        return self.execute_query(query, params)
    
    def load_click_logs(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load click logs from the database
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with click logs
        """
        query = """
        SELECT 
            click_id,
            query_id,
            user_id,
            session_id,
            doc_id,
            position,
            timestamp,
            dwell_time
        FROM click_logs
        WHERE DATE(timestamp) BETWEEN :start_date AND :end_date
        ORDER BY timestamp DESC
        """
        
        params = {
            "start_date": start_date,
            "end_date": end_date
        }
        
        return self.execute_query(query, params)
    
    def load_experiment_data(self, experiment_id: str) -> Dict[str, pd.DataFrame]:
        """
        Load data for a specific experiment
        
        Args:
            experiment_id: ID of the experiment
            
        Returns:
            Dictionary with experiment data frames
        """
        # Load experiment details
        exp_query = """
        SELECT *
        FROM experiments
        WHERE id = :experiment_id
        """
        
        # Load experiment metrics
        metrics_query = """
        SELECT 
            group_id,
            metric_name,
            metric_value,
            timestamp
        FROM experiment_metrics
        WHERE experiment_id = :experiment_id
        ORDER BY timestamp
        """
        
        try:
            experiment = self.execute_query(exp_query, {"experiment_id": experiment_id})
            metrics = self.execute_query(metrics_query, {"experiment_id": experiment_id})
            
            return {
                "experiment": experiment,
                "metrics": metrics
            }
        except Exception as e:
            logger.error(f"Error loading experiment data: {str(e)}")
            raise
    
    def save_experiment_results(self, experiment_id: str, results: Dict[str, Any]) -> bool:
        """
        Save experiment results to the database
        
        Args:
            experiment_id: ID of the experiment
            results: Dictionary with result data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # First, update experiment status if needed
            if "status" in results:
                status_query = """
                UPDATE experiments
                SET status = :status, updated_at = CURRENT_TIMESTAMP
                WHERE id = :experiment_id
                """
                
                with self.engine.connect() as connection:
                    connection.execute(
                        text(status_query),
                        {"experiment_id": experiment_id, "status": results["status"]}
                    )
            
            # Save metric results
            if "metrics" in results:
                # Create a list of metric records to insert
                metric_records = []
                for metric_name, metric_data in results["metrics"].items():
                    for group_id, values in metric_data.items():
                        if isinstance(values, list):
                            for value in values:
                                metric_records.append({
                                    "experiment_id": experiment_id,
                                    "group_id": group_id,
                                    "metric_name": metric_name,
                                    "metric_value": value,
                                    "timestamp": results.get("timestamp", "CURRENT_TIMESTAMP")
                                })
                
                if metric_records:
                    metrics_insert = """
                    INSERT INTO experiment_metrics
                    (experiment_id, group_id, metric_name, metric_value, timestamp)
                    VALUES (:experiment_id, :group_id, :metric_name, :metric_value, :timestamp)
                    """
                    
                    with self.engine.connect() as connection:
                        for record in metric_records:
                            connection.execute(text(metrics_insert), record)
            
            logger.info(f"Saved results for experiment: {experiment_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving experiment results: {str(e)}")
            return False