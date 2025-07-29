import pyodbc
import threading
from typing import Optional, List, Any
from .debugprinter import DebugPrinter, DebugLevel

__all__ = ["odbcConnector", "AzureFileStorageLocationURI", "Row"]


def AzureFileStorageLocationURI(containerName: str, storageAccount: str, subFolderPath: str) -> str:
    return f"abfss://{containerName}@{storageAccount}.dfs.core.windows.net/{subFolderPath}"

Row = pyodbc.Row  # Type alias for pyodbc.Row, which is used to represent a row in the result set.

class odbcConnector:
    """
    A class to handle ODBC database connections and operations with thread safety.
    """
    _lockConnection = threading.Lock()  # Class-level lock    

    def __init__(self, secretConnectionString: str) -> None:
        """
        Initializes the odbcConnector with a connection to the database.

        Fetch the connectionstring you want to pass from the keyvault using a command like 'dbutils.secrets.get(scope=self._keyvaultScope, key=self._keyvaultSecretName)'.

        Args:
            keyvaultScope (str): The scope within the key vault to retrieve the secret.
            keyvaultSecretName (str): The name of the secret that contains the connection string.

        Raises:
            Exception: If the connection test fails.
        """
        DebugPrinter.Msg('start creating odbc connector', DebugLevel.Verbose)                    
        self._buildConnection(secretConnectionString)
        self.testConnection()

    def _buildConnection(self, secretConnectionString: str) -> None:
        """
        Builds the database connection and sets the cursor using the connection string
        retrieved from the key vault.

        Fetch the connectionstring you want to pass from the keyvault using a command like 'dbutils.secrets.get(scope=self._keyvaultScope, key=self._keyvaultSecretName)'.
        """
        self.ConnectionString: str = secretConnectionString
        with odbcConnector._lockConnection:            
            self.DatabaseConnection: pyodbc.Connection = pyodbc.connect(self.ConnectionString)
            self.Cursor: pyodbc.Cursor = self.DatabaseConnection.cursor()            

    def executeAndCommit(self, sqlcommand: str, arguments: Optional[List[Any]] = None) -> None:
        """
        Executes a SQL command and commits the transaction.

        Args:
            sqlcommand (str): The SQL command to be executed.
            arguments (Optional[List]): Optional list of arguments for parameterized queries.

        Raises:
            pyodbc.Error: If an error occurs during SQL execution or commit.
        """        
        with odbcConnector._lockConnection:
            if (not self.DatabaseConnection) or self.DatabaseConnection.closed:
                DebugPrinter.Msg(f'Tried to execute statement while connection was not available.', DebugLevel.Critical) 
                # TO-DO: Rebuild the connection instead of raising an exception. Keep the lock in mind, you can not double lock. 
                raise Exception("Database connection is closed.")
            if arguments is None:
                self.Cursor.execute(sqlcommand)
            else:
                self.Cursor.execute(sqlcommand, arguments)        
            self.DatabaseConnection.commit()

    def testConnection(self) -> None:
        """
        Tests the database connection by executing a simple query.

        Raises:
            Exception: If the connection test fails.
        """
        try:
            with odbcConnector._lockConnection:
                self.Cursor.execute("SELECT 1")
                self.Cursor.fetchone()
                DebugPrinter.Msg('Connection test successful.', DebugLevel.Informational)
        except Exception as e:
            DebugPrinter.Msg(f'Connection test failed: {e}', DebugLevel.Critical)            
            self.DatabaseConnection.close()
            raise