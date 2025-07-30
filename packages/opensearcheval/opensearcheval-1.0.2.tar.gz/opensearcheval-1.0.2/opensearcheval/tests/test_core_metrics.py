import pytest
from opensearcheval.core.metrics import (
    mean_reciprocal_rank, precision_at_k, ndcg_at_k,
    click_through_rate, time_to_first_click, abandoned_search_rate
)

# Test data
query = "test query"
results = [
    {"doc_id": "doc1", "title": "Test Document 1", "snippet": "This is a test document"},
    {"doc_id": "doc2", "title": "Test Document 2", "snippet": "This is another test document"},
    {"doc_id": "doc3", "title": "Test Document 3", "snippet": "Yet another test document"},
    {"doc_id": "doc4", "title": "Test Document 4", "snippet": "Final test document"}
]
relevance_judgments = {
    "doc1": 3,  # Very relevant
    "doc2": 0,  # Not relevant
    "doc3": 2,  # Relevant
    "doc4": 1   # Somewhat relevant
}
user_interactions = [
    {"type": "search", "timestamp": 100, "query": query},
    {"type": "click", "timestamp": 105, "doc_id": "doc1", "position": 0},
    {"type": "click", "timestamp": 110, "doc_id": "doc3", "position": 2}
]

def test_mean_reciprocal_rank():
    # Test when first result is relevant
    mrr = mean_reciprocal_rank(query, results, relevance_judgments)
    assert mrr == 1.0
    
    # Test when first result is not relevant
    modified_judgments = relevance_judgments.copy()
    modified_judgments["doc1"] = 0
    modified_judgments["doc3"] = 3
    mrr = mean_reciprocal_rank(query, results, modified_judgments)
    assert mrr == 1.0 / 3  # Third document is relevant
    
    # Test when no results are relevant
    all_zero_judgments = {doc_id: 0 for doc_id in relevance_judgments}
    mrr = mean_reciprocal_rank(query, results, all_zero_judgments)
    assert mrr == 0.0

def test_precision_at_k():
    # Test precision@2
    p2 = precision_at_k(query, results, relevance_judgments, k=2)
    assert p2 == 0.5  # 1 out of 2 are relevant
    
    # Test precision@4
    p4 = precision_at_k(query, results, relevance_judgments, k=4)
    assert p4 == 0.75  # 3 out of 4 are relevant
    
    # Test with k > len(results)
    p6 = precision_at_k(query, results, relevance_judgments, k=6)
    assert p6 == 0.75  # Should still be 3 out of 4

def test_ndcg_at_k():
    # Test NDCG@4
    ndcg = ndcg_at_k(query, results, relevance_judgments, k=4)
    # The ideal ordering would be [3, 2, 1, 0] but actual is [3, 0, 2, 1]
    # This is not a perfect ordering, so NDCG < 1.0
    assert 0.0 < ndcg < 1.0
    
    # Test with perfect ordering
    perfect_results = [
        {"doc_id": "doc1", "title": "Test Document 1", "snippet": "This is a test document"},
        {"doc_id": "doc3", "title": "Test Document 3", "snippet": "Yet another test document"},
        {"doc_id": "doc4", "title": "Test Document 4", "snippet": "Final test document"},
        {"doc_id": "doc2", "title": "Test Document 2", "snippet": "This is another test document"}
    ]
    perfect_ndcg = ndcg_at_k(query, perfect_results, relevance_judgments, k=4)
    assert perfect_ndcg == 1.0

def test_click_through_rate():
    # 2 clicks out of 4 results
    ctr = click_through_rate(query, results, user_interactions)
    assert ctr == 0.5
    
    # Test with no clicks
    no_clicks = [i for i in user_interactions if i["type"] != "click"]
    ctr = click_through_rate(query, results, no_clicks)
    assert ctr == 0.0
    
    # Test with no results
    ctr = click_through_rate(query, [], user_interactions)
    assert ctr == 0.0

def test_time_to_first_click():
    # First click is at timestamp 105, search is at 100
    ttfc = time_to_first_click(query, results, user_interactions)
    assert ttfc == 5  # 105 - 100 = 5
    
    # Test with no clicks
    no_clicks = [i for i in user_interactions if i["type"] != "click"]
    ttfc = time_to_first_click(query, results, no_clicks)
    assert ttfc == 0.0
    
    # Test with no search event
    no_search = [i for i in user_interactions if i["type"] != "search"]
    ttfc = time_to_first_click(query, results, no_search)
    assert ttfc == 0.0

def test_abandoned_search_rate():
    # There are clicks, so not abandoned
    asr = abandoned_search_rate(query, results, user_interactions)
    assert asr == 0.0
    
    # Test with no clicks (abandoned)
    no_clicks = [i for i in user_interactions if i["type"] != "click"]
    asr = abandoned_search_rate(query, results, no_clicks)
    assert asr == 1.0
    
    # Test with no interactions
    asr = abandoned_search_rate(query, results, [])
    assert asr == 1.0