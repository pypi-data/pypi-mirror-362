from pyspark.sql import SparkSession, DataFrame, Row
from typing import List, Tuple, Dict
from collections import namedtuple
import time
from .debugprinter import DebugLevel, DebugPrinter #this is the correct way to import from a relative path
from databricks.sdk.runtime import spark as spark

def createDatabricksSchema(schemaName: str, location: str) -> None:
    """
    Simply create the catalog schema if it does not exist.
    """
    spark.sql(f'CREATE SCHEMA IF NOT EXISTS {schemaName} LOCATION "{location}"')

def __restore_Or_Reset_DeltaTable(targetSchema: str, deltaTableName: str, targetVersion: int, targetFolder: str) -> bool:
    """
    Restore to previous situation. When Deltatable existed before current loop, then return to version that was loaded successfull.
    Otherwise, drop deltatable and remove files that are in the assigned folder (staging).
    """
    DebugPrinter.Msg('Function restore_Or_Reset_DeltaTable should not be called?', DebugLevel.Critical)
    if(spark.catalog.tableExists(f'{targetSchema}.{deltaTableName}')):
        restore_DeltaTable(targetSchema, deltaTableName, targetVersion)
        return True
    else:
        reset_DeltaTable(targetSchema, deltaTableName, targetFolder)
        return False

def reset_DeltaTable(targetSchema: str, deltaTableName: str, targetFolder: str) -> None:
    """
    Delete the entire deltatable (because no valid version exists)
    """
    spark.sql(f'DROP TABLE IF EXISTS {targetSchema}.{deltaTableName}')

    try:
        listoffiles = dbutils.fs.ls(targetFolder)
        DebugPrinter.Msg(f'Deleting files in folder {targetFolder}.', DebugLevel.Verbose)
        deletedFileCount: int = 0
        for file in listoffiles:
            dbutils.fs.rm(file.path, recurse=True) # Deletes the actual files
            deletedFileCount += 1
        DebugPrinter.Msg(f'Finished deleting {deletedFileCount} files.', DebugLevel.Informational)
    except FileNotFoundError:
        DebugPrinter.Msg(f'Folder [{targetFolder}] does not exist, no need to delete content.', DebugLevel.Informational)
    except Exception as e:
        if "java.io.FileNotFoundException" in str(e):
            DebugPrinter.Msg(f'Folder [{targetFolder}] does not exist, no need to delete content (java message).', DebugLevel.Informational)
        else:
            DebugPrinter.Msg(f'Error while trying to reset DeltaTable. : ' + str(e), DebugLevel.Critical)
            raise(e)
    DebugPrinter.Msg(f'Dropped the DeltaTable and deleted all files in targetfolder "{targetFolder}"', DebugLevel.Verbose)

    for attempt in range(10):  # Retry logic to ensure table creation was succesful. 
        try: # Try refreshing the table regardless of existence        
            spark.sql(f"REFRESH TABLE {targetSchema}.{deltaTableName}")
            DebugPrinter.Msg('Table metadata refresh succeeded, but should have failed.', DebugLevel.Warnings)            
            if attempt == 9:  # After 10 attempts, raise the error
                DebugPrinter.Msg('Maximum attempts reached, code will continue with a high chance of failure.', DebugLevel.Warnings)
                break     
            time.sleep(1)
            DebugPrinter.Msg(f"Retrying refresh after delete... (Attempt {attempt + 1})", DebugLevel.Warnings)
        except Exception as e:        
            if "TABLE_OR_VIEW_NOT_FOUND" in str(e).upper():  # This error indicates the drop was already processed correctly, refresh was not required. This is okay!                
                DebugPrinter.Msg(f'Table does not exist, refresh skipped.', DebugLevel.Verbose)
                break
            else:         
                if attempt == 9:  # After 10 attempts, raise the error
                    DebugPrinter.Msg(f'Unexpected error on refreshing table after reset, might not impact result.', DebugLevel.Critical)
                    break
                time.sleep(1)
                DebugPrinter.Msg(f"Retrying refresh after delete... (Attempt {attempt + 1})", DebugLevel.Warnings)

def restore_DeltaTable(targetSchema: str, deltaTableName: str, targetVersion: int) -> bool:
    """
    Restores a Delta table to a specified version, or truncates it if no valid version exists.

    Args:
        targetSchema (str): The schema where the Delta table is located.
        deltaTableName (str): The name of the Delta table to be restored.
        targetVersion (int): The version to which the table should be restored. If -1 or None, the table will be truncated.

    Returns:
        bool: True if the restore or truncation was successful, False if the table did not exist.

    Functionality:
        - If the table exists and a valid target version is provided, it restores the Delta table to that version.
        - If no valid version is provided (-1 or None), it truncates the table.
        - If the table does not exist, it logs a failure and returns False.
    """
    tableIdentifier: str = f'{targetSchema}.{deltaTableName}'
    if spark._jsparkSession.catalog().tableExists(tableIdentifier):
        if targetVersion == -1 or targetVersion is None:
            DebugPrinter.Msg(f'There was never a valid version, but the table exists, therefor truncating it.', DebugLevel.Warnings)
            spark.sql(f'TRUNCATE TABLE {tableIdentifier}')
            return True
        else:            
            spark.sql(f'RESTORE TABLE {tableIdentifier} TO VERSION AS OF {targetVersion}')
            DebugPrinter.Msg(f'Restored DeltaTable to version {targetVersion}', DebugLevel.Warnings)
            return True
    else:
        DebugPrinter.Msg(f'DeltaTable did not exist, restore failed', DebugLevel.Critical)
        return False

def get_DeltaTable_Version(targetSchema: str, deltaTableName: str) -> int:
    """
    Get current active DeltaTable version.

    Returns -2 if it failed to get a valid version. Because -1 has a deltatable version meaning (= last table version).
    """
    version: int = -2
    if spark._jsparkSession.catalog().tableExists(f'{targetSchema}.{deltaTableName}'):
        version = spark.sql(f'DESCRIBE HISTORY {targetSchema}.{deltaTableName} LIMIT 1').collect()
        version = int(version[0].asDict()['version'])
    DebugPrinter.Msg(f'Collected deltatable version "{version}".', DebugLevel.Informational)
    return version

def get_DeltaTable_Columns(targetSchema: str, deltaTableName: str) -> List[Tuple[str, str]]:
    """
    Fetches the column names and data types of a DeltaTable.
    """
    columnList: List[Row] = spark.sql(f"DESCRIBE TABLE {targetSchema}.{deltaTableName}").select('col_name', 'data_type').collect()
    return [(row['col_name'], row['data_type']) for row in columnList]

def get_DeltaTable_Count(targetSchema: str, deltaTableName: str) -> int:
    """
    Fetches the row count of a DeltaTable.
    
    Parameters:
    targetSchema (str): The schema of the DeltaTable.
    deltaTableName (str): The name of the DeltaTable.
    
    Returns:
    int: The row count of the DeltaTable. Returns 0 if the table does not exist.
    """
    DebugPrinter.Msg('Fetching DeltaTable rowcount.', DebugLevel.Verbose)
    if not spark.catalog.tableExists(f'{targetSchema}.{deltaTableName}'):
        return 0
    else:
        return spark.sql(f'SELECT COUNT(*) AS row_count FROM {targetSchema}.{deltaTableName}').first()["row_count"]

def append_DeltaTable_Data(SchemaTo: str, TableName: str, dataFrame: DataFrame) -> None:
    """
    Appends data from a DataFrame to a DeltaTable.
    
    Parameters:
    SchemaTo (str): The schema of the DeltaTable.
    TableName (str): The name of the DeltaTable.
    dataFrame (DataFrame): The DataFrame to append to the DeltaTable.
    """    
    DebugPrinter.Msg('Started appending data from dataframe to the DeltaTable.', DebugLevel.Informational)
    dataFrame.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(f"{SchemaTo}.{TableName}")
    DebugPrinter.Msg('Finished appending data from dataframe to the DeltaTable.', DebugLevel.Informational)

def append_DeltaTable_Data_WithRowcount(SchemaTo: str, TableName: str, dataFrame: DataFrame, oldRowCount: int) -> Tuple[int, int]:    
    """
    Appends data from a DataFrame to a DeltaTable and returns the new row count and the number of rows written.
    
    Parameters:
    SchemaTo (str): The schema of the DeltaTable.
    TableName (str): The name of the DeltaTable.
    dataFrame (DataFrame): The DataFrame to append to the DeltaTable.
    oldRowCount (int): The old row count of the DeltaTable.
    
    Returns:
    Tuple[int, int]: The number of rows written [0] and the new row count [1].
    """
    append_DeltaTable_Data(SchemaTo, TableName, dataFrame)
    newRowCount = get_DeltaTable_Count(SchemaTo, TableName)
    writtenRecordCount = newRowCount - oldRowCount
    return writtenRecordCount, newRowCount

GeneratedColumn = namedtuple('GeneratedColumn', ['ColumnName', 'TargetDataType', 'ColumnDefinition'])
FixedColumn = namedtuple('FixedColumn', ['ColumnName', 'DataType'])

def DeltaTableCreateSQL(SchemaTo: str, TableName: str, LocationTo: str, PartitionColumnName: str, columnDefinitionList: List[FixedColumn]) -> str:
    """
    Returns a SQL Statement in string format that can be executed with spark to create a deltatable. 
    Automatically calculates the column definitions based on the schema from the DataFrame parameter.

    Args:
        SchemaTo (str): The schema where the table will be created.
        TableName (str): The name of the Delta table to be created.
        LocationTo (str): The file path where the Delta table will be stored.
        PartitionColumnName (str): The column by which the table will be partitioned.
        columnDefinitionList (List[FixedColumn]): A list of FixedColumn objects, each having ColumnName and DataType attributes.

    Returns:
        str: A SQL query string to create the Delta table.
    """    
    col_string: str = ', '.join(f"`{col.ColumnName}` {col.DataType}" for col in columnDefinitionList)
    createSQL: str = (
            f"CREATE TABLE IF NOT EXISTS {SchemaTo}.{TableName} "
            f"({col_string}) "
            f"USING DELTA LOCATION '{LocationTo}' "
            f"PARTITIONED BY ({PartitionColumnName})"
        )   
    return createSQL

def DeltaTableCreateSQLWithGeneratedColumns(SchemaTo: str, TableName: str, LocationTo: str, PartitionColumnName: str, columnDefinitionList: List[FixedColumn], generatedColumns: List[GeneratedColumn]) -> str:
    """
    Returns a sql statement in string format that can be executed with spark to create a deltatable. 
    Automatically calculates the column definitions based on the schema from the DataFrame parameter 
    and adds the generated columns beneath.
    """    
    DebugPrinter.Msg(f"Attempting to build table creation statement based on {len(columnDefinitionList)} columndefinitions.", DebugLevel.Informational)
    col_string: str = ', '.join(f'`{col.ColumnName}` {col.DataType}' for col in columnDefinitionList)
    generated_columns_definitions = [f", `{col.ColumnName}` {col.TargetDataType} GENERATED ALWAYS AS ({col.ColumnDefinition})" for col in generatedColumns]
    generated_columns_string = ' '.join(generated_columns_definitions)
    createSQL: str = f"CREATE TABLE IF NOT EXISTS {SchemaTo}.{TableName} ({col_string}{generated_columns_string}) USING DELTA LOCATION '{LocationTo}' PARTITIONED BY ({PartitionColumnName})"
    return createSQL

def DeltaTableCreate(  SchemaTo: str
                     , TableName: str
                     , LocationTo: str
                     , PartitionColumnName: str
                     , columnDefinitionList: List[FixedColumn]
                     , generatedColumns: List[GeneratedColumn] = None
                     , tblProperties: Dict[str, str] = None
                     ) -> None:
    """
    Creates a DeltaTable with the given parameters.

    Parameters:
    SchemaTo (str): The schema of the DeltaTable.
    TableName (str): The name of the DeltaTable.
    LocationTo (str): The location of the DeltaTable.
    PartitionColumnName (str): The name of the partition column.
    columnDefinitionList (List[FixedColumn]): A list of FixedColumn objects.
    generatedColumns (List[GeneratedColumn]): A list of GeneratedColumn objects.
    tblProperties (Dict[str, str]): A dictionary of table properties.
    """
    namedColumnDefinitionList: List[FixedColumn] = [col if isinstance(col, FixedColumn) else FixedColumn(*col) for col in columnDefinitionList]
    if generatedColumns:
        namedGeneratedColumns: List[GeneratedColumn] = [col if isinstance(col, GeneratedColumn) else GeneratedColumn(*col) for col in generatedColumns]
        tableCreationSQL: str = DeltaTableCreateSQLWithGeneratedColumns(SchemaTo, TableName, LocationTo, PartitionColumnName, namedColumnDefinitionList, namedGeneratedColumns)
    else:
        tableCreationSQL: str = DeltaTableCreateSQL(SchemaTo, TableName, LocationTo, PartitionColumnName, namedColumnDefinitionList)
    DebugPrinter.Msg(f"tableCreationStatement created: [\n{tableCreationSQL}\n]", DebugLevel.Maximal)
    spark.sql(tableCreationSQL)
    DebugPrinter.Msg('DeltaTable created.', DebugLevel.Informational)
    if tblProperties:
        properties_string = ', '.join([f"'{key}' = '{value}'" for key, value in tblProperties.items()])
        spark.sql(f"ALTER TABLE {SchemaTo}.{TableName} SET TBLPROPERTIES ({properties_string})")        
        DebugPrinter.Msg('DeltaTable properties configured.', DebugLevel.Verbose)

    for attempt in range(10):  # Retry logic to ensure table creation was succesful. 
        try:
            spark.sql(f"REFRESH TABLE {SchemaTo}.{TableName}")  # Refresh the table to ensure the latest metadata is used.
            DebugPrinter.Msg('DeltaTable refreshed to make sure it exists for any following commands.', DebugLevel.Verbose)
            spark.sql(f"OPTIMIZE {SchemaTo}.{TableName}")
            DebugPrinter.Msg('DeltaTable optimized to make sure the create transactions are fully processed.', DebugLevel.Informational)       
            break
        except Exception as e:
            if attempt == 9:  # After 10 attempts, raise the error
                raise
            time.sleep(1)
            DebugPrinter.Msg(f"Retrying refresh... (Attempt {attempt + 1})", DebugLevel.Warnings)
    