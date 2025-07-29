"""Package for soil.task"""

from typing import Any, Callable, List

from soil.data_structure import DataStructure


def task(modulified_module: Callable) -> Callable:
    """Decorates a modulified module in soil. This function is to call
    soil modules from other soil modules.

    Example:
    -------
        task(my_module)(data, arg1='val1')

    """

    def decorator(*args: DataStructure, **kwargs: Any) -> List[DataStructure]:
        return modulified_module(*args, **kwargs)

    return decorator


def task_wait(futures: Any) -> Any:
    """Wait until computation completes and gather results.

    Accepts a future, nested container of futures, iterator, or queue.
    The return type will match the input type.

    Example:
    -------
        result = tasks_wait([future1, future2])

    """
    return futures
