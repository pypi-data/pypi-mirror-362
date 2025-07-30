"""
Interaction data processor for OpenSearchEval
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class InteractionDataProcessor:
    """Processor for user interaction data"""
    
    def __init__(self):
        """Initialize the interaction data processor"""
        self.processed_data = []
        
    def process_interactions(self, interactions: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Process user interaction data
        
        Args:
            interactions: List of interaction records
            
        Returns:
            DataFrame with processed interaction data
        """
        logger.info(f"Processing {len(interactions)} interaction records")
        
        processed_records = []
        for interaction in interactions:
            processed_record = self._process_interaction(interaction)
            if processed_record:
                processed_records.append(processed_record)
        
        df = pd.DataFrame(processed_records)
        if not df.empty:
            df = self._enrich_interaction_data(df)
        
        return df
    
    def _process_interaction(self, interaction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single interaction record"""
        # Required fields
        interaction_type = interaction.get("type") or interaction.get("event_type")
        timestamp = interaction.get("timestamp") or interaction.get("time")
        
        if not interaction_type or not timestamp:
            logger.warning(f"Missing required fields in interaction: {interaction}")
            return None
        
        # Parse timestamp
        timestamp = self._parse_timestamp(timestamp)
        if not timestamp:
            logger.warning(f"Failed to parse timestamp: {interaction.get('timestamp')}")
            return None
        
        # Extract common fields
        user_id = interaction.get("user_id") or interaction.get("userId")
        session_id = interaction.get("session_id") or interaction.get("sessionId")
        query = interaction.get("query") or interaction.get("search_query")
        doc_id = interaction.get("doc_id") or interaction.get("document_id")
        position = interaction.get("position") or interaction.get("rank")
        
        # Extract type-specific fields
        type_specific = self._extract_type_specific_fields(interaction_type, interaction)
        
        base_record = {
            "timestamp": timestamp,
            "type": interaction_type,
            "user_id": user_id,
            "session_id": session_id,
            "query": query,
            "doc_id": doc_id,
            "position": position,
            "ip_address": interaction.get("ip_address"),
            "user_agent": interaction.get("user_agent"),
            "page": interaction.get("page", 1)
        }
        
        # Merge with type-specific fields
        base_record.update(type_specific)
        
        return base_record
    
    def _extract_type_specific_fields(self, interaction_type: str, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Extract fields specific to interaction type"""
        type_specific = {}
        
        if interaction_type == "click":
            type_specific.update({
                "click_url": interaction.get("url"),
                "click_title": interaction.get("title"),
                "dwell_time": interaction.get("dwell_time"),
                "is_quick_back": interaction.get("is_quick_back", False)
            })
        
        elif interaction_type == "search":
            type_specific.update({
                "results_count": interaction.get("results_count", 0),
                "response_time": interaction.get("response_time", 0),
                "filters": interaction.get("filters", {}),
                "sort_order": interaction.get("sort_order")
            })
        
        elif interaction_type == "scroll":
            type_specific.update({
                "scroll_position": interaction.get("scroll_position"),
                "scroll_direction": interaction.get("scroll_direction"),
                "viewport_height": interaction.get("viewport_height")
            })
        
        elif interaction_type == "hover":
            type_specific.update({
                "hover_duration": interaction.get("hover_duration"),
                "hover_element": interaction.get("hover_element")
            })
        
        elif interaction_type == "filter":
            type_specific.update({
                "filter_type": interaction.get("filter_type"),
                "filter_value": interaction.get("filter_value"),
                "filter_action": interaction.get("filter_action")  # add, remove, change
            })
        
        return type_specific
    
    def _parse_timestamp(self, timestamp: Union[str, int, float]) -> Optional[datetime]:
        """Parse timestamp from various formats"""
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp)
        
        if isinstance(timestamp, str):
            # Try common timestamp formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%d %H:%M:%S.%f"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(timestamp, fmt)
                except ValueError:
                    continue
        
        return None
    
    def _enrich_interaction_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enrich interaction data with derived fields"""
        # Sort by timestamp
        df = df.sort_values(["session_id", "timestamp"])
        
        # Add session-level enrichments
        df = self._add_session_features(df)
        
        # Add query-level enrichments
        df = self._add_query_features(df)
        
        # Add time-based features
        df = self._add_time_features(df)
        
        return df
    
    def _add_session_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add session-level features"""
        # Session order
        df["session_order"] = df.groupby("session_id").cumcount() + 1
        
        # Time since session start
        df["time_since_session_start"] = df.groupby("session_id")["timestamp"].transform(
            lambda x: (x - x.min()).dt.total_seconds().fillna(0)
        )
        
        # Session duration (only for last interaction in session)
        session_durations = df.groupby("session_id")["timestamp"].agg(["min", "max"])
        session_durations["session_duration"] = (
            session_durations["max"] - session_durations["min"]
        ).dt.total_seconds()
        
        df = df.merge(
            session_durations[["session_duration"]], 
            left_on="session_id", 
            right_index=True, 
            how="left"
        )
        
        return df
    
    def _add_query_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add query-level features"""
        # Query order in session
        df["query_order"] = df.groupby(["session_id", "query"]).cumcount() + 1
        
        # Time since query start
        df["time_since_query_start"] = df.groupby(["session_id", "query"])["timestamp"].transform(
            lambda x: (x - x.min()).dt.total_seconds()
        )
        
        return df
    
    def _add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features"""
        # Time between interactions
        df["time_since_last_interaction"] = df.groupby("session_id")["timestamp"].diff().dt.total_seconds()
        
        # Hour of day
        df["hour_of_day"] = df["timestamp"].dt.hour
        
        # Day of week
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        
        # Is weekend
        df["is_weekend"] = df["day_of_week"].isin([5, 6])
        
        return df
    
    def calculate_session_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate session-level metrics"""
        session_metrics = df.groupby("session_id").agg({
            "timestamp": ["min", "max", "count"],
            "type": lambda x: x.value_counts().to_dict(),
            "query": "nunique",
            "doc_id": "nunique",
            "user_id": "first",
            "session_duration": "first"
        }).reset_index()
        
        # Flatten column names
        session_metrics.columns = ["_".join(col) if col[1] else col[0] for col in session_metrics.columns]
        
        # Calculate derived metrics
        session_metrics["interaction_count"] = session_metrics["timestamp_count"]
        session_metrics["unique_queries"] = session_metrics["query_nunique"]
        session_metrics["unique_documents"] = session_metrics["doc_id_nunique"]
        
        return session_metrics
    
    def calculate_query_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate query-level metrics"""
        query_metrics = df.groupby(["session_id", "query"]).agg({
            "timestamp": ["min", "max", "count"],
            "type": lambda x: x.value_counts().to_dict(),
            "doc_id": "nunique",
            "position": "min"
        }).reset_index()
        
        # Flatten column names
        query_metrics.columns = ["_".join(col) if col[1] else col[0] for col in query_metrics.columns]
        
        # Calculate derived metrics
        query_metrics["interaction_count"] = query_metrics["timestamp_count"]
        query_metrics["unique_documents"] = query_metrics["doc_id_nunique"]
        query_metrics["query_duration"] = (
            query_metrics["timestamp_max"] - query_metrics["timestamp_min"]
        ).dt.total_seconds()
        
        return query_metrics
    
    def identify_behavior_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Identify user behavior patterns"""
        session_patterns = []
        
        for session_id, session_data in df.groupby("session_id"):
            pattern = self._classify_session_behavior(session_data)
            session_patterns.append({
                "session_id": session_id,
                "behavior_pattern": pattern["pattern"],
                "confidence": pattern["confidence"],
                "characteristics": pattern["characteristics"]
            })
        
        return pd.DataFrame(session_patterns)
    
    def _classify_session_behavior(self, session_data: pd.DataFrame) -> Dict[str, Any]:
        """Classify behavior pattern for a session"""
        interaction_counts = session_data["type"].value_counts()
        
        search_count = interaction_counts.get("search", 0)
        click_count = interaction_counts.get("click", 0)
        scroll_count = interaction_counts.get("scroll", 0)
        hover_count = interaction_counts.get("hover", 0)
        
        total_interactions = len(session_data)
        session_duration = session_data["session_duration"].iloc[0]
        unique_queries = session_data["query"].nunique()
        
        # Pattern classification logic
        if search_count == 0:
            return {
                "pattern": "browsing",
                "confidence": 0.9,
                "characteristics": {"no_searches": True}
            }
        
        elif click_count == 0 and search_count > 0:
            return {
                "pattern": "scanning",
                "confidence": 0.8,
                "characteristics": {"searches_without_clicks": True}
            }
        
        elif search_count > 0 and click_count / search_count > 0.8:
            return {
                "pattern": "focused",
                "confidence": 0.9,
                "characteristics": {"high_click_rate": True}
            }
        
        elif unique_queries > 5 and session_duration > 300:
            return {
                "pattern": "exploring",
                "confidence": 0.7,
                "characteristics": {"many_queries": True, "long_session": True}
            }
        
        elif scroll_count > click_count * 2:
            return {
                "pattern": "browsing",
                "confidence": 0.6,
                "characteristics": {"high_scroll_rate": True}
            }
        
        else:
            return {
                "pattern": "mixed",
                "confidence": 0.5,
                "characteristics": {"unclear_pattern": True}
            } 