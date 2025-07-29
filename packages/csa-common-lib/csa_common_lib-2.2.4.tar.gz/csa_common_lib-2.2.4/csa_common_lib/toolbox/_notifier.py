import os
import sys


# Global variable _counter for internal indefinite progress use
_counter = 0
_cache_msg = None


def task_update(status_msg:str=None, current_iter:int=None, total_iter:int=None, is_done=False):
    """Displays progress for iterative tasks items, followed by a line break.

    Parameters
    ----------
    status_msg : str
        Status update message string.
    current_iter : int, optional
        Current task number, by default None
    total_iter : int, optional
        Total task count, by default None
    is_done : bool, optional
        Logical to indicate completion, by default False
    """    
    
    if is_notifier_enabled():
        
        # Global variable the message (cache)
        global _cache_msg
        
        if status_msg is not None:
            # Update status_msg
            _cache_msg = status_msg
        
        # Hide the cursor
        hide_cursor()
        
        # Construct task iteration status message
        iter_msg = ''
        if current_iter is not None and total_iter is not None:
            iter_msg = f" [{current_iter} of {total_iter}]"

        
        # Write to console
        if is_done:
            sys.stdout.write(f"{_cache_msg} [done]      \n")
        else:
            sys.stdout.write(f"{_cache_msg}{iter_msg}\r")
        sys.stdout.flush()
    
        # Revert to showing the cursor
        show_cursor()


def display_progress(current_iter:float, total_iter: float, 
                     status_msg: str = 'Processing, please wait...', 
                     is_done=False):
    """Shows progress status given a current iteration out of a total
    known iteration.

    Parameters
    ----------
    current_iter : float
        Current counter toward progress of task.
    total_iter : float
        Total counter for progress of task.
    status_msg : str, optional
        Progress message string, by default 'Processing, please wait...'
    is_done : bool, optional
        Logical to indicate when progress is completed.
    """
    
    if is_notifier_enabled():
        # Calculate the current iteration progress
        progress = round((current_iter / total_iter) * 100)
        
        # Construct the message
        if is_done:
            sys.stdout.write(f"{status_msg} [done]      \n")
        else:
            sys.stdout.write(f"{status_msg} [{progress}%] ")
            sys.stdout.write("\r")  # Move the cursor back to the beginning of the line
        
        # Flush the buffer to ensure it's displayed immediately
        sys.stdout.flush()  
    
    
def display_processing(status_msg: str = 'Processing, this may take a few minutes', 
                       is_done=False):
    """Shows indeterminant progress status, where the time to completion is unknown.

    Parameters
    ----------
    status_msg : str, optional
        Message string, by default 'Processing, this may take a few minutes'
    is_done : bool, optional
        Logical to indicate when progress is completed.
    """
    
    if is_notifier_enabled():
        if status_msg is None:
            status_msg = "Processing, this may take a few minutes"
        
        # Use the global variable _counter
        global _counter
        
        # Calculate the current iteration progress
        _dots = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        _points = ["∙∙∙∙∙","●∙∙∙∙","∙●∙∙∙","∙∙●∙∙","∙∙∙●∙","∙∙∙∙●","∙∙∙∙∙","∙∙∙∙●","∙∙∙●∙","∙∙●∙∙","∙●∙∙∙","●∙∙∙∙"]
        
        symbol = _points
        
        # Construct the message
        if is_done:
            sys.stdout.write(f"{status_msg} [done]     \n")
        else:
            sys.stdout.write(f"{status_msg} {symbol[_counter]}")
            
        _counter = _counter + 1
        if _counter >= len(symbol):
            _counter = 0 # reset to zero
        
        # Flush the buffer to ensure it's displayed immediately
        sys.stdout.flush()  
        sys.stdout.write("\r")  # Move the cursor back to the beginning of the line
    

def hide_cursor():
    """Hides the cursor in the terminal.
    """    
    sys.stdout.write("\033[?25l")  # Hide cursor
    sys.stdout.flush()


def show_cursor():
    """Shows the cursor in terminal.
    """    
    sys.stdout.write("\033[?25h")  # Show cursor
    sys.stdout.flush()
    
    
def is_notifier_enabled():

    return get_notifier_status() == 'True'


def get_notifier_status():
    
    # Defaults to true if user does not specify to prevent system failure
    return os.environ.get('CSA_CONSOLE_NOTIFIER', 'False').capitalize()
    
    
def set_notifier_status(is_enable:bool=True):
    os.environ['CSA_CONSOLE_NOTIFIER'] = 'True' if is_enable else 'False'


def enable_notifier():
    set_notifier_status(True)
    
    
def disable_notifier():
    set_notifier_status(False)
    
    
if __name__ == "__main__":
    
    hide_cursor()
    # Test the display_progress function
    for k in range(101):
        display_progress(k, 100)
        import time
        time.sleep(0.1)
        
    show_cursor()