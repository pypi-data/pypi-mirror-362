import os
from pyspark.sql import SparkSession
 

__all__ = [
    'is_running_in_databricks',
    'get_dbutils',
    'get_spark',
]


def is_running_in_databricks() -> bool:
    try:                
        return "DATABRICKS_RUNTIME_VERSION" in os.environ or 'dbutils' in globals() or 'spark' in globals()
    except:
        return False

def get_spark() -> SparkSession:
    try:
        # Check if running inside Databricks by testing known environment variables
        if 'DATABRICKS_RUNTIME_VERSION' in os.environ:
            # Already inside a Databricks notebook
            from pyspark.sql import SparkSession
            return SparkSession.builder.getOrCreate()
        else:
            # Outside Databricks, assume local development
            from databricks.connect import DatabricksSession
            return DatabricksSession.builder.getOrCreate()
    except Exception as e:
        raise RuntimeError(f"Failed to create SparkSession: {e}")
    
def get_dbutils():
    try:
        from databricks.sdk import WorkspaceClient
        return WorkspaceClient().dbutils
    except:
        raise ImportError("Databricks SDK unable to initialize dbutils.")





