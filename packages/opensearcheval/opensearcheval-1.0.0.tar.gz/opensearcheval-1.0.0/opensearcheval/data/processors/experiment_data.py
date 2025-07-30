"""
Experiment data processor for OpenSearchEval
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class ExperimentDataProcessor:
    """Processor for experiment data"""
    
    def __init__(self):
        """Initialize the experiment data processor"""
        self.experiments = {}
        
    def process_experiment_data(self, experiment_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Process experiment data
        
        Args:
            experiment_data: Dictionary containing experiment data
            
        Returns:
            DataFrame with processed experiment data
        """
        logger.info(f"Processing experiment data for: {experiment_data.get('experiment_id')}")
        
        # Extract experiment metadata
        experiment_id = experiment_data.get("experiment_id") or "unknown"
        experiment_name = experiment_data.get("experiment_name") or "unknown"
        start_time = experiment_data.get("start_time")
        end_time = experiment_data.get("end_time")
        
        # Process participant data
        participants = experiment_data.get("participants", [])
        processed_records = []
        
        for participant in participants:
            participant_records = self._process_participant_data(
                participant, experiment_id, experiment_name
            )
            processed_records.extend(participant_records)
        
        df = pd.DataFrame(processed_records)
        
        # Add experiment metadata
        if not df.empty:
            df["experiment_id"] = experiment_id
            df["experiment_name"] = experiment_name
            df["experiment_start_time"] = start_time
            df["experiment_end_time"] = end_time
        
        return df
    
    def _process_participant_data(self, participant: Dict[str, Any], 
                                 experiment_id: str, experiment_name: str) -> List[Dict[str, Any]]:
        """Process data for a single participant"""
        participant_id = participant.get("participant_id") or "unknown"
        group = participant.get("group") or "unknown"  # control, treatment, etc.
        
        # Process search sessions
        sessions = participant.get("sessions", [])
        records = []
        
        for session in sessions:
            session_records = self._process_session_data(
                session, participant_id, group, experiment_id
            )
            records.extend(session_records)
        
        return records
    
    def _process_session_data(self, session: Dict[str, Any], participant_id: str,
                             group: str, experiment_id: str) -> List[Dict[str, Any]]:
        """Process data for a single session"""
        session_id = session.get("session_id") or "unknown"
        session_start = session.get("start_time")
        session_end = session.get("end_time")
        
        # Process search queries in the session
        queries = session.get("queries", [])
        records = []
        
        for query_data in queries:
            query_records = self._process_query_data(
                query_data, participant_id, group, experiment_id, session_id
            )
            records.extend(query_records)
        
        return records
    
    def _process_query_data(self, query_data: Dict[str, Any], participant_id: str,
                           group: str, experiment_id: str, session_id: str) -> List[Dict[str, Any]]:
        """Process data for a single query"""
        query = query_data.get("query")
        query_time = query_data.get("timestamp")
        
        # Process interactions for this query
        interactions = query_data.get("interactions", [])
        records = []
        
        for interaction in interactions:
            record = {
                "experiment_id": experiment_id,
                "participant_id": participant_id,
                "group": group,
                "session_id": session_id,
                "query": query,
                "query_time": query_time,
                "interaction_type": interaction.get("type"),
                "interaction_time": interaction.get("timestamp"),
                "doc_id": interaction.get("doc_id"),
                "position": interaction.get("position"),
                "dwell_time": interaction.get("dwell_time"),
                "click_url": interaction.get("url"),
                "user_rating": interaction.get("user_rating")
            }
            records.append(record)
        
        return records
    
    def calculate_experiment_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate experiment-level metrics"""
        if df.empty:
            return {}
        
        # Group by experiment and treatment group
        group_metrics = {}
        
        for group, group_data in df.groupby("group"):
            group_metrics[group] = {
                "participants": group_data["participant_id"].nunique(),
                "sessions": group_data["session_id"].nunique(),
                "queries": group_data["query"].nunique(),
                "interactions": len(group_data),
                "clicks": len(group_data[group_data["interaction_type"] == "click"]),
                "avg_dwell_time": group_data["dwell_time"].mean(),
                "avg_user_rating": group_data["user_rating"].mean()
            }
        
        return {
            "experiment_id": df["experiment_id"].iloc[0] if not df.empty else None,
            "experiment_name": df["experiment_name"].iloc[0] if not df.empty else None,
            "group_metrics": group_metrics,
            "total_participants": df["participant_id"].nunique(),
            "total_sessions": df["session_id"].nunique(),
            "total_queries": df["query"].nunique(),
            "total_interactions": len(df)
        }
    
    def prepare_ab_test_data(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Prepare data for A/B testing"""
        ab_test_data = {}
        
        # Calculate metrics by group
        for group, group_data in df.groupby("group"):
            # Calculate session-level metrics
            session_metrics = group_data.groupby("session_id").agg({
                "dwell_time": "mean",
                "user_rating": "mean",
                "interaction_type": lambda x: (x == "click").sum()
            }).reset_index()
            
            session_metrics.columns = ["session_id", "avg_dwell_time", "avg_rating", "click_count"]
            
            ab_test_data[group] = {
                "avg_dwell_time": session_metrics["avg_dwell_time"].tolist(),
                "avg_rating": session_metrics["avg_rating"].tolist(),
                "click_count": session_metrics["click_count"].tolist()
            }
        
        return ab_test_data
    
    def export_experiment_results(self, df: pd.DataFrame, output_file: str):
        """Export experiment results to CSV"""
        if df.empty:
            logger.warning("No data to export")
            return
        
        # Calculate summary statistics
        summary_stats = df.groupby(["experiment_id", "group"]).agg({
            "participant_id": "nunique",
            "session_id": "nunique",
            "query": "nunique",
            "dwell_time": ["mean", "std", "count"],
            "user_rating": ["mean", "std", "count"]
        }).reset_index()
        
        # Flatten column names
        summary_stats.columns = ["_".join(col) if col[1] else col[0] for col in summary_stats.columns]
        
        # Export to CSV
        summary_stats.to_csv(output_file, index=False)
        logger.info(f"Experiment results exported to {output_file}")
    
    def identify_significant_differences(self, df: pd.DataFrame, 
                                       metric: str = "dwell_time") -> Dict[str, Any]:
        """Identify significant differences between groups"""
        from scipy import stats
        
        groups = df["group"].unique()
        if len(groups) < 2:
            return {"error": "Need at least 2 groups for comparison"}
        
        # Calculate metric by session for each group
        group_data = {}
        for group in groups:
            group_df = df[df["group"] == group]
            session_metrics = group_df.groupby("session_id")[metric].mean()
            group_data[group] = session_metrics.dropna().values
        
        # Perform statistical tests
        results = {}
        group_names = list(group_data.keys())
        
        for i in range(len(group_names)):
            for j in range(i + 1, len(group_names)):
                group1, group2 = group_names[i], group_names[j]
                data1, data2 = group_data[group1], group_data[group2]
                
                if len(data1) > 0 and len(data2) > 0:
                    # T-test
                    t_stat, t_p_value = stats.ttest_ind(data1, data2)
                    
                    # Mann-Whitney U test
                    u_stat, u_p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                    
                    results[f"{group1}_vs_{group2}"] = {
                        "t_test": {"statistic": t_stat, "p_value": t_p_value},
                        "mann_whitney": {"statistic": u_stat, "p_value": u_p_value},
                        "effect_size": (data2.mean() - data1.mean()) / data1.std() if data1.std() > 0 else 0,
                        "group1_mean": data1.mean(),
                        "group2_mean": data2.mean(),
                        "group1_std": data1.std(),
                        "group2_std": data2.std()
                    }
        
        return results 