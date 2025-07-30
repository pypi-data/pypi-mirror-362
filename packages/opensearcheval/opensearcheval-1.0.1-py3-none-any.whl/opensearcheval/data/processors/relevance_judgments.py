"""
Relevance judgment processor for OpenSearchEval
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

class RelevanceJudgmentProcessor:
    """Processor for relevance judgment data"""
    
    def __init__(self):
        """Initialize the relevance judgment processor"""
        self.judgments = {}
        
    def process_judgments(self, judgments: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Process relevance judgment data
        
        Args:
            judgments: List of relevance judgment records
            
        Returns:
            DataFrame with processed relevance judgments
        """
        logger.info(f"Processing {len(judgments)} relevance judgments")
        
        processed_records = []
        for judgment in judgments:
            processed_record = self._process_judgment(judgment)
            if processed_record:
                processed_records.append(processed_record)
        
        return pd.DataFrame(processed_records)
    
    def _process_judgment(self, judgment: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single relevance judgment"""
        # Required fields
        query = judgment.get("query")
        doc_id = judgment.get("doc_id") or judgment.get("document_id")
        relevance = judgment.get("relevance") or judgment.get("relevance_score")
        
        if not query or not doc_id or relevance is None:
            logger.warning(f"Missing required fields in judgment: {judgment}")
            return None
        
        # Normalize relevance score
        relevance = self._normalize_relevance(relevance)
        
        return {
            "query": query,
            "doc_id": doc_id,
            "relevance": relevance,
            "judge_id": judgment.get("judge_id"),
            "judgment_time": judgment.get("judgment_time"),
            "confidence": judgment.get("confidence", 1.0),
            "query_intent": judgment.get("query_intent"),
            "document_category": judgment.get("document_category"),
            "notes": judgment.get("notes")
        }
    
    def _normalize_relevance(self, relevance: Union[int, float, str]) -> float:
        """Normalize relevance score to 0-1 range"""
        if isinstance(relevance, str):
            # Handle string relevance labels
            relevance_map = {
                "irrelevant": 0,
                "not_relevant": 0,
                "partially_relevant": 0.5,
                "relevant": 1,
                "highly_relevant": 1,
                "perfect": 1
            }
            return relevance_map.get(relevance.lower(), 0)
        
        # Handle numeric relevance scores
        if isinstance(relevance, (int, float)):
            # Assume 0-4 scale and normalize to 0-1
            if relevance >= 0 and relevance <= 4:
                return relevance / 4.0
            # Already in 0-1 range
            elif relevance >= 0 and relevance <= 1:
                return float(relevance)
            # Binary relevance
            elif relevance > 1:
                return 1.0
            else:
                return 0.0
        
        return 0.0
    
    def create_judgment_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create a query-document relevance matrix"""
        return df.pivot_table(
            index="query", 
            columns="doc_id", 
            values="relevance", 
            fill_value=0
        )
    
    def calculate_inter_annotator_agreement(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate inter-annotator agreement metrics"""
        # Group by query and doc_id to get multiple judgments
        judgment_groups = df.groupby(["query", "doc_id"])["relevance"].apply(list)
        
        agreements = []
        for judgments in judgment_groups:
            if len(judgments) > 1:
                # Calculate pairwise agreement
                pairwise_agreements = []
                for i in range(len(judgments)):
                    for j in range(i + 1, len(judgments)):
                        agreement = 1 - abs(judgments[i] - judgments[j])
                        pairwise_agreements.append(agreement)
                
                if pairwise_agreements:
                    agreements.append(sum(pairwise_agreements) / len(pairwise_agreements))
        
        if not agreements:
            return {"average_agreement": 0.0, "num_comparisons": 0}
        
        return {
            "average_agreement": sum(agreements) / len(agreements),
            "num_comparisons": len(agreements)
        }
    
    def get_judgment_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get statistics about relevance judgments"""
        return {
            "total_judgments": len(df),
            "unique_queries": df["query"].nunique(),
            "unique_documents": df["doc_id"].nunique(),
            "unique_judges": df["judge_id"].nunique() if "judge_id" in df.columns else 0,
            "relevance_distribution": df["relevance"].value_counts().to_dict(),
            "average_relevance": df["relevance"].mean(),
            "judgments_per_query": df.groupby("query").size().mean(),
            "judgments_per_document": df.groupby("doc_id").size().mean()
        }
    
    def export_to_trec_format(self, df: pd.DataFrame, output_file: str):
        """Export judgments to TREC format"""
        with open(output_file, 'w') as f:
            for _, row in df.iterrows():
                # TREC format: query_id Q0 doc_id relevance
                f.write(f"{row['query']} Q0 {row['doc_id']} {int(row['relevance'] * 4)}\n")
    
    def import_from_trec_format(self, input_file: str) -> pd.DataFrame:
        """Import judgments from TREC format"""
        records = []
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    query = parts[0]
                    doc_id = parts[2]
                    relevance = float(parts[3]) / 4.0  # Normalize to 0-1
                    
                    records.append({
                        "query": query,
                        "doc_id": doc_id,
                        "relevance": relevance
                    })
        
        return pd.DataFrame(records) 