from typing import List, Any, final
from abc import abstractmethod
from .debugprinter import DebugLevel, DebugPrinter
from .connectors import odbcConnector, Row

__all__ = ["SqlCommand", "SqlProcedure", "SqlTableValuedFunction", "SqlScalarValuedFunction", "add_brackets"]

def add_brackets(name: str) -> str:
    return f'[{name.strip("[]")}]'

class SqlCommand:
    @final
    def __init__(self, procedureSchema: str, procedureName: str, procedureArgumentValues: list[Any]):
        self.procedureSchema: str = add_brackets(procedureSchema)
        self.procedureName: str = add_brackets(procedureName)
        self.procedureArgumentValues: list[Any] = procedureArgumentValues

    @abstractmethod
    def getSqlCommand(self) -> str:
        """This method should be implemented in the child classes."""
        pass

    @final
    def execute(self, connector: odbcConnector) -> None:
        connector.executeAndCommit(self.getSqlCommand(), self.procedureArgumentValues)

    def executeAndFetchAll(self, connector: odbcConnector) -> List[Row]:
        """
        This method can be overridden by subclasses that can fetch multiple rows.
        The default implementation raises a NotImplementedError.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def executeAndFetchScalar(self, connector: odbcConnector) -> Any:
        """
        This method can be overridden by subclasses that can fetch a single scalar value.
        The default implementation raises a NotImplementedError.
        """
        raise NotImplementedError("This method must be implemented by subclasses that support fetching scalar values.")

class SqlProcedure(SqlCommand):
    """
    Example usage:
    proc = SqlProcedure('MyProcedure', 'dbo', ['arg1', 'arg2', 'arg3'])
    print(proc.getSqlCommand())
    """ 
    def getSqlCommand(self) -> str:
        parameterList = ', '.join(['?' for _argumentValue in self.procedureArgumentValues])
        return f'EXEC {self.procedureSchema}.{self.procedureName} {parameterList}'    
 
    def executeAndFetchAll(self, connector: odbcConnector) -> List[Row]:
        connector.Cursor.execute(self.getSqlCommand(), self.procedureArgumentValues)
        connector.DatabaseConnection.commit()
        return connector.Cursor.fetchall()

class SqlTableValuedFunction(SqlCommand):
    """
    Example usage:
    proc = SqlTableValuedFunction('MyTVF', 'dbo', ['arg1', 'arg2', 'arg3'])
    print(proc.getSqlCommand())
    """ 
    def getSqlCommand(self) -> str:
        parameterList = ', '.join(['?' for _argumentValue in self.procedureArgumentValues])
        return f'SELECT * FROM {self.procedureSchema}.{self.procedureName} ({parameterList})'
    
    def executeAndFetchAll(self, connector: odbcConnector) -> List[Row]:        
        """
        Note: Cursor rowcount property does not show a valid count untill fetchall has been run. 
        """        
        DebugPrinter.Msg(f'Fetching data from TVF: {self.procedureSchema}.{self.procedureName}', DebugLevel.Verbose)

        sqlCommand = self.getSqlCommand()
        DebugPrinter.Msg(f'Using sql command: {sqlCommand}   \n with arguments: {self.procedureArgumentValues}', DebugLevel.Maximal)
        connector.Cursor.execute(sqlCommand, self.procedureArgumentValues)

        # Check if the cursor has any description (columns)
        if not connector.Cursor.description:
            DebugPrinter.Msg(f'No columns in the result set.', DebugLevel.Warnings)
            return []
        else:
            DebugPrinter.Msg(f'TVF description returned: {connector.Cursor.description}', DebugLevel.Maximal)

        tempresult = connector.Cursor.fetchall()
        if not tempresult:
            DebugPrinter.Msg('No results returned from the TVF.', DebugLevel.Warnings)
            emptyList: List[Row] = []
            return emptyList
        return tempresult
    
class SqlScalarValuedFunction(SqlCommand):
    """
    Example usage:
    proc = SqlScalarValuedFunction('MySVF', 'dbo', ['arg1', 'arg2', 'arg3'])
    print(proc.getSqlCommand())
    """ 
    def getSqlCommand(self) -> str:
        parameterList = ', '.join(['?' for _argumentValue in self.procedureArgumentValues])
        return f'SELECT {self.procedureSchema}.{self.procedureName}({parameterList})'
    
    def executeAndFetchAll(self, connector: odbcConnector) -> List[Row]:
        """
        This method is not applicable for scalar-valued functions and raises a NotImplementedError.

        :param connector: The ODBC connector used to execute the SQL command.
        :raises NotImplementedError: Always raised because fetching multiple rows is not possible for scalar functions.
        :return: This method does not return.
        """
        raise NotImplementedError("Scalar-valued functions do not return multiple rows.")
    
    def executeAndFetchScalar(self, connector: odbcConnector) -> Any:
        """
        Execute the scalar function and return a single value.
        """
        sqlCommand = self.getSqlCommand()
        DebugPrinter.Msg(f'Executing scalar-valued function: {sqlCommand} with arguments: {self.procedureArgumentValues}', DebugLevel.Verbose)

        connector.Cursor.execute(sqlCommand, self.procedureArgumentValues)
        result = connector.Cursor.fetchone()

        if result is None:
            DebugPrinter.Msg(f'No result returned from the scalar function.', DebugLevel.Warnings)
            return None
        else:
            DebugPrinter.Msg(f'Scalar function returned: {result[0]}', DebugLevel.Maximal)
            return result[0]