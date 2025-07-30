import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import os

logger = logging.getLogger(__name__)

class SparkConnector:
    """Connector for Apache Spark"""
    
    def __init__(self, spark_session=None):
        """
        Initialize the Spark connector
        
        Args:
            spark_session: Optional existing Spark session
        """
        if spark_session:
            self.spark = spark_session
            logger.info("Using provided Spark session")
        else:
            try:
                # Import Spark and create session if not provided
                from pyspark.sql import SparkSession
                
                self.spark = SparkSession.builder \
                    .appName("OpenSearchEval") \
                    .config("spark.driver.memory", "4g") \
                    .config("spark.executor.memory", "4g") \
                    .getOrCreate()
                
                logger.info("Created new Spark session")
            except ImportError:
                logger.error("PySpark not installed. Please install it with 'pip install pyspark'")
                raise
            except Exception as e:
                logger.error(f"Error initializing Spark session: {str(e)}")
                raise
    
    def load_data(self, path: str, format: str = "parquet") -> pd.DataFrame:
        """
        Load data from a file into a Spark DataFrame and convert to Pandas
        
        Args:
            path: File or directory path
            format: File format (parquet, csv, json, etc.)
            
        Returns:
            Pandas DataFrame with the data
        """
        try:
            spark_df = self.spark.read.format(format).load(path)
            pandas_df = spark_df.toPandas()
            logger.info(f"Loaded {len(pandas_df)} rows from {path}")
            return pandas_df
        except Exception as e:
            logger.error(f"Error loading data from {path}: {str(e)}")
            raise
    
    def save_data(self, df: pd.DataFrame, path: str, format: str = "parquet", mode: str = "overwrite") -> bool:
        """
        Save Pandas DataFrame to a file using Spark
        
        Args:
            df: Pandas DataFrame
            path: Output path
            format: Output format (parquet, csv, json, etc.)
            mode: Write mode (overwrite, append, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a Spark DataFrame from the Pandas DataFrame
            spark_df = self.spark.createDataFrame(df)
            
            # Save the data
            spark_df.write.format(format).mode(mode).save(path)
            
            logger.info(f"Saved {len(df)} rows to {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving data to {path}: {str(e)}")
            return False
    
    def run_spark_query(self, query: str) -> pd.DataFrame:
        """
        Run a Spark SQL query and return results as a Pandas DataFrame
        
        Args:
            query: Spark SQL query
            
        Returns:
            Pandas DataFrame with query results
        """
        try:
            result = self.spark.sql(query)
            pandas_df = result.toPandas()
            logger.info(f"Executed Spark SQL query, returned {len(pandas_df)} rows")
            return pandas_df
        except Exception as e:
            logger.error(f"Error executing Spark SQL query: {str(e)}")
            raise
    
    def process_search_logs(self, input_path: str, output_path: str) -> pd.DataFrame:
        """
        Process search logs using Spark
        
        Args:
            input_path: Path to input data
            output_path: Path to save processed data
            
        Returns:
            Pandas DataFrame with processed data
        """
        try:
            # Load the data
            spark_df = self.spark.read.format("parquet").load(input_path)
            
            # Register as temp view for SQL
            spark_df.createOrReplaceTempView("search_logs")
            
            # Process with Spark SQL
            processed_df = self.spark.sql("""
                SELECT
                    DATE(timestamp) as date,
                    query_text,
                    COUNT(*) as query_count,
                    COUNT(DISTINCT user_id) as unique_users,
                    AVG(num_results) as avg_result_count
                FROM search_logs
                GROUP BY DATE(timestamp), query_text
                ORDER BY query_count DESC
            """)
            
            # Save processed data
            processed_df.write.format("parquet").mode("overwrite").save(output_path)
            
            # Return as Pandas DataFrame
            result = processed_df.toPandas()
            logger.info(f"Processed {len(result)} search log records")
            return result
        except Exception as e:
            logger.error(f"Error processing search logs: {str(e)}")
            raise
    
    def close(self):
        """Close the Spark session"""
        if hasattr(self, 'spark'):
            self.spark.stop()
            logger.info("Closed Spark session")