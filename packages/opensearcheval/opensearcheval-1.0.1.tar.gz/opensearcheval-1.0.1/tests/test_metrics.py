import unittest
import numpy as np
from opensearcheval.core.metrics import (
    mean_reciprocal_rank, precision_at_k, ndcg_at_k, click_through_rate,
    time_to_first_click, abandoned_search_rate, diversity_metric,
    reciprocal_rank_fusion, normalized_discounted_cumulative_gain
)

class TestMetrics(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing
        self.query = "test query"
        
        self.results = [
            {"doc_id": "doc1", "title": "Test Document 1", "snippet": "This is a test document"},
            {"doc_id": "doc2", "title": "Test Document 2", "snippet": "This is another test document"},
            {"doc_id": "doc3", "title": "Test Document 3", "snippet": "This is a third test document"},
            {"doc_id": "doc4", "title": "Test Document 4", "snippet": "This is a fourth test document"},
            {"doc_id": "doc5", "title": "Test Document 5", "snippet": "This is a fifth test document"}
        ]
        
        self.relevance_judgments = {
            "doc1": 3,
            "doc3": 2,
            "doc4": 1,
            "doc6": 3  # Not in results
        }
        
        self.user_interactions = [
            {"type": "search", "query": "test query", "timestamp": 1000.0},
            {"type": "click", "doc_id": "doc1", "position": 0, "timestamp": 1005.0, "dwell_time": 15.0},
            {"type": "click", "doc_id": "doc3", "position": 2, "timestamp": 1020.0, "dwell_time": 30.0}
        ]
        
        self.categories = {
            "doc1": "category1",
            "doc2": "category2",
            "doc3": "category1",
            "doc4": "category3",
            "doc5": "category2"
        }
    
    def test_mean_reciprocal_rank(self):
        # Test when first relevant document is at position 1
        mrr = mean_reciprocal_rank(self.query, self.results, self.relevance_judgments)
        self.assertEqual(mrr, 1.0)
        
        # Test when no relevant documents are found
        irrelevant_results = [
            {"doc_id": "doc10", "title": "Irrelevant", "snippet": "This is irrelevant"}
        ]
        mrr = mean_reciprocal_rank(self.query, irrelevant_results, self.relevance_judgments)
        self.assertEqual(mrr, 0.0)
    
    def test_precision_at_k(self):
        # Test precision@3
        p3 = precision_at_k(self.query, self.results, self.relevance_judgments, k=3)
        # In the first 3 results, 2 are relevant (doc1, doc3)
        self.assertEqual(p3, 2/3)
        
        # Test precision@5
        p5 = precision_at_k(self.query, self.results, self.relevance_judgments, k=5)
        # In all 5 results, 3 are relevant (doc1, doc3, doc4)
        self.assertEqual(p5, 3/5)
        
        # Test with k > number of results
        pk = precision_at_k(self.query, self.results, self.relevance_judgments, k=10)
        self.assertEqual(pk, 3/5)  # Should use min(k, len(results))
    
    def test_ndcg_at_k(self):
        # Test NDCG@3
        ndcg3 = ndcg_at_k(self.query, self.results, self.relevance_judgments, k=3)
        self.assertGreater(ndcg3, 0.0)
        self.assertLessEqual(ndcg3, 1.0)
        
        # Test with empty results
        ndcg = ndcg_at_k(self.query, [], self.relevance_judgments, k=3)
        self.assertEqual(ndcg, 0.0)
    
    def test_click_through_rate(self):
        # Test CTR calculation
        ctr = click_through_rate(self.query, self.results, self.user_interactions)
        # 2 clicks on 5 results
        self.assertEqual(ctr, 2/5)
        
        # Test with no interactions
        ctr = click_through_rate(self.query, self.results, [])
        self.assertEqual(ctr, 0.0)
    
    def test_time_to_first_click(self):
        # Test time to first click
        ttfc = time_to_first_click(self.query, self.results, self.user_interactions)
        # First click at 1005, search at 1000
        self.assertEqual(ttfc, 5.0)
        
        # Test with no clicks
        ttfc = time_to_first_click(self.query, self.results, [
            {"type": "search", "query": "test query", "timestamp": 1000.0}
        ])
        self.assertEqual(ttfc, 0.0)
    
    def test_abandoned_search_rate(self):
        # Test with clicks (not abandoned)
        asr = abandoned_search_rate(self.query, self.results, self.user_interactions)
        self.assertEqual(asr, 0.0)
        
        # Test with no clicks (abandoned)
        asr = abandoned_search_rate(self.query, self.results, [
            {"type": "search", "query": "test query", "timestamp": 1000.0}
        ])
        self.assertEqual(asr, 1.0)
    
    def test_diversity_metric(self):
        # Test diversity calculation
        diversity = diversity_metric(self.query, self.results, self.categories)
        # 3 unique categories in 5 results
        self.assertEqual(diversity, 3/5)
        
        # Test with empty results
        diversity = diversity_metric(self.query, [], self.categories)
        self.assertEqual(diversity, 0.0)
    
    def test_reciprocal_rank_fusion(self):
        # Test RRF with multiple result lists
        results_list1 = [
            {"doc_id": "doc1", "title": "Test 1"},
            {"doc_id": "doc2", "title": "Test 2"},
            {"doc_id": "doc3", "title": "Test 3"}
        ]
        
        results_list2 = [
            {"doc_id": "doc3", "title": "Test 3"},
            {"doc_id": "doc1", "title": "Test 1"},
            {"doc_id": "doc4", "title": "Test 4"}
        ]
        
        fused_results = reciprocal_rank_fusion(self.query, [results_list1, results_list2])
        
        # Check length
        self.assertEqual(len(fused_results), 4)  # Unique documents from both lists
        
        # Check first result (should be doc1 or doc3 as they appear in both lists)
        self.assertIn(fused_results[0]["doc_id"], ["doc1", "doc3"])
        
        # Test with empty list
        fused_results = reciprocal_rank_fusion(self.query, [])
        self.assertEqual(fused_results, [])
    
    def test_normalized_discounted_cumulative_gain(self):
        # Test with sample rankings
        rankings = [3, 2, 3, 0, 1, 2]
        ndcg = normalized_discounted_cumulative_gain(rankings)
        self.assertGreater(ndcg, 0.0)
        self.assertLessEqual(ndcg, 1.0)
        
        # Test with perfect ranking
        ndcg = normalized_discounted_cumulative_gain([3, 3, 2, 2, 1, 0])
        self.assertEqual(ndcg, 1.0)
        
        # Test with empty rankings
        ndcg = normalized_discounted_cumulative_gain([])
        self.assertEqual(ndcg, 0.0)
        
        # Test with k parameter
        ndcg = normalized_discounted_cumulative_gain(rankings, k=3)
        self.assertGreater(ndcg, 0.0)
        self.assertLessEqual(ndcg, 1.0)

if __name__ == '__main__':
    unittest.main()