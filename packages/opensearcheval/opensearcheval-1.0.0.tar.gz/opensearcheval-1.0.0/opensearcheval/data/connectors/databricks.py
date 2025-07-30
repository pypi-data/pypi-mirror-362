import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import os

logger = logging.getLogger(__name__)

class DatabricksConnector:
    """Connector for Databricks"""
    
    def __init__(
        self, 
        host: str, 
        token: str, 
        http_path: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None
    ):
        """
        Initialize the Databricks connector
        
        Args:
            host: Databricks host (e.g., 'adb-1234567890123456.78.azuredatabricks.net')
            token: Databricks access token
            http_path: HTTP path for the cluster
            catalog: Optional catalog name
            schema: Optional schema name
        """
        self.host = host
        self.token = token
        self.http_path = http_path
        self.catalog = catalog
        self.schema = schema
        
        try:
            # Import PySpark
            from pyspark.sql import SparkSession
            import pyspark.sql.functions as F
            
            # Build connection URL
            jdbc_url = f"jdbc:spark://{host}:443/;transportMode=http;ssl=1;httpPath={http_path};AuthMech=3;UID=token;PWD={token}"
            
            # Create Spark session
            self.spark = SparkSession.builder \
                .appName("OpenSearchEval-Databricks") \
                .config("spark.jars", self._get_jdbc_jar_path()) \
                .config("spark.driver.memory", "4g") \
                .getOrCreate()
            
            # Set catalog and schema if provided
            if catalog:
                self.spark.sql(f"USE CATALOG {catalog}")
                if schema:
                    self.spark.sql(f"USE SCHEMA {schema}")
            
            logger.info(f"Connected to Databricks: {host}")
        except ImportError:
            logger.error("PySpark not installed. Please install it with 'pip install pyspark'")
            raise
        except Exception as e:
            logger.error(f"Error connecting to Databricks: {str(e)}")
            raise
    
    def _get_jdbc_jar_path(self) -> str:
        """
        Get the path to the Databricks JDBC driver
        
        Returns:
            Path to the JDBC driver JAR
        """
        # Check common locations for the JAR
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "../../lib/databricks-jdbc.jar"),
            os.path.join(os.path.expanduser("~"), ".opensearcheval/lib/databricks-jdbc.jar"),
            "/opt/opensearcheval/lib/databricks-jdbc.jar"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # If not found, log a warning and return an empty string
        logger.warning("Databricks JDBC driver not found. Please download it and place it in one of these locations: " + 
                      ", ".join(possible_paths))
        return ""
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a SQL query against Databricks
        
        Args:
            query: SQL query
            params: Optional parameters for the query
            
        Returns:
            Pandas DataFrame with query results
        """
        try:
            # If params are provided, replace them in the query
            # This is a simple implementation, in practice you would use proper parameterization
            if params:
                for key, value in params.items():
                    placeholder = f":{key}"
                    if isinstance(value, str):
                        query = query.replace(placeholder, f"'{value}'")
                    else:
                        query = query.replace(placeholder, str(value))
            
            # Execute the query
            spark_df = self.spark.sql(query)
            
            # Convert to Pandas DataFrame
            pandas_df = spark_df.toPandas()
            
            logger.info(f"Executed query, returned {len(pandas_df)} rows")
            return pandas_df
        
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
    
    def load_table(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Load data from a Databricks table
        
        Args:
            table_name: Name of the table to load
            limit: Optional limit on the number of rows
            
        Returns:
            Pandas DataFrame with table data
        """
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        
        return self.execute_query(query)
    
    def load_search_logs(self, start_date: str, end_date: str, table_name: str = "search_logs") -> pd.DataFrame:
        """
        Load search logs from Databricks
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            table_name: Name of the search logs table
            
        Returns:
            Pandas DataFrame with search logs
        """
        query = f"""
        SELECT 
            query_id,
            query_text,
            user_id,
            session_id,
            timestamp,
            num_results,
            result_ids
        FROM {table_name}
        WHERE DATE(timestamp) BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY timestamp DESC
        """
        
        return self.execute_query(query)
    
    def save_dataframe(self, df: pd.DataFrame, table_name: str, mode: str = "overwrite") -> bool:
        """
        Save a Pandas DataFrame to a Databricks table
        
        Args:
            df: Pandas DataFrame to save
            table_name: Name of the target table
            mode: Write mode (overwrite, append, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert Pandas DataFrame to Spark DataFrame
            spark_df = self.spark.createDataFrame(df)
            
            # Save to table
            spark_df.write.mode(mode).saveAsTable(table_name)
            
            logger.info(f"Saved {len(df)} rows to table {table_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving data to table {table_name}: {str(e)}")
            return False
    
    def close(self):
        """Close the Spark session"""
        if hasattr(self, 'spark'):
            self.spark.stop()
            logger.info("Closed Databricks Spark session")