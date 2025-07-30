from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.metrics import ndcg_score

def mean_reciprocal_rank(query: str, results: List[Dict[str, Any]], 
                         relevance_judgments: Dict[str, int]) -> float:
    """
    Calculate Mean Reciprocal Rank (MRR) for search results
    
    Args:
        query: The search query
        results: List of search results with doc_id fields
        relevance_judgments: Dictionary mapping doc_id to relevance score
        
    Returns:
        MRR score
    """
    for i, result in enumerate(results, 1):
        doc_id = result.get("doc_id")
        if doc_id in relevance_judgments and relevance_judgments[doc_id] > 0:
            return 1.0 / i
    return 0.0

def precision_at_k(query: str, results: List[Dict[str, Any]], 
                   relevance_judgments: Dict[str, int], k: int = 10) -> float:
    """
    Calculate Precision@K for search results
    
    Args:
        query: The search query
        results: List of search results with doc_id fields
        relevance_judgments: Dictionary mapping doc_id to relevance score
        k: The position to calculate precision at
        
    Returns:
        Precision@K score
    """
    if not results or k <= 0:
        return 0.0
    
    k = min(k, len(results))
    relevant_count = sum(1 for r in results[:k] 
                         if r.get("doc_id") in relevance_judgments 
                         and relevance_judgments[r.get("doc_id")] > 0)
    
    return relevant_count / k

def ndcg_at_k(query: str, results: List[Dict[str, Any]], 
              relevance_judgments: Dict[str, int], k: int = 10) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain at K (NDCG@K)
    
    Args:
        query: The search query
        results: List of search results with doc_id fields
        relevance_judgments: Dictionary mapping doc_id to relevance score
        k: The position to calculate NDCG at
        
    Returns:
        NDCG@K score
    """
    if not results or k <= 0:
        return 0.0
    
    k = min(k, len(results))
    
    # Get relevance scores for each result
    relevance = [relevance_judgments.get(r.get("doc_id"), 0) for r in results[:k]]
    
    # Ideal ordering would be relevance scores sorted in descending order
    ideal_relevance = sorted(relevance, reverse=True)
    
    # Convert to numpy arrays for ndcg_score function
    y_true = np.array([ideal_relevance])
    y_score = np.array([relevance])
    
    return ndcg_score(y_true, y_score, k=k)

def click_through_rate(query: str, results: List[Dict[str, Any]], 
                       user_interactions: List[Dict[str, Any]]) -> float:
    """
    Calculate Click-Through Rate (CTR) for search results
    
    Args:
        query: The search query
        results: List of search results
        user_interactions: List of user interaction events
        
    Returns:
        CTR score
    """
    if not results or not user_interactions:
        return 0.0
    
    # Count clicks on search results
    result_ids = [r.get("doc_id") for r in results]
    clicks = sum(1 for interaction in user_interactions 
                if interaction.get("type") == "click" 
                and interaction.get("doc_id") in result_ids)
    
    # Number of impressions is the number of results shown
    impressions = len(results)
    
    return clicks / impressions if impressions > 0 else 0.0

def time_to_first_click(query: str, results: List[Dict[str, Any]], 
                        user_interactions: List[Dict[str, Any]]) -> float:
    """
    Calculate average time to first click
    
    Args:
        query: The search query
        results: List of search results
        user_interactions: List of user interaction events with timestamps
        
    Returns:
        Average time to first click in seconds
    """
    if not results or not user_interactions:
        return 0.0
    
    # Find search start time
    search_time = next((i.get("timestamp") for i in user_interactions 
                        if i.get("type") == "search" and i.get("query") == query), None)
    
    if not search_time:
        return 0.0
    
    # Find first click time
    click_events = [i for i in user_interactions if i.get("type") == "click"]
    if not click_events:
        return 0.0
    
    first_click_time = min(i.get("timestamp") for i in click_events)
    
    # Calculate time difference
    return first_click_time - search_time

def abandoned_search_rate(query: str, results: List[Dict[str, Any]], 
                          user_interactions: List[Dict[str, Any]]) -> float:
    """
    Calculate the rate of abandoned searches (no clicks after results shown)
    
    Args:
        query: The search query
        results: List of search results
        user_interactions: List of user interaction events
        
    Returns:
        Abandoned search rate (0.0 to 1.0)
    """
    if not results or not user_interactions:
        return 1.0  # No interactions means 100% abandonment
    
    # Check if there are any clicks after the search
    has_clicks = any(i.get("type") == "click" for i in user_interactions)
    
    # If no clicks, the search was abandoned
    return 0.0 if has_clicks else 1.0

def llm_judge_score(query: str, results: List[Dict[str, Any]], 
                    llm_judgments: Dict[str, float]) -> float:
    """
    Get the LLM judge score for search results
    
    Args:
        query: The search query
        results: List of search results with doc_id fields
        llm_judgments: Dictionary mapping doc_id to LLM relevance score
        
    Returns:
        Average LLM judgment score for the results
    """
    if not results or not llm_judgments:
        return 0.0
    
    # Get LLM scores for each result
    scores = [llm_judgments.get(r.get("doc_id"), 0) for r in results]
    
    # Return average score
    return sum(scores) / len(scores) if scores else 0.0

def average_dwell_time(query: str, results: List[Dict[str, Any]], 
                      user_interactions: List[Dict[str, Any]]) -> float:
    """
    Calculate average dwell time on clicked results
    
    Args:
        query: The search query
        results: List of search results
        user_interactions: List of user interaction events with dwell times
        
    Returns:
        Average dwell time in seconds
    """
    if not results or not user_interactions:
        return 0.0
    
    # Find click events with dwell times
    click_events = [
        i for i in user_interactions 
        if i.get("type") == "click" and i.get("dwell_time") is not None
    ]
    
    if not click_events:
        return 0.0
    
    # Calculate average dwell time
    dwell_times = [i.get("dwell_time", 0) for i in click_events]
    return sum(dwell_times) / len(dwell_times)

def first_result_click_rate(query: str, results: List[Dict[str, Any]], 
                           user_interactions: List[Dict[str, Any]]) -> float:
    """
    Calculate the rate of clicks on the first search result
    
    Args:
        query: The search query
        results: List of search results
        user_interactions: List of user interaction events
        
    Returns:
        First result click rate (0.0 to 1.0)
    """
    if not results or not user_interactions:
        return 0.0
    
    # Check if there are any searches
    search_events = [i for i in user_interactions if i.get("type") == "search"]
    if not search_events:
        return 0.0
    
    # Count searches and first result clicks
    num_searches = len(search_events)
    
    first_result_clicks = [
        i for i in user_interactions
        if i.get("type") == "click" and i.get("position") == 0
    ]
    
    num_first_clicks = len(first_result_clicks)
    
    return num_first_clicks / num_searches if num_searches > 0 else 0.0

def reciprocal_rank_fusion(query: str, results_lists: List[List[Dict[str, Any]]], 
                          k: int = 60) -> List[Dict[str, Any]]:
    """
    Combine multiple result lists using Reciprocal Rank Fusion
    
    Args:
        query: The search query
        results_lists: List of result lists to combine
        k: Constant in RRF formula (default: 60)
        
    Returns:
        Combined and reranked list of results
    """
    if not results_lists:
        return []
    
    # Calculate RRF scores
    doc_scores = {}
    
    for results in results_lists:
        for rank, result in enumerate(results, 1):
            doc_id = result.get("doc_id")
            if not doc_id:
                continue
            
            # RRF formula: 1 / (k + rank)
            score = 1.0 / (k + rank)
            
            if doc_id in doc_scores:
                doc_scores[doc_id]["score"] += score
            else:
                doc_scores[doc_id] = {
                    "doc_id": doc_id,
                    "score": score,
                    "result": result
                }
    
    # Sort by score in descending order
    sorted_docs = sorted(doc_scores.values(), key=lambda x: x["score"], reverse=True)
    
    # Return the reranked results
    return [doc["result"] for doc in sorted_docs]

def diversity_metric(query: str, results: List[Dict[str, Any]], 
                    categories: Dict[str, str]) -> float:
    """
    Calculate diversity of search results based on categories
    
    Args:
        query: The search query
        results: List of search results with doc_id fields
        categories: Dictionary mapping doc_id to category
        
    Returns:
        Diversity score (0.0 to 1.0)
    """
    if not results:
        return 0.0
    
    # Count unique categories
    result_categories = set()
    for result in results:
        doc_id = result.get("doc_id")
        if doc_id in categories:
            result_categories.add(categories[doc_id])
    
    # Calculate diversity as ratio of unique categories to results
    return len(result_categories) / len(results)

def satisfaction_score(query: str, results: List[Dict[str, Any]], 
                      user_interactions: List[Dict[str, Any]], 
                      satisfaction_threshold: float = 30.0) -> float:
    """
    Calculate user satisfaction based on dwell time and interaction patterns
    
    Args:
        query: The search query
        results: List of search results
        user_interactions: List of user interaction events
        satisfaction_threshold: Dwell time threshold for satisfaction (seconds)
        
    Returns:
        Satisfaction score (0.0 to 1.0)
    """
    if not results or not user_interactions:
        return 0.0
    
    # Count clicks with long dwell time
    satisfied_clicks = 0
    total_clicks = 0
    
    for interaction in user_interactions:
        if interaction.get("type") == "click":
            total_clicks += 1
            dwell_time = interaction.get("dwell_time", 0)
            
            if dwell_time >= satisfaction_threshold:
                satisfied_clicks += 1
    
    # If no clicks, check if search was abandoned
    if total_clicks == 0:
        return 0.0
    
    return satisfied_clicks / total_clicks

def normalized_discounted_cumulative_gain(rankings: List[float], k: int = None) -> float:
    """
    Calculate NDCG for a single ranking
    
    Args:
        rankings: List of relevance scores
        k: Number of results to consider (default: all)
        
    Returns:
        NDCG score
    """
    if not rankings:
        return 0.0
    
    # If k is not specified, use all rankings
    if k is None:
        k = len(rankings)
    else:
        k = min(k, len(rankings))
    
    rankings = rankings[:k]
    
    # Calculate DCG
    dcg = rankings[0] + sum(
        r / np.log2(i + 1) for i, r in enumerate(rankings[1:], 2)
    )
    
    # Calculate ideal DCG (sorted rankings)
    ideal_rankings = sorted(rankings, reverse=True)
    idcg = ideal_rankings[0] + sum(
        r / np.log2(i + 1) for i, r in enumerate(ideal_rankings[1:], 2)
    )
    
    # Return NDCG
    return dcg / idcg if idcg > 0 else 0.0