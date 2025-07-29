
# Third-party library imports
import numpy as np  # Third-party library import
import time # Third-party library import

# Local application / library-specific imports
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # For parallel processing
from csa_common_lib.toolbox import _notifier # For notification handling
from csa_common_lib.toolbox.concurrency.parallel_helpers import get_results_progress

def run_tasks_local(inputs, dispatcher, max_workers:int, notifier):
    """
    Generic function to run parallel tasks using the provided dispatcher.

    Parameters
    ----------
    inputs : list of tuples
        List of arguments to be passed to the dispatcher function.
    dispatcher : callable
        The dispatcher function that will handle each task.
    max_workers : int
        Maximum number of workers to use in the ProcessPoolExecutor.
    notifier : object
        Notifier object to manage notifications and state.

    Returns
    -------
    yhat : ndarray
        Aggregated prediction outcomes.
    yhat_details : list
        List of detailed model results.
    """
    
    
    # Get the current notifier state and disable the notifier
    n_state = notifier.get_notifier_status()
    notifier.disable_notifier()

    # Execute tasks in multi-threaded pool
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(dispatcher, inputs))

    # Restore notifier state
    notifier.set_notifier_status(n_state)

    # Unpack yhat results
    yhat = np.vstack([result[0] for result in results])

    # Unpack output_details results using list comprehension
    yhat_details = [result[1] for result in results]

    return yhat, yhat_details


def run_tasks_api(inputs, dispatcher, get_results_dispatcher, max_workers:int, notifier):
    """
    Generic function to run parallel tasks using the 
    provided dispatcher for CSA API calls.

    Parameters
    ----------
    inputs : list of tuples
        List of arguments to be passed to the dispatcher function.
    dispatcher : callable
        The dispatcher function that will handle each task.
    get_results_dispatcher : callabale
        The dispatcher function that will retrieve results from the API.
    max_workers : int
        Maximum number of workers to use in the ProcessPoolExecutor.
    notifier : object
        Notifier object to manage notifications and state.

    Returns
    -------
    yhat : ndarray
        Aggregated prediction outcomes.
    yhat_details : list
        List of detailed model results.
    """
    
    
    # Get the current notifier state and disable the notifier
    n_state = notifier.get_notifier_status()
    notifier.disable_notifier()

    # Execute tasks in multi-threaded pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        jobs = list(executor.map(dispatcher, inputs))

    # Unpack job_id and job_code using list comprehension
    job_id, job_code = zip(*jobs)
    
 
    # Set timeout to 15 minutes (15 * 60 seconds)
    TIMEOUT = 15 * 60  # 15 minutes in seconds

    inputs_for_get = [
        (job_id[q], job_code[q]) for q in range(len(jobs))
    ]

    # Create boolean array to track processing jobs.
    processing_jobs = [True] * len(inputs_for_get)

    completed_results = [None] * len(inputs_for_get)

    failed_jobs = 0

    # Track the start time
    start_time = time.time()

    while True in processing_jobs:
        # Dispatch the get_results task in a multi-threaded pool
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Update the inputs
            active_indices = [i for i in range(len(inputs_for_get)) if processing_jobs[i] == True]

            # Submit tasks to the executor
            future_to_index = {executor.submit(get_results_dispatcher, inputs_for_get[i]): i for i in active_indices}
            
            for future in future_to_index:
                index = future_to_index[future]
                try:
                    # Wait for the result with a timeout
                    result = future.result(timeout=TIMEOUT)

                    detail_keys = result[1].keys()

                    # If a yhat is returned or an error is reported mark as completed
                    if result[0] is not None or 'error' in detail_keys:  
                        # Update job to completed
                        processing_jobs[index] = False
                        # Save completed result
                        completed_results[index] = result
                        
                        # increment failed jobs tracker
                        if 'error' in detail_keys:
                            failed_jobs += 1

                except TimeoutError:
                    print(f"Job {index} timed out after {TIMEOUT / 60} minutes.")
                    processing_jobs[index] = False
                    completed_results[index] = None
                except Exception as e:
                    print(f"Error processing job {index}: {str(e)}")
                    # Optionally handle other errors here
                    processing_jobs[index] = False
                    completed_results[index] = None
            
                # Print status after each iteration
                get_results_progress(processing_jobs=processing_jobs, failed_jobs=failed_jobs)

        # Check if the total passes timeout cutoff
        if time.time() - start_time > TIMEOUT:
            print("\n15 minutes have passed. Exiting.")
            break
    
    print("\n")

    # restore notifier state
    _notifier.set_notifier_status(n_state)

    # Unpack yhat results
    yhat = np.vstack([result[0] for result in completed_results])
    
    # Unpack output_details results using list comprehension
    yhat_details = [result[1] for result in completed_results]

    # Return results
    return yhat, yhat_details