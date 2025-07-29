from enum import Enum
from queue import Queue, Empty
from typing import NamedTuple, Dict
import threading
import time

class DebugLevel(Enum):
    Disabled        = 0
    Critical        = 1    
    Warnings        = 2
    Informational   = 3
    Verbose         = 4
    Maximal         = 5

class DebugPrinter:    
    """
    A utility class for printing debug messages with configurable levels, threading safety, and message formatting.

    Attributes:
        DebugLevel (DebugLevel): Determines which debug messages are printed based on their importance.
        ThreadSafe (bool): If True, messages are added to a queue for thread-safe printing.
        Colorized (bool): If True, messages are printed with colored HTML spans.
        PrintInterval (int): Interval in seconds between HTML message displays.
        config_Lock (threading.Lock): Lock to ensure thread-safe configuration updates.
        msgQueue (Queue): Queue to hold messages for thread-safe printing.
        writerEnabled (bool): Indicates whether the log writer thread is active.
        writerEnabled_lock (threading.Lock): Lock for managing the log writer thread state.
        printerFinished (bool): Indicates if the printer thread has finished processing all messages.
        msgQueueThread (threading.Thread): The thread handling message queue printing.

    Methods:
        Configure(debugLevel, threadSafe, colorized, printInterval):
            Configures the debug printer settings and clears the message queue.

        Msg(message, debugLevel):
            Prints a message if the specified debug level meets the current settings.

        EnableLogWriter():
            Enables the background log writer thread for processing the message queue.

        DisableLogWriter():
            Disables the log writer thread and ensures all messages are processed before stopping.

        msgQueuePrinter():
            Continuously processes the message queue for printing messages.
    """

    class __QueueMessage(NamedTuple):
        """
        A simple container for a debug message to be processed by the DebugPrinter.

        Attributes:
            message (str): The message to be printed. Defaults to an empty string.
            debugLevel (DebugLevel): The severity level of the message. Defaults to DebugLevel.Disabled.
            Colorized (bool): Whether the message should be colorized in HTML. Defaults to False.
        """
        message: str = ""
        debugLevel: DebugLevel = DebugLevel.Disabled
        Colorized: bool = False

    # Set this property to determine which messages are printed and which arent. 
    __DebugLevel: DebugLevel = DebugLevel.Disabled
    # Set this bool to determine whether messages are printed directly (not safe for multithreading)
    # , or whether they are added to a queue for printing one by one. 
    __ThreadSafe: bool = False
    # Set this bool to determine whether messages are printed in color (ANSI), or plain text.
    __Colorized: bool = True
    # Determines how often messages are displayed, value in seconds.
    __PrintInterval: int = 3

    # Make sure messages are using the new config when there is one. 
    __config_Lock: threading.Lock = threading.Lock()

    __msgQueue: Queue[__QueueMessage] = Queue()

    __defaultColorAnsi: str = "\033[0m"

    # A dictionary mapping DebugLevel values to corresponding color codes for visual representation.
    __switch: Dict[Enum, str] = {
        DebugLevel.Critical:        "\033[91m",                     # Red (#FF0000)
        DebugLevel.Warnings:        "\033[38;2;255;165;0m",         # Orange (#FFA500)
        DebugLevel.Informational:   "\033[38;2;217;201;59m",        # Yellow (#d9c93b)
        DebugLevel.Verbose:         "\033[38;2;86;207;0m",          # Green (#56cf00)
        DebugLevel.Maximal:         "\033[38;2;49;178;204m",        # Light Blue (#31b2cc)
        DebugLevel.Disabled:        "\033[0m"                       # Default
    }

    @staticmethod
    def GetCurrentDebugLevel():
        return DebugPrinter.__DebugLevel

    @staticmethod
    def Configure(debugLevel: DebugLevel = DebugLevel.Disabled, threadSafe: bool = True, colorized: bool = False, printInterval: int = 0): 
        with DebugPrinter.__config_Lock:
            DebugPrinter.__DebugLevel = debugLevel
            DebugPrinter.__ThreadSafe = threadSafe
            DebugPrinter.__Colorized = colorized
            if printInterval > 0:
                DebugPrinter.__PrintInterval = printInterval 
            
            while not DebugPrinter.__msgQueue.empty():
                time.sleep(0.1)          

    @staticmethod
    def Msg(message: str, debugLevel: DebugLevel):
        """
        Prints the message if the debugLevel for this message is fits the debug setting for the debugPrinter.

        Example usage:
        DebugPrinter.DebugLevel = DebugLevel.Maximal
        DebugPrinter.Msg('Test warning message', DebugLevel.Warnings)
        """
        try:
            # Load config into memory for this msg execution and ensure they are not attached to previous messages.
            with DebugPrinter.__config_Lock:                
                localDebugLevel: DebugLevel = DebugPrinter.__DebugLevel
                localThreadSafe: bool = DebugPrinter.__ThreadSafe
                localColorized: bool = DebugPrinter.__Colorized

                if localDebugLevel.value == DebugLevel.Disabled.value:
                    return            
                if localDebugLevel.value >= debugLevel.value: # Check whether the message importance is equal or higher than the configured value.
                    if localThreadSafe:                    
                        DebugPrinter.EnableLogWriter()
                        queueMessage = DebugPrinter.__QueueMessage(message, debugLevel, localColorized)
                        DebugPrinter.__msgQueue.put(queueMessage)         
                    else: 
                        if localColorized:
                            msgColor = DebugPrinter.__switch.get(debugLevel, DebugPrinter.__defaultColorAnsi) 
                            Print_colored_message(message, color=msgColor)  
                        else:                                  
                            print(message)
                    #TO-DO: 
                    #if __printToFile:
                    #    printToFile(message)                    
                else: 
                    # We won't print this message because the config is set to only print more important messages.
                    pass
        except Exception as e:
            print(str(e))

    __writerEnabled: bool = False
    __writerEnabled_lock: threading.Lock = threading.Lock()   
    __msgQueueThread: threading.Thread
    __printerFinished: bool = False

    @staticmethod
    def EnableLogWriter() -> None:
        with DebugPrinter.__writerEnabled_lock:            
            if DebugPrinter.__writerEnabled:
                return
            else:            
                DebugPrinter.__writerEnabled = True
                DebugPrinter.__msgQueueThread = threading.Thread(target=DebugPrinter.__msgQueuePrinter)
                DebugPrinter.__msgQueueThread.start()                

    # TO-DO:
    # @staticmethod
    #def printToFile(message: str):
    #    try:
    #        with open('debug.log', 'a') as f:
    #            f.write(message)
    #    except Exception as e:
    #        print(str(e))

    @staticmethod
    def DisableLogWriter() -> None:        
        with DebugPrinter.__config_Lock: # No updates should be taking place
            with DebugPrinter.__writerEnabled_lock: # No new messages should be written
                if DebugPrinter.__writerEnabled: # If we are already disabled, this has no point.
                    DebugPrinter.__writerEnabled = False
                    while not DebugPrinter.__msgQueue.empty(): # We are enabled so we can wait untill the queue is empty.
                        time.sleep(0.1)
                    DebugPrinter.__msgQueue.join()
                    if DebugPrinter.__msgQueueThread:
                        DebugPrinter.__msgQueueThread.join()

    @staticmethod
    def __msgQueuePrinter():        
        # Always only one of these.
        DebugPrinter.__printerFinished = False
        combinedMessage: str = ''
        try:            
            last_print_time = time.time()            
            while DebugPrinter.__writerEnabled:
                try:
                    msg: DebugPrinter.__QueueMessage = DebugPrinter.__msgQueue.get(timeout=0.5)
                    if msg.Colorized:
                        current_time = time.time()
                        msgColor = DebugPrinter.__switch.get(msg.debugLevel, DebugPrinter.__defaultColorAnsi) 
                        combinedMessage += f"{msgColor}{msg.message}\033[0m \r\n"                     
                        if current_time - last_print_time >= DebugPrinter.__PrintInterval: # Interval between showing HTML messages in seconds
                            last_print_time = time.time()          
                            print(combinedMessage)
                            combinedMessage = ''
                        elif len(combinedMessage) > 10000:
                            last_print_time = time.time()          
                            print(combinedMessage)
                            combinedMessage = ''
                    else:                                  
                        print(msg.message)
                    DebugPrinter.__msgQueue.task_done()
                except Empty:
                    pass
            while not DebugPrinter.__msgQueue.empty():
                msg: DebugPrinter.__QueueMessage = DebugPrinter.__msgQueue.get_nowait()
                if msg.Colorized:
                    msgColor = DebugPrinter.__switch.get(msg.debugLevel, DebugPrinter.__defaultColorAnsi) 
                    combinedMessage += f"{msgColor}{msg.message}\033[0m \r\n"
                else:
                    combinedMessage += f"{msg.message} \r\n"
                    print(msg.message)
                DebugPrinter.__msgQueue.task_done()
                if len(combinedMessage) > 10000:
                    print('printing due to message length: ')
                    print(combinedMessage)
                    combinedMessage = ''
            if combinedMessage != '':
                print(combinedMessage)
        except Exception as e:
            print(e)
        finally:
            DebugPrinter.__printerFinished = True

def __colored_message(message: str, color:str='black') -> str:
    """
    Generates the ansi colored string that is required for printing a message in a specified color in a Databricks notebook.
    """
    return f"{color}{message}\033[0m"   

def Print_colored_message(message: str, color:str='\033[0m') -> None:
    """
    Prints a message in a specified color using ANSI Escape codes in a Databricks notebook.
    
    :param message: The message to display
    :param color: The color of the message text.
    """
    print(__colored_message(message, color))    
