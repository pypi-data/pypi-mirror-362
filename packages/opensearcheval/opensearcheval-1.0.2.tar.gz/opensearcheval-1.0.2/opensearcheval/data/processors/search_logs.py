"""
Search log processor for OpenSearchEval
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class SearchLogProcessor:
    """Processor for search log data"""
    
    def __init__(self, log_format: str = "json"):
        """
        Initialize the search log processor
        
        Args:
            log_format: Format of the log files ("json", "csv", "tsv", "apache")
        """
        self.log_format = log_format
        self.processed_data = []
        
    def process_file(self, file_path: str) -> pd.DataFrame:
        """
        Process a search log file
        
        Args:
            file_path: Path to the log file
            
        Returns:
            DataFrame with processed search log data
        """
        logger.info(f"Processing search log file: {file_path}")
        
        if self.log_format == "json":
            return self._process_json_logs(file_path)
        elif self.log_format == "csv":
            return self._process_csv_logs(file_path)
        elif self.log_format == "tsv":
            return self._process_tsv_logs(file_path)
        elif self.log_format == "apache":
            return self._process_apache_logs(file_path)
        else:
            raise ValueError(f"Unsupported log format: {self.log_format}")
    
    def _process_json_logs(self, file_path: str) -> pd.DataFrame:
        """Process JSON log files"""
        records = []
        
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    processed_record = self._extract_search_data(record)
                    if processed_record:
                        records.append(processed_record)
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse JSON line: {line}")
                    continue
        
        return pd.DataFrame(records)
    
    def _process_csv_logs(self, file_path: str) -> pd.DataFrame:
        """Process CSV log files"""
        df = pd.read_csv(file_path)
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Extract search data
        processed_records = []
        for _, row in df.iterrows():
            processed_record = self._extract_search_data(row.to_dict())
            if processed_record:
                processed_records.append(processed_record)
        
        return pd.DataFrame(processed_records)
    
    def _process_tsv_logs(self, file_path: str) -> pd.DataFrame:
        """Process TSV log files"""
        df = pd.read_csv(file_path, sep='\t')
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Extract search data
        processed_records = []
        for _, row in df.iterrows():
            processed_record = self._extract_search_data(row.to_dict())
            if processed_record:
                processed_records.append(processed_record)
        
        return pd.DataFrame(processed_records)
    
    def _process_apache_logs(self, file_path: str) -> pd.DataFrame:
        """Process Apache-style log files"""
        # Common log format pattern
        log_pattern = r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+) "([^"]*)" "([^"]*)"'
        
        records = []
        with open(file_path, 'r') as f:
            for line in f:
                match = re.match(log_pattern, line)
                if match:
                    ip, timestamp, method, url, protocol, status, size, referer, user_agent = match.groups()
                    
                    # Extract query from URL
                    query = self._extract_query_from_url(url)
                    if query:
                        record = {
                            "timestamp": self._parse_apache_timestamp(timestamp),
                            "query": query,
                            "ip_address": ip,
                            "method": method,
                            "url": url,
                            "status_code": int(status),
                            "response_size": int(size),
                            "user_agent": user_agent
                        }
                        records.append(record)
        
        return pd.DataFrame(records)
    
    def _extract_search_data(self, record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract search-related data from a log record"""
        # Look for common search fields
        query = record.get("query") or record.get("q") or record.get("search_query")
        if not query:
            return None
        
        # Extract timestamp
        timestamp = record.get("timestamp") or record.get("time") or record.get("@timestamp")
        if timestamp:
            timestamp = self._parse_timestamp(timestamp)
        
        # Extract other fields
        user_id = record.get("user_id") or record.get("userId") or record.get("uid")
        session_id = record.get("session_id") or record.get("sessionId") or record.get("sid")
        search_id = record.get("search_id") or record.get("searchId")
        
        return {
            "timestamp": timestamp,
            "query": query,
            "user_id": user_id,
            "session_id": session_id,
            "search_id": search_id,
            "results_count": record.get("results_count", 0),
            "response_time": record.get("response_time", 0),
            "ip_address": record.get("ip_address"),
            "user_agent": record.get("user_agent"),
            "page": record.get("page", 1),
            "per_page": record.get("per_page", 10)
        }
    
    def _extract_query_from_url(self, url: str) -> Optional[str]:
        """Extract search query from URL"""
        # Common query parameters
        query_params = ["q", "query", "search", "s", "term"]
        
        from urllib.parse import urlparse, parse_qs
        
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)
        
        for param in query_params:
            if param in query_dict:
                return query_dict[param][0]
        
        return None
    
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
                "%d/%b/%Y:%H:%M:%S %z"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(timestamp, fmt)
                except ValueError:
                    continue
        
        return None
    
    def _parse_apache_timestamp(self, timestamp: str) -> Optional[datetime]:
        """Parse Apache log timestamp"""
        try:
            return datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
        except ValueError:
            return None
    
    def aggregate_by_query(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate search data by query"""
        return df.groupby("query").agg({
            "timestamp": ["count", "min", "max"],
            "user_id": "nunique",
            "session_id": "nunique",
            "results_count": "mean",
            "response_time": "mean"
        }).reset_index()
    
    def get_top_queries(self, df: pd.DataFrame, top_n: int = 100) -> pd.DataFrame:
        """Get top N queries by frequency"""
        query_counts = df.groupby("query").size()
        query_counts.name = "count"
        return query_counts.reset_index().sort_values("count", ascending=False).head(top_n) 