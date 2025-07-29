"""soil.decorator package."""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union


def decorator(depth: Optional[int] = None) -> Callable:
    """Decorator of decorators. It allows to serialize a
    decorator that is not fully executed.

    If the decorated function is executed with __show_calls it will return the lists
    of args and kwargs that ran until that moment.

    When the function is fully executed it will run normally.

    Attributes
    ----------
        depth: The number of times the decorator will return a function.

    """
    if depth is None:
        raise ValueError("The depth of the decorator must be specified.")

    def wrapper(actual_decorator: Callable) -> Callable:
        def wrapper_logger_fn(
            args_list: List[Tuple[Any, ...]], kwargs_list: List[Dict[Any, Any]]
        ) -> Callable:
            def arg_logger_fn(
                *args: Any, __show_calls: bool = False, **kwargs: Any
            ) -> Union[
                Callable, Tuple[Callable, List[Tuple[Tuple[Any, ...], Dict[Any, Any]]]]
            ]:
                if __show_calls:
                    return (actual_decorator, list(zip(args_list, kwargs_list)))
                new_args_list = [*args_list, args]
                new_kwargs_list = [*kwargs_list, kwargs]
                if depth == len(args_list):
                    # if depth is 0 it will run the function normally.
                    res = actual_decorator
                    for args, kwargs in zip(new_args_list, new_kwargs_list):  # noqa: PLR1704
                        res = res(*args, **kwargs)
                    return res
                return wrapper_logger_fn(new_args_list, new_kwargs_list)

            return arg_logger_fn

        return wrapper_logger_fn([], [])

    return wrapper
