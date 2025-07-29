import random
import string
import requests
import logging
import time
import functools


def list_functions(module, verbose=False):
    """
    ============================
    List Functions Utility
    ============================

    This function lists all callable functions within a given module. If verbose is set to True, it also prints the docstring of each function.

    :param module: The module to list functions from.
    :type module: module

    :param verbose: If True, prints the docstring of each function. Default is False.
    :type verbose: bool, `optional`

    :returns: None

    **Example Usage**
    -----------------
    .. code-block:: python

        list_functions(some_module, verbose=True)

    **See Also**
    ------------
    - `dir <https://docs.python.org/3/library/functions.html#dir>`_
    - `callable <https://docs.python.org/3/library/functions.html#callable>`_
    """
    if verbose:
        for name in dir(module):
            if callable(getattr(module, name)):
                func = getattr(module, name)
                print(f"Function: {name}\nDocstring: {func.__doc__}")
    else:
        for name in dir(module):
            if callable(getattr(module, name)):
                print(name)


def flatten_list(nested_list):
    """
    =============================
    Flatten List Utility
    =============================

    This function takes a nested list and returns a flat list containing all the elements.

    :param nested_list: The nested list to be flattened.
    :type nested_list: list

    :returns: A flat list containing all the elements of the nested list.
    :rtype: list

    **Example Usage**
    -----------------
    .. code-block:: python

        nested_list = [1, [2, [3, 4], 5], 6]
        flat_list = flatten_list(nested_list)
        print(flat_list)  # Outputs [1, 2, 3, 4, 5, 6]

    **See Also**
    ------------
    - `list <https://docs.python.org/3/library/stdtypes.html#list>`_
    """
    flat = []
    for item in nested_list:
        if isinstance(item, list):
            flat.extend(flatten_list(item))
        else:
            flat.append(item)
    return flat


def generate_random_string(length=8):
    """
    =============================
    Random string Utility
    =============================

    This function generates a random string of `n` length.

    :param length: The length of returned random string.
    :type length: int, `optional`

    :returns: A string of `n` length.
    :rtype: str

    **Example Usage**
    -----------------
    .. code-block:: python

            result = generate_random_string(8)
            print(result)  # 'aBcD3eF4'
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def send_ntfy(message: str, topic: str):
    """
    =============================
    Send Notification Utility
    =============================

    This function sends a notification message to a specified topic using the ntfy.sh service.

    :param message: The notification message to be sent.
    :type message: str
    :param topic: The topic to which the notification will be sent.
    :type topic: str

    :returns: None

    **Example Usage**
    -----------------
    .. code-block:: python

            send_ntfy("Hello, World!", "my_topic")
    ```
    """
    url = f"https://ntfy.sh/{topic}"
    response = requests.post(url, data=message.encode("utf-8"))
    if response.status_code == 200:
        return
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")


def setup_logger(name, log_file, level=logging.INFO):
    """
    =============================
    Logger Setup Utility
    =============================
    This function sets up and returns a logger instance with a specified name, log file, and logging level.
    The logger writes log messages to the specified file in a formatted manner.
    :param name: The name of the logger.
    :type name: str
    :param log_file: The file path where log messages will be written.
    :type log_file: str
    :param level: The logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.
    :type level: int
    :returns: A configured logger instance.
    :rtype: logging.Logger
    **Example Usage**
    -----------------
    .. code-block:: python
            logger = setup_logger("my_logger", "app.log", logging.DEBUG)
            logger.info("This is an info message.")
    """
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """
    =============================
    Retry Decorator
    =============================
    This decorator retries the execution of a function a specified number of times
    with a delay between attempts if an exception is raised.
    :param max_attempts: The maximum number of retry attempts. Defaults to 3.
    :type max_attempts: int
    :param delay: The delay (in seconds) between retry attempts. Defaults to 1.
    :type delay: int
    :param exceptions: A tuple of exception classes that should trigger a retry. Defaults to (Exception,).
    :type exceptions: tuple
    :returns: The result of the decorated function if it succeeds within the allowed attempts.
    :raises: The last exception raised if the maximum number of attempts is reached.
    **Example Usage**
    -----------------
    .. code-block:: python
        @retry(max_attempts=5, delay=2)
        def fragile_operation():
            i = random.randint(0, 10)
            if i <= 1:
                return "Operation succeeded!"
            print(f"Attempt failed with i={i}. Retrying...")
            raise ValueError("Simulated failure")
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    time.sleep(delay)
                    if attempts == max_attempts:
                        raise

        return wrapper

    return decorator
