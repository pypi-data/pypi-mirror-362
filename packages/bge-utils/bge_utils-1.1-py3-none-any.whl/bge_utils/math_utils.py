import math


def mean_and_stddev(numbers):
    """
    =============================
    Mean and Standard Deviation Utility
    =============================

    This function calculates the mean and standard deviation of a list of numbers.

    :param numbers: The list of numbers to calculate the mean and standard deviation for.
    :type numbers: list of float

    :returns: A tuple containing:

        - **mean** → The mean of the numbers
        - **stddev** → The standard deviation of the numbers
    :rtype: tuple

    **Example Usage**
    -----------------
    .. code-block:: python

        result = mean_and_stddev([1, 2, 3, 4, 5])
        print(result)  # (3.0, 1.4142135623730951)
        print(result[0])  # 3.0

    **See Also**
    ------------
    - `Standard Deviation Reference <https://en.wikipedia.org/wiki/Standard_deviation>`_
    """
    mean = sum(numbers) / len(numbers)
    stddev = math.sqrt(sum((x - mean) ** 2 for x in numbers) / len(numbers))
    return mean, stddev
