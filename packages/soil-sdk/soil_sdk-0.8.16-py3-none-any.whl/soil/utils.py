"""Module that defines some useful functions"""

from typing import Any, Callable, Dict, List
from uuid import uuid4

from pandas import Timestamp


def _isalambda(value: Any) -> bool:
    return callable(value) and value.__name__ == "<lambda>"


def generate_data_structure_ids(fn_name: str, quantity: int) -> List[str]:
    """Generates an id for a datastructure"""
    rnd = str(uuid4())
    return [
        fn_name.replace(".", "/") + "-" + str(rnd) + "-" + str(i)
        for i in range(quantity)
    ]


def build_function(function: Callable) -> Dict[str, Any]:
    """Mounts the argument structure to serialize a function. It uses the reserved dict key
    `__soil_arg_type` to mark a function. The function code must be inside modules or
    data_structures folders.
    It recognises 3 types of functions:
        * Named functions: `__soil_arg_type='function'` functions with a module
            and a name.
        * Lambda functions: `__soil_arg_type='lambda'` They are not actually serialized
            but kept as a placeholder for the pattern matching in the server.
            They can only be used as a decorator parameter.
        * Decorated functions: `__soil_arg_type='decorated'` A function that has been
            decorated with one or more decorators that have been decorated with
            soil.decorator or functions returned by that decorated function.
    """
    first_qual = function.__qualname__.split(".")[0]
    if function.__module__ == "soil.decorator" and first_qual == "decorator":
        wrapped, calls = function(__show_calls=True)
        return {
            "__soil_arg_type": "decorated",
            "module": wrapped.__module__,
            "name": wrapped.__name__,
            "calls": [
                {
                    "args": [build_arguments(arg) for arg in call[0]],
                    "kwargs": build_arguments(call[1]),
                }
                for call in calls
            ],
        }

    if _isalambda(function):
        return {"__soil_arg_type": "lambda"}

    return {
        "__soil_arg_type": "function",
        "module": function.__module__,
        "name": function.__name__,
    }


def build_arguments(args: Any) -> Any:
    """Transforms the module arguments into serializable arguments"""
    if isinstance(args, dict):
        return {key: build_arguments(value) for (key, value) in args.items()}

    if isinstance(args, list):
        return [build_arguments(value) for value in args]

    if callable(args):
        return build_function(args)

    if isinstance(args, Timestamp):
        additional_kwargs = {}
        if (
            args.tzinfo
            and hasattr(args.tzinfo, "zone")
            and args.tzinfo.zone is not None
        ):
            additional_kwargs = {"tz": args.tzinfo.zone}
        return {
            "_object": Timestamp.__name__,
            "_constructor_params": {
                "positional_args": [args.isoformat()],
                "keywords_args": {**additional_kwargs},
            },
        }

    return args


def generate_transformation(
    input_ids: List[str], output_ids: List[str], fn_name: str, args: Dict[str, Any]
) -> Dict[str, Any]:
    """Mounts the dictionary for a module in a plan"""
    tid = fn_name + "-" + str(uuid4())

    return {
        "id": tid,
        "module": fn_name,
        "inputs": input_ids,
        "outputs": output_ids,
        "args": build_arguments(args),
    }
