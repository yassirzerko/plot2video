import logging
import functools 
import os  

def get_logger(filename):
    """
    Set up and get a logger, the associated log file : logger_name.log.

    Args:
        filename (str): The name of the file.

    Returns:
        logging.Logger: The configured logger object.
    """

    LOG_FOLDER_PATH = 'logging_output'
    logger_name = os.path.basename(filename)
    logger = logging.getLogger(logger_name) 
    logger.setLevel(logging.INFO)  

    # Create a file handler that logs to a file named after the module
    log_file_name = f"{logger_name}.log"  
    file_handler = logging.FileHandler(os.path.join(LOG_FOLDER_PATH, log_file_name))
    file_handler.setLevel(logging.INFO)

    # Create a console handler for output to console
    console_handler = logging.StreamHandler() 
    console_handler.setLevel(logging.INFO) 

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)  

    # Add the handlers to the logger
    logger.addHandler(file_handler) 
    logger.addHandler(console_handler)  

    return logger 

def log_function_call(logger):
    """
    Decorator for logging function calls, inputs, and outputs.

    Args:
        logger (logging.Logger): The logger object to be used for logging.

    Returns:
        function: Decorator function for logging function calls.
    """
    def decorator(wrapped_fun):
        @functools.wraps(wrapped_fun)
        def wrapper(*args, **kwargs):
            # Log function input
            logger.info(f"\n Called function: {wrapped_fun.__name__}")
            logger.info(f"Input arguments: args={args}, kwargs={kwargs}") 

            # Call the original function
            result = wrapped_fun(*args, **kwargs)

            # Log function output
            logger.info(f"Output: {result} \n")

            return result
        return wrapper
    return decorator