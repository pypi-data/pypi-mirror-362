from typing import List, Tuple, Union

def createWidgets(widgetList: List[Tuple[str, str]]) -> None:
    """
    Creates widgets based on the provided list of tuples.

    Args:
    widgetList (List[Tuple]): A list of tuples where each tuple contains:
        - A string (widget name) representing the name of the widget.
        - A string (default value) representing the default value to be assigned to the widget.
    """
    for widget in widgetList:
        addWidget(widget)

def addWidget(widget: Union[Tuple[str, str], str], defaultValue: str = "") -> None:
    """
    Adds a text widget. Can accept either a tuple or separate arguments.

    Args:
    widget (Union[Tuple[str, str], str]): If a tuple is provided, it should contain:
        - A string (widget name) representing the name of the widget.
        - A string (default value) representing the default value.
        If a string is provided, it is treated as the widget name.
    defaultValue (str): The default value for the widget, only used if `widget` is a string.
    """
    if isinstance(widget, tuple):
        dbutils.widgets.text(widget[0], defaultValue=widget[1])
    elif isinstance(widget, str):
        dbutils.widgets.text(widget, defaultValue=defaultValue)
    else:
        raise TypeError("widget must be either a tuple (name, value) or a string with a default value.")

def removeWidget(widgetName: str) -> None:
    """
    Removes a widget by its name.

    Args:
    widgetName (str): The name of the widget to be removed.
    """
    dbutils.widgets.remove(widgetName)

def clearWidgets() -> None:
    """
    Removes all widgets.
    """
    dbutils.widgets.removeAll()

def getWidget(widgetName: str) -> str:
    """
    Retrieves the value of a widget by its name.

    Args:
    widgetName (str): The name of the widget to retrieve the value for.
    
    Returns:
    str: The value of the widget, always as a string.
    """
    return dbutils.widgets.get(widgetName)
