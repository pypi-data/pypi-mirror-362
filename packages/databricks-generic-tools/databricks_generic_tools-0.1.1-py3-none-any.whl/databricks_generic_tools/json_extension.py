import json
import datetime as dt
from typing import Any, Tuple
from pyspark.sql.functions import lit
from pyspark.sql import functions as fc
from pyspark.sql import DataFrame
from .debugprinter import DebugLevel, DebugPrinter
from .databricks_extension import get_dbutils, get_spark

dbutils_e = get_dbutils()
spark_e = get_spark()

### Type hints in this file are still massively incorrect.
### Requires a refactor to use and pass the correct types.


def read_jsonfile(json_location: str) -> str:
    """
    This function reads the content of a JSON file from the specified location and processes it 
    by replacing any escape sequences. It returns the JSON content as a string.
    :param json_location: str - The location of the JSON file to be read.
    :return: str - The content of the JSON file as a string, with escape sequences replaced.
    """

    # Read the entire file as a string using wholeTextFiles. This returns an RDD where each element 
    # is a tuple (file path, file content).
    json_rdd = spark_e.sparkContext.wholeTextFiles(json_location)
    # Extract the content from the first tuple element (ignoring the file path).
    json_string: str = json_rdd.collect()[0][1]
    
    return json_string  # Return the parsed JSON structure.


def create_jsonpath_list(json_path: str, json_data: str) -> list[str]:
    """
    Create a JSONPath list from the provided JSON path and data.
    Args:
        json_path (str): The JSON path to be used.
        json_data (str): The JSON data in string format.
    Returns:
        list: A list representing the JSONPath.
    """

    # Ensure the path starts with a dot ('.') for consistency.
    # All JSON files must start with either a { or a [ to be processable.
    # A JSON Path should start with '' as that is the position before the file is analysed.
    if json_data[0] == '{' or json_data[0] == '[':
        next
    else:
        json_data = '{' + json_data + '}'

    # Split the JSON path by dot ('.') into individual keys and return as a list
    json_path = '.' + json_path
    json_path_list = json_path.split('.')

    return json_path_list


def increase_level(level: int, previous_level: int, json_path: list, key: str, final: int, inPath: int) -> Tuple[int,int,int]:
    """
    Adjusts the current level based on the provided key and the JSON path.
    Args:
        level (int): The current level in the JSON path traversal.
        previous_level (int): The level before the current one.
        json_path (list): The list representing the JSON path.
        key (str): The key being checked against the next element in the JSON path.
        final (int): A flag indicating if the final level has been reached.
        inPath (int): A flag indicating if the key is in the current path.
    Returns:
        tuple: A tuple containing the updated level, final flag, and inPath flag.
    """
    
    # Set the current level to the previous level.
    # When then next iteration of the dictionary is reached the previous level should be used as this is the one before the last iteration.
    level = previous_level
    # Check if the next level is the last one in the json_path.
    # This is the lowest level that should be processed.
    if level + 1 == len(json_path):
        # If at the last level, keep the current level and set final to 1.
        final = 1
        inPath = inPath  # Retain the current inPath value.
    # Check if the provided key matches the next key in the json_path.
    # In that case a next level that is in the path has been found.
    elif key == json_path[level + 1]:
        # If there is a match, increment the level and set final to 0.
        level += 1
        final = 0
        inPath = 1  # Mark that the key is in the current path.
    else:
        # If there is no match, retain the current level and final value.
        level = level  # No change to the level.
        final = final  # Retain the current final value.
        inPath = 0  # Mark that the key is not in the current path.
    
    return level, final, inPath


def create_new_key_col(parent_key: str, i: int, item: Any) -> str:
    """
    Creates a new key for a given item in a list or dictionary and increments the field count if necessary.
    If the item is a dictionary, the parent key is used. If the item is not a dictionary (list), a positional suffix is added
    to the parent key to form the new key. Additionally, it increments the nth_field for non-dictionary items.

    Args:
        parent_key (str): The key of the parent element.
        i (int): The position index of the item in a list.
        item (any): The current item in the list (can be a dict or any other type).
        nth_field (int): A counter to track fields at a certain position level.
    Returns:
        tuple: A tuple containing the new key (str) and the updated nth_field (int).
    """
    
    # Check if the current item is a dictionary
    if isinstance(item, dict):
        # If item is a dictionary, retain the parent key
        new_key = parent_key
    else:
        # If item is not a dictionary, append positional index to parent key
        new_key = f'{parent_key}_P{i:03}'   
        # Increment the nth_field to track the number of fields at the current level

    return new_key


def flatten_json(data: Any, 
                 json_path: list, 
                 row: dict, 
                 dataset: list, 
                 level: int = 0, 
                 final: int = 0, 
                 parent_key: str = None, 
                 added_keys: list = [], inPath=0  
                 ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """
    Flattens a nested JSON structure into a flat list of dictionaries.
    Args:
        data (any): The JSON data (could be a dict, list, or other types).
        json_path (list): The path to the desired JSON keys.
        row (dict): The current dictionary being built. This is row level
        dataset (list): The list where the final flattened dictionaries will be stored.
        level (int, optional): The current level in the JSON structure (default is 0).
        final (int, optional): A flag indicating if the final level has been reached (default is 0).
        parent_key (str, optional): The key for the current level of flattening (default is None).
        added_keys (list, optional): A list of keys added during the flattening process (default is empty) for that level.
        inPath (int, optional): A flag indicating if the key is in the current path (default is 0).
    Returns:
        tuple: A tuple containing the flattened dataset and any additional data.
    """

    # Check if the input data is a dictionary.
    if isinstance(data, dict):
        previous_level: int = level  # Store the previous level.
        added_keys = []  # Reset added_keys for this level.
        # Iterate through key-value pairs in the dictionary.
        for key, value in data.items():
            # Determine the new level and flags based on the key.
            level, final, inPath = increase_level(level, previous_level, json_path, key, final, inPath)
            new_key: str = f'{parent_key}_{key}' if parent_key else key  # Create a new key for the flattened structure.

            # Check if we are at the final level.
            if final == 1:
                #If in the final level there is a dictionary. A list of keys is stored in the columns.
                if isinstance(value, dict):
                    keys = ', '.join(value.keys())  # Join keys for a string representation.
                    valueString = f"Keys: {key}"  # Prepare the value string.
                    flatten_json(valueString, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath) 
                else:
                    # If the final level is not a dictionary, analyse further
                    flatten_json(value, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath)
            # If the next step in the path is reached:
            elif level > previous_level:
                flatten_json(value, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath)  
            # If something is a key that is found while traveling the path (but it is not in the path):
            elif level == previous_level:
                # A list of keys is stored in the columns.
                if isinstance(value, dict):
                    keys = ', '.join(value.keys())
                    valueString = f"Keys: {keys}"
                    flatten_json(valueString, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath) 
                # If not a dictionary analyse further
                else:
                    flatten_json(value, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath)    
            else:
                break  # Break if level conditions are not met.

        # If we are done with the current level, append the row to the dataset.
        if previous_level >= level:
            dataset.append(row.copy()) 
        # Clear any added keys from this level in the row-level-dictionary.
        for added_key in added_keys:
            if added_key in row:
                row[added_key] = ''  # Reset added key to an empty string.
        added_keys = []  # Clear added_keys for this level.  

    # Check if the input data is a list.
    elif isinstance(data, list):
        # If at the final level, record the number of list items. 
        if final == 1:
            valueString = str(len(data))  # Create a string representation of the list length.
            new_key = f"{parent_key}_NumberOfListItems"  # Create a new key for the number of items.
            flatten_json(valueString, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath)
        else:
            # Iterate through items in the list.
            for i, item in enumerate(data):
                new_key = create_new_key_col(parent_key, i, item)  # Generate a new key for the list item.
                flatten_json(item, json_path, row, dataset, level, final, parent_key=new_key, added_keys=added_keys, inPath=inPath)            
            
    else:
        # If the data is neither a list nor a dict, update the row with the value.
        row.update({parent_key: data})  # Update the row with the current value.
        added_keys.append(parent_key)  # Record the added key.

    return dataset


def create_timestamp_from_str(Datestring: str) -> str:
    """
    This function takes a date string and converts it into a formatted timestamp string.
    The input string is expected to represent a date and time, and if necessary, the function pads it 
    to ensure it has the correct length for processing.
    :param Datestring: str - A string representing the date and time, potentially requiring padding.
    :return: str - A formatted timestamp string in the format 'YYYY-MM-DD HH:MM:SS.ssssss'.
    """
    
    # Ensure Datestring is padded correctly if its length is not already 17 characters.
    if len(Datestring) == 17:
        pass  # If the length is already 17, no padding is required.
    else:
        # Add padding zeros to ensure the length of the Datestring is exactly 17 characters.
        Datestring = Datestring + '000000000'
    # Extract the individual components (year, month, day, hour, minute, second, millisecond) from the Datestring.
    year: int = int(Datestring[0:4])
    month: int = int(Datestring[4:6])
    day: int = int(Datestring[6:8])
    hour: int = int(Datestring[8:10])
    minute: int = int(Datestring[10:12])
    second: int = int(Datestring[12:14])
    millisecond: int = int(Datestring[14:17])
    # Create a datetime object using the extracted components. 
    # Milliseconds are converted to microseconds by multiplying by 1000 (since datetime requires microseconds).
    timestamp: dt.datetime = dt.datetime(year, month, day, hour, minute, second, millisecond * 1000)
    timestampstr: str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")

    return timestampstr


def add_fields_to_df(df: DataFrame, Datestring: str, SourceConfigId: int, TableName: str, DeltaTableName: str, pk_columns: str):
    """
    Adds additional fields to a DataFrame for JSON output.
    Args:
        df: The input DataFrame to which fields will be added.
        Datestring (str): A string representing the landing date and time.
        SourceConfigId (int): An identifier for the source configuration.
        TableName (str): The name of the source table.
        DeltaTableName (str): The name of the Delta table from which to derive the primary key.
    Returns:
        DataFrame: The updated DataFrame with additional fields.
    """
    # Create a timestamp from the provided date string.
    LandingDateTime = create_timestamp_from_str(Datestring)
    # Retrieve the list of primary key columns from the Delta table.
    # Add a new column for the landing date and time.
    df = df.withColumn('__LandingDateTime', lit(LandingDateTime))
    # Add a new column for the source configuration ID.
    df = df.withColumn('__SourceConfigId', lit(SourceConfigId))
    # Add a new column for the source table name.
    df = df.withColumn('__SourceTableName', lit(TableName))
    # Create a concatenated primary key column from the primary key columns.
    pk_column_list = pk_columns.split('.')
    df = df.withColumn('PrimaryKeyColumn', fc.concat_ws("_", *[fc.col(c).cast("string") for c in pk_column_list]))

    return df


def clean_dataset(dataset: tuple[list[dict[str, str]], list[dict[str, str]]]) -> list[dict[str, str]]:
    """
    Cleans a dataset by ensuring that each dictionary in the dataset has consistent keys.
    Args:
        dataset (list): A list containing one or more lists of dictionaries.
    Returns:
        list: A list of cleaned dictionaries with consistent keys.
    """
    # Create an empty dictionary with keys from the last dictionary. This dict has all the fields that were found.
    # initialized to a dictionary with empty values.
    empty_dict = {key: '' for key in dataset[-1]}
    cleaned_dict: list[dict[str,str]] = []  # Initialize a list to hold the cleaned dictionaries.
    # Iterate over each dictionary in the first list of the dataset.
    for data in dataset:
        # data = list[dict[str, str]]
        # Use the empty dictionary as a base for cleaning.
        temp_dict = empty_dict.copy()  # Copy the empty_dict to avoid mutating it.
        # Update the temporary dictionary with the current data.
        temp_dict.update(data)
        # Append the cleaned dictionary to the cleaned_dict list.
        cleaned_dict.append(temp_dict)
    
    return cleaned_dict  # Return the list of cleaned dictionaries.


def load_json_to_df(json_location: str, DeltaTableName: str, FolderName: str, SourceConfigId: int, TableName: str, json_search_path: str, pk_columns: str):
    """
    Converts JSON data into a pandas DataFrame based on a specified JSON path.
    The JSON data is flattened and then structured into a tabular format.
    Args:
        json_data (str): The JSON data in string format to be processed.
        json_path (str): The dot-separated path in the JSON structure to extract the relevant data.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the flattened and corrected JSON data.
    """
    # Between start and the end of a path, stores the values, unpack lists and dictionaries. If dictionary is not in path do not unpack but store keys.
    # If the end of path is reached: Store values, give number of items in list and store keys in dictionary.
    # Get json data
    DebugPrinter.Msg(f"Read json file on: {json_location}", DebugLevel.Informational)
    json_string: str = read_jsonfile(json_location)
    data = json.loads(json_string)
    # Convert the dot-separated JSON path into a list of path components.
    json_path_list: list[str] = create_jsonpath_list(json_search_path, json_string)
    # Flatten the JSON structure based on the given path and initialize empty structures for row, dataset, and added items.
    DebugPrinter.Msg(f"Start flattening json file: {json_location}", DebugLevel.Informational)
    dataset = flatten_json(data, json_path_list, row={}, dataset=[], added_keys = [])
    DebugPrinter.Msg(f"Finished flattening json file: {json_location}", DebugLevel.Informational)
    # Give all dictionaries the same columns
    standardized_dataset = clean_dataset(dataset)
    DebugPrinter.Msg(f"Write dataframe from flattened json file: {json_location}", DebugLevel.Informational)
    df = spark_e.createDataFrame(standardized_dataset)
    #Add fields necessary for the Delta Lake table.
    DebugPrinter.Msg(f"Add necessary fields to dataframe for file on location: {json_location}", DebugLevel.Informational)
    df = add_fields_to_df(df, FolderName, SourceConfigId, TableName, DeltaTableName, pk_columns)
    NRecordsToWrite = df.count()
    DebugPrinter.Msg(f"Flattening json-file and writing it to a dataframe finalized for files in: {json_location}", DebugLevel.Informational)
    
    return df, NRecordsToWrite