import zipfile
import io
import os
from .debugprinter import DebugLevel, DebugPrinter

def extract_and_store_from_zipfile(LocFrom: str, LocToUnzipped: str, ZipFileNameFilter: str) -> str:
    """
    Extracts and processes files from a zip archive located in Azure Storage, storing the extracted files 
    into an unzipped folder and renaming the file based on the DeltaTableName.
    Warning: File is read into dataframe, then unzipped to local storage of databricks and then copied to azure storage.
    Args:
        LocFrom (str): The location (path) from where the zip file is read (Azure Storage path).
        LocToUnzipped (str): The destination folder where the extracted file is stored.
    Returns:
        str: The name of the extracted file from the zip archive.
    """
    DebugPrinter.Msg(f'Start extracting and storing zipfile for {LocFrom}', DebugLevel.Informational)
    
    # Get zip file, unzip and store on databricks storage, then store file on azure storage.
    # Read the zip file from Azure Storage into memory
    zip_file_data = spark.read.format("binaryFile").load(LocFrom).select("content").collect()[0][0]
    # Open the in-memory zip file and read its contents
    DebugPrinter.Msg(f'Start processing zipfile for {LocFrom}', DebugLevel.Informational)
    with zipfile.ZipFile(io.BytesIO(zip_file_data), 'r') as zip_ref:
        # Find the correct file inside the zip archive that matches the ZipFileNameFilter
        fileName = [Name for Name in zip_ref.namelist() if ZipFileNameFilter in Name][0] #For now only take the first file that matches ZipFileNameFilter.
        DebugPrinter.Msg(f'Start processing filename: {fileName}', DebugLevel.Informational)
        # Extract the content of the identified file as bytes
        localFilePath = f"/tmp/unzipped_files/{utcRunDatetime()}"
        # Extract to the local file system first
        zip_ref.extract(fileName, localFilePath)
        # Move the extracted file tothe local file system to the Azure Storage location.
        dbutils.fs.cp(f"file:{localFilePath}/{fileName}", f"{LocToUnzipped}/{fileName}")
        if os.path.exists(f"{localFilePath}/{fileName}"):
            os.remove(f"{localFilePath}/{fileName}")  # Remove the file on databricks storage.
            DebugPrinter.Msg(f"Removed temporary file: {localFilePath}/{fileName}", DebugLevel.Informational)
    DebugPrinter.Msg(f'Finished extracting and storing zipfile for {LocFrom}', DebugLevel.Informational)