import argparse
import json
import logging
import os
import sys
import asyncio
import httpx
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime

from opensearcheval.core.config import get_settings
from opensearcheval.utils.visualization import (
    metrics_time_series, ab_test_results_plot, user_behavior_heatmap,
    metric_comparison_radar, save_figure
)
from opensearcheval.data.connectors.sql import SQLConnector
from opensearcheval.data.connectors.spark import SparkConnector
from opensearcheval.ml.embeddings import create_embedding_model

# Get settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# API base URL
API_BASE_URL = f"http://{settings.API_HOST}:{settings.API_PORT}"

async def make_api_request(endpoint: str, method: str = "get", data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make a request to the API
    
    Args:
        endpoint: API endpoint
        method: HTTP method
        data: Optional data for POST/PUT requests
        
    Returns:
        Response data
    """
    url = f"{API_BASE_URL}/{endpoint}"
    
    async with httpx.AsyncClient() as client:
        if method.lower() == "get":
            response = await client.get(url)
        elif method.lower() == "post":
            response = await client.post(url, json=data)
        elif method.lower() == "put":
            response = await client.put(url, json=data)
        elif method.lower() == "delete":
            response = await client.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code >= 400:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        return response.json()

def evaluate_command(args):
    """Handle 'evaluate' command"""
    # Load search data from JSON file
    with open(args.input_file, 'r') as f:
        search_data = json.load(f)
    
    # Add evaluation ID if not present
    if "id" not in search_data:
        search_data["id"] = f"eval_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Make API request
    response = asyncio.run(make_api_request(
        "api/v1/evaluate", 
        method="post", 
        data=search_data
    ))
    
    # Print initial response
    print(f"Evaluation submitted with ID: {response['id']}")
    print(f"Initial metrics: {json.dumps(response['metrics'], indent=2)}")
    
    # Poll for complete results if requested
    if args.wait:
        print("Waiting for complete results...")
        complete = False
        max_attempts = 10
        attempt = 0
        
        while not complete and attempt < max_attempts:
            try:
                complete_response = asyncio.run(make_api_request(
                    f"api/v1/evaluation-results/{response['id']}"
                ))
                
                if complete_response.get("status") == "complete":
                    complete = True
                    print("\nComplete evaluation results:")
                    print(json.dumps(complete_response['metrics'], indent=2))
                    
                    # Save results if output file specified
                    if args.output_file:
                        with open(args.output_file, 'w') as f:
                            json.dump(complete_response, f, indent=2)
                        print(f"Results saved to {args.output_file}")
                else:
                    print(".", end="", flush=True)
                    asyncio.run(asyncio.sleep(1))
            except Exception as e:
                print(f"\nError polling for results: {str(e)}")
                break
            
            attempt += 1
        
        if not complete:
            print("\nTimeout waiting for complete results. Try retrieving them later with:")
            print(f"opensearcheval results {response['id']}")

def experiment_command(args):
    """Handle 'experiment' command"""
    if args.action == "create":
        # Create experiment
        experiment_data = {
            "name": args.name,
            "description": args.description or "",
            "experiment_type": args.type or "A_B",
            "metrics": args.metrics.split(",") if args.metrics else ["mean_reciprocal_rank", "click_through_rate"]
        }
        
        # Add traffic split if provided
        if args.traffic_split:
            splits = {}
            for item in args.traffic_split.split(","):
                key, value = item.split(":")
                splits[key] = float(value)
            experiment_data["traffic_split"] = splits
        
        # Create the experiment
        response = asyncio.run(make_api_request(
            "api/v1/experiments", 
            method="post", 
            data=experiment_data
        ))
        
        print(f"Experiment created with ID: {response['id']}")
        print(json.dumps(response, indent=2))
    
    elif args.action == "list":
        # List experiments
        response = asyncio.run(make_api_request("api/v1/experiments"))
        
        if not response:
            print("No experiments found")
            return
        
        # Print table
        df = pd.DataFrame(response)
        print(df[["id", "name", "status", "created_at"]].to_string(index=False))
    
    elif args.action == "view":
        # View experiment details
        if not args.id:
            print("Error: Experiment ID is required")
            return
        
        response = asyncio.run(make_api_request(f"api/v1/experiments/{args.id}"))
        print(json.dumps(response, indent=2))
    
    elif args.action == "start":
        # Start experiment
        if not args.id:
            print("Error: Experiment ID is required")
            return
        
        response = asyncio.run(make_api_request(
            f"api/v1/experiments/{args.id}/start", 
            method="post"
        ))
        
        print(f"Experiment {args.id} started")
        print(f"Status: {response['status']}")
    
    elif args.action == "stop":
        # Stop experiment
        if not args.id:
            print("Error: Experiment ID is required")
            return
        
        response = asyncio.run(make_api_request(
            f"api/v1/experiments/{args.id}/complete", 
            method="post"
        ))
        
        print(f"Experiment {args.id} stopped")
        print(f"Status: {response['status']}")
    
    elif args.action == "analyze":
        # Submit analysis data
        if not args.input_file:
            print("Error: Input file is required")
            return
        
        with open(args.input_file, 'r') as f:
            analysis_data = json.load(f)
        
        response = asyncio.run(make_api_request(
            "api/v1/analyze-ab-test", 
            method="post", 
            data=analysis_data
        ))
        
        print(f"Analysis submitted for experiment: {response['experiment_id']}")
        print(f"Status: {response['status']}")
        
        # Wait for results if requested
        if args.wait:
            print("Waiting for analysis results...")
            complete = False
            max_attempts = 10
            attempt = 0
            
            while not complete and attempt < max_attempts:
                try:
                    complete_response = asyncio.run(make_api_request(
                        f"api/v1/ab-test-results/{response['experiment_id']}"
                    ))
                    
                    if complete_response.get("status") == "complete":
                        complete = True
                        print("\nAnalysis results:")
                        print(json.dumps(complete_response['results'], indent=2))
                        
                        # Save results if output file specified
                        if args.output_file:
                            with open(args.output_file, 'w') as f:
                                json.dump(complete_response, f, indent=2)
                            print(f"Results saved to {args.output_file}")
                    else:
                        print(".", end="", flush=True)
                        asyncio.run(asyncio.sleep(1))
                except Exception as e:
                    print(f"\nError polling for results: {str(e)}")
                    break
                
                attempt += 1
            
            if not complete:
                print("\nTimeout waiting for analysis results. Try retrieving them later.")

def llm_judge_command(args):
    """Handle 'llm-judge' command"""
    # Load documents from file
    with open(args.input_file, 'r') as f:
        data = json.load(f)
    
    query = data.get("query", "")
    documents = data.get("documents", [])
    criteria = data.get("criteria", ["relevance", "factuality", "completeness"])
    
    if not query or not documents:
        print("Error: Input file must contain 'query' and 'documents' fields")
        return
    
    # Make API request
    response = asyncio.run(make_api_request(
        "api/v1/llm-judge", 
        method="post", 
        data={
            "query": query,
            "documents": documents,
            "evaluation_criteria": criteria
        }
    ))
    
    # Print results
    print(f"Query: {response['query']}")
    print(f"Average Score: {response['average_score']:.2f}")
    print("\nDocument Judgments:")
    
    for i, judgment in enumerate(response['judgments']):
        print(f"\nDocument {i+1}:")
        print(f"  Overall Score: {judgment.get('overall_score', 0):.2f}")
        print("  Scores:")
        
        for criterion, score in judgment.get('scores', {}).items():
            print(f"    {criterion}: {score:.2f}")
        
        print(f"  Explanation: {judgment.get('explanation', 'No explanation provided')}")
    
    # Save results if requested
    if args.output_file:
        with open(args.output_file, 'w') as f:
            json.dump(response, f, indent=2)
        print(f"\nResults saved to {args.output_file}")

def data_command(args):
    """Handle 'data' command"""
    if args.action == "import":
        if args.type == "sql":
            # Import data from SQL
            if not args.connection_string:
                print("Error: Connection string is required for SQL import")
                return
            
            try:
                connector = SQLConnector(args.connection_string)
                
                if args.query:
                    # Execute custom query
                    df = connector.execute_query(args.query)
                elif args.table:
                    # Query a specific table
                    df = connector.execute_query(f"SELECT * FROM {args.table}")
                else:
                    print("Error: Either --query or --table is required")
                    return
                
                # Save the data
                if args.output_file.endswith(".csv"):
                    df.to_csv(args.output_file, index=False)
                elif args.output_file.endswith(".json"):
                    df.to_json(args.output_file, orient="records")
                elif args.output_file.endswith(".parquet"):
                    df.to_parquet(args.output_file, index=False)
                else:
                    df.to_csv(args.output_file, index=False)
                
                print(f"Imported {len(df)} rows to {args.output_file}")
            except Exception as e:
                print(f"Error importing data: {str(e)}")
        
        elif args.type == "spark":
            # Import data using Spark
            try:
                connector = SparkConnector()
                
                if not args.input_file:
                    print("Error: Input file is required for Spark import")
                    return
                
                # Load the data
                format_type = args.format or "parquet"
                df = connector.load_data(args.input_file, format=format_type)
                
                # Save the data
                if args.output_file.endswith(".csv"):
                    df.to_csv(args.output_file, index=False)
                elif args.output_file.endswith(".json"):
                    df.to_json(args.output_file, orient="records")
                elif args.output_file.endswith(".parquet"):
                    df.to_parquet(args.output_file, index=False)
                else:
                    df.to_csv(args.output_file, index=False)
                
                print(f"Imported {len(df)} rows to {args.output_file}")
                
                # Close Spark session
                connector.close()
            except Exception as e:
                print(f"Error importing data with Spark: {str(e)}")
    
    elif args.action == "process":
        # Process search logs
        if not args.input_file:
            print("Error: Input file is required")
            return
        
        if not args.output_file:
            print("Error: Output file is required")
            return
        
        try:
            # Load data
            if args.input_file.endswith(".csv"):
                df = pd.read_csv(args.input_file)
            elif args.input_file.endswith(".json"):
                df = pd.read_json(args.input_file)
            elif args.input_file.endswith(".parquet"):
                df = pd.read_parquet(args.input_file)
            else:
                print("Error: Unsupported file format")
                return
            
            # Basic processing
            print(f"Processing {len(df)} rows of data...")
            
            if "search_logs" in args.type:
                # Process search logs
                if "query" in df.columns and "timestamp" in df.columns:
                    # Group by query and date
                    result = df.groupby([
                        pd.to_datetime(df["timestamp"]).dt.date,
                        df["query"]
                    ]).agg({
                        "user_id": "nunique",
                        "session_id": "count"
                    }).reset_index()
                    
                    result.columns = ["date", "query", "unique_users", "search_count"]
                    
                    # Save processed data
                    if args.output_file.endswith(".csv"):
                        result.to_csv(args.output_file, index=False)
                    elif args.output_file.endswith(".json"):
                        result.to_json(args.output_file, orient="records")
                    elif args.output_file.endswith(".parquet"):
                        result.to_parquet(args.output_file, index=False)
                    else:
                        result.to_csv(args.output_file, index=False)
                    
                    print(f"Processed search logs: {len(result)} rows saved to {args.output_file}")
                else:
                    print("Error: Input file must contain 'query' and 'timestamp' columns")
            
            elif "click_logs" in args.type:
                # Process click logs
                if "query_id" in df.columns and "doc_id" in df.columns:
                    # Calculate CTR by position
                    if "position" in df.columns:
                        position_ctr = df.groupby("position").agg({
                            "doc_id": "count"
                        }).reset_index()
                        
                        position_ctr.columns = ["position", "clicks"]
                        total_positions = pd.DataFrame({
                            "position": range(max(position_ctr["position"]) + 1)
                        })
                        
                        position_ctr = total_positions.merge(
                            position_ctr, on="position", how="left"
                        ).fillna(0)
                        
                        position_ctr["impression_count"] = len(df["query_id"].unique())
                        position_ctr["ctr"] = position_ctr["clicks"] / position_ctr["impression_count"]
                        
                        # Save processed data
                        if args.output_file.endswith(".csv"):
                            position_ctr.to_csv(args.output_file, index=False)
                        elif args.output_file.endswith(".json"):
                            position_ctr.to_json(args.output_file, orient="records")
                        elif args.output_file.endswith(".parquet"):
                            position_ctr.to_parquet(args.output_file, index=False)
                        else:
                            position_ctr.to_csv(args.output_file, index=False)
                        
                        print(f"Processed click logs: {len(position_ctr)} rows saved to {args.output_file}")
                    else:
                        print("Error: Input file must contain 'position' column for click log processing")
                else:
                    print("Error: Input file must contain 'query_id' and 'doc_id' columns")
            
            else:
                print("Error: Unsupported processing type")
        
        except Exception as e:
            print(f"Error processing data: {str(e)}")

def embedding_command(args):
    """Handle 'embedding' command"""
    if args.action == "generate":
        # Create embedding model
        try:
            # Load configuration
            if args.config_file:
                with open(args.config_file, 'r') as f:
                    config = json.load(f)
            else:
                # Use default configuration
                config = {
                    "type": "api",
                    "model_name": "text-embedding-ada-002",
                    "api_key": os.environ.get("OPENAI_API_KEY", ""),
                    "api_url": "https://api.openai.com/v1/embeddings",
                    "dimension": 1536
                }
            
            # Create model
            model = create_embedding_model(config)
            
            # Load texts
            with open(args.input_file, 'r') as f:
                if args.input_file.endswith(".json"):
                    data = json.load(f)
                    
                    if isinstance(data, list):
                        if all(isinstance(item, str) for item in data):
                            texts = data
                        elif all(isinstance(item, dict) for item in data):
                            # Extract text from a specific field
                            field = args.field or "text"
                            texts = [item.get(field, "") for item in data]
                        else:
                            print("Error: Unsupported JSON format")
                            return
                    elif isinstance(data, dict):
                        field = args.field or "text"
                        if field in data:
                            texts = [data[field]]
                        else:
                            print(f"Error: Field '{field}' not found in JSON")
                            return
                    else:
                        print("Error: Unsupported JSON format")
                        return
                else:
                    # Assume text file with one text per line
                    texts = [line.strip() for line in f if line.strip()]
            
            # Generate embeddings
            print(f"Generating embeddings for {len(texts)} texts...")
            embeddings = model.embed(texts)
            
            # Save embeddings
            output_data = []
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                output_data.append({
                    "id": i,
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "embedding": embedding.tolist()
                })
            
            with open(args.output_file, 'w') as f:
                json.dump(output_data, f)
            
            print(f"Saved {len(output_data)} embeddings to {args.output_file}")
        
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
    
    elif args.action == "similarity":
        # Calculate similarity between embeddings
        try:
            # Load embeddings
            with open(args.input_file, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list) or not all("embedding" in item for item in data):
                print("Error: Input file must contain a list of objects with 'embedding' field")
                return
            
            # Convert embeddings to numpy arrays
            embeddings = [np.array(item["embedding"]) for item in data]
            
            # Calculate similarities
            if args.query_index is not None:
                # Similarity to a specific query
                query_idx = int(args.query_index)
                if query_idx < 0 or query_idx >= len(embeddings):
                    print(f"Error: Query index {query_idx} out of range")
                    return
                
                query_embedding = embeddings[query_idx]
                query_text = data[query_idx].get("text", f"Item {query_idx}")
                
                # Create embedding model just for similarity calculation
                model = EmbeddingModel("similarity_model", len(query_embedding))
                
                # Calculate similarities
                similarities = []
                for i, embedding in enumerate(embeddings):
                    if i == query_idx:
                        continue
                    
                    similarity = model.similarity(query_embedding, embedding)
                    similarities.append({
                        "index": i,
                        "text": data[i].get("text", f"Item {i}"),
                        "similarity": similarity
                    })
                
                # Sort by similarity
                similarities.sort(key=lambda x: x["similarity"], reverse=True)
                
                # Print results
                print(f"Similarities to: {query_text}")
                for i, item in enumerate(similarities[:10]):
                    print(f"{i+1}. [{item['index']}] {item['text']} - {item['similarity']:.4f}")