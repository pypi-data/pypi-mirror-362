from typing import Dict, List, Any, Optional
import logging
import json
import asyncio
import httpx
from pydantic import BaseModel

from opensearcheval.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class LLMJudge:
    """LLM-as-a-judge system for evaluating search results"""
    
    def __init__(self, model_name: str, config: Dict[str, Any]):
        self.model_name = model_name
        self.config = config
        self.endpoint = config.get("endpoint", "https://api.openai.com/v1/chat/completions")
        self.api_key = config.get("api_key", "")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 1024)
        logger.info(f"Initialized LLM Judge with model: {model_name}")
    
    async def evaluate(self, query: str, document: Dict[str, Any], 
                      criteria: List[str]) -> Dict[str, Any]:
        """
        Evaluate a single document against a query using the LLM
        
        Args:
            query: The search query
            document: The document to evaluate (with title, content, etc.)
            criteria: List of evaluation criteria
            
        Returns:
            Evaluation results
        """
        # Construct prompt for LLM
        prompt = self._construct_evaluation_prompt(query, document, criteria)
        
        try:
            # Call LLM API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.endpoint,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    json={
                        "model": self.model_name,
                        "messages": [
                            {"role": "system", "content": "You are an expert search quality evaluator."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                        "response_format": {"type": "json_object"}
                    },
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.error(f"LLM API error: {response.status_code} - {response.text}")
                    return {
                        "error": f"API error: {response.status_code}",
                        "scores": {c: 0.0 for c in criteria},
                        "overall_score": 0.0,
                        "explanation": "Failed to get evaluation from LLM"
                    }
                
                result = response.json()
                llm_response = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
                
                # Parse LLM response
                try:
                    evaluation = json.loads(llm_response)
                    return evaluation
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse LLM response as JSON: {llm_response}")
                    return {
                        "error": "Failed to parse LLM response",
                        "scores": {c: 0.0 for c in criteria},
                        "overall_score": 0.0,
                        "explanation": "Invalid response format"
                    }
                    
        except Exception as e:
            logger.error(f"Error evaluating with LLM: {str(e)}")
            return {
                "error": str(e),
                "scores": {c: 0.0 for c in criteria},
                "overall_score": 0.0,
                "explanation": f"Exception: {str(e)}"
            }
    
    def _construct_evaluation_prompt(self, query: str, document: Dict[str, Any], 
                                    criteria: List[str]) -> str:
        """Construct a prompt for the LLM to evaluate a document"""
        criteria_str = ", ".join(criteria)
        
        prompt = f"""
        Evaluate the following search result for the query:
        
        QUERY: {query}
        
        SEARCH RESULT:
        Title: {document.get('title', 'N/A')}
        Snippet: {document.get('snippet', 'N/A')}
        URL: {document.get('url', 'N/A')}
        
        Please evaluate this result based on the following criteria: {criteria_str}
        
        For each criterion, assign a score from 0.0 to 5.0, where:
        - 0.0-1.0: Poor - Does not satisfy the criterion at all
        - 1.0-2.0: Fair - Minimally satisfies the criterion
        - 2.0-3.0: Good - Adequately satisfies the criterion
        - 3.0-4.0: Very Good - Strongly satisfies the criterion
        - 4.0-5.0: Excellent - Perfectly satisfies the criterion
        
        Also provide an overall score and a detailed explanation of your evaluation.
        
        Respond in the following JSON format:
        {{
            "scores": {{
                "criterion1": score1,
                "criterion2": score2,
                ...
            }},
            "overall_score": overall_score,
            "explanation": "your detailed explanation"
        }}
        """
        
        return prompt


async def evaluate_search_results(query: str, documents: List[Dict[str, Any]], 
                                 criteria: List[str]) -> List[Dict[str, Any]]:
    """
    Evaluate a set of search results using the LLM judge
    
    Args:
        query: Search query
        documents: List of documents to evaluate
        criteria: Evaluation criteria
        
    Returns:
        List of evaluation results
    """
    # Initialize LLM judge
    judge = LLMJudge(
        model_name=settings.LLM_MODEL,
        config={
            "temperature": 0.1,
            "max_tokens": 1024,
            "endpoint": settings.LLM_ENDPOINT,
            "api_key": settings.LLM_API_KEY
        }
    )
    
    # Evaluate each document in parallel
    tasks = []
    for doc in documents:
        task = judge.evaluate(query, doc, criteria)
        tasks.append(task)
    
    # Wait for all evaluations to complete
    results = await asyncio.gather(*tasks)
    
    # Attach document IDs to results
    for i, result in enumerate(results):
        result["doc_id"] = documents[i].get("doc_id", f"doc_{i}")
    
    return results