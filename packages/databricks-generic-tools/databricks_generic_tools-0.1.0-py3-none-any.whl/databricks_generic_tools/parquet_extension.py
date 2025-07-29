from pyspark.sql import DataFrame
from typing import Tuple
import os
from .debugprinter import DebugLevel, DebugPrinter
from .databricks_extension import get_dbutils, get_spark

dbutils_e = get_dbutils()
spark_e = get_spark()

def copyParquetFile(locationFrom: str, targetLocation: str):
    """
    Copy a Parquet file from an ADFS location to another ADFS location.

    Args:
        location_from (str): The source location of the Parquet file.
        target_location (str): The target location to copy the file to.
    """    
    try:
        DebugPrinter.Msg(f'Start copying file from [{locationFrom}] to [{targetLocation}]', DebugLevel.Verbose)
        dbutils_e.fs.cp(locationFrom,targetLocation)
        DebugPrinter.Msg('File copied successfully using dbutils.', DebugLevel.Verbose)
    except:
        df = spark_e.read.parquet(locationFrom)
        df.write.mode('overwrite').parquet(targetLocation)
        DebugPrinter.Msg('File copied successfully using spark because dbutils copy failed.', DebugLevel.Warnings)

def read_ParquetFile(location: str) -> Tuple[DataFrame, int]: 
    """
    Read file and return dataframe and number of records in dataframe
    """
    DebugPrinter.Msg(f'Reading parquetfile from "{location}".', DebugLevel.Verbose)

    # Check if file exists
    try:
        folderPath: str = os.path.dirname(location)
        #fileName: str = os.path.basename(location)
        fileList = dbutils_e.fs.ls(folderPath)
        fileCount: int = len(fileList)
        fileExists: bool = bool(fileCount > 0)
        DebugPrinter.Msg(f"Found {fileCount} files at the given location.", DebugLevel.Informational)
    except Exception as e:
        DebugPrinter.Msg('Error checking whether file exists.', DebugLevel.Critical)        
        raise e

    if not fileExists:
        raise FileNotFoundError(f'No file exists at the provided path. [{location}]')

    try:
        parquetFileData = spark_e.read.parquet(location)
    except Exception as e:
        DebugPrinter.Msg('Unable to parse parquetfile into DataFrame. Possibly corrupt parquet file.', DebugLevel.Critical)        
        raise e

    recordCount: int = parquetFileData.count()
    DebugPrinter.Msg(f'Read {recordCount} records from parquetfile.', DebugLevel.Informational)       
    return parquetFileData, recordCount

def testStorageConnection(rootContainerName: str) -> bool:
    """
    Try to list the contents of the container, if it succeeds, then connecting is successful.
    """
    try:
        files = dbutils_e.fs.ls(rootContainerName)
        DebugPrinter.Msg(f"Successfully connected to the container. Found {len(files)} items.", DebugLevel.Informational)
        return True
    except Exception as e:
        DebugPrinter.Msg(f"Connection failed: {e}", DebugLevel.Warnings)        
        return False