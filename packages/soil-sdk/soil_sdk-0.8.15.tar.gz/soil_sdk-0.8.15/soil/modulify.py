#  pylint:disable=unused-argument
"""Module that defines the @modulify decorator."""

import warnings
from functools import wraps
from types import GenericAlias
from typing import Callable, TypeVar, cast, get_args

from soil.data_structure import DataStructure
from soil.decorator import decorator
from soil.pipeline import Pipeline
from soil.utils import generate_data_structure_ids, generate_transformation

_IterableGenericDataStructure = TypeVar(
    "_IterableGenericDataStructure", bound=["list", "tuple"]
)


def _omittable_parentheses[**T](
    maybe_decorator: Callable[T, _IterableGenericDataStructure] | None = None,
    /,
    allow_partial: bool = False,
) -> Callable[T, _IterableGenericDataStructure]:
    # https://gist.github.com/oakkitten/03ca8f9c1113a7e32e32135e2cf5fef9
    def _decorator(func):
        @wraps(func)
        def wrapper(*args: T.args, **kwargs: T.kwargs):
            if allow_partial:
                if args and callable(args[-1]):
                    *args, fu = args  # pylint:disable=invalid-name
                    return func(*args, **kwargs)(fu)
            elif len(args) == 1 and callable(args[-1]) and not kwargs:
                return func()(args[0])
            return func(*args, **kwargs)

        return wrapper

    return _decorator if maybe_decorator is None else _decorator(maybe_decorator)


@_omittable_parentheses(allow_partial=True)
@decorator(depth=2)
def modulify[**T](
    _func: Callable[T, _IterableGenericDataStructure] | None = None,
    *,
    output_types: Callable | None = None,
) -> Callable[T, _IterableGenericDataStructure]:
    """Decorates a function to mark it as a soil module."""

    def modulify_decorator(
        fn: Callable[T, _IterableGenericDataStructure],
    ) -> Callable[T, _IterableGenericDataStructure]:
        fnn = fn if _func is None else _func
        num_outputs = fnn.__annotations__.get("return", None)

        mod_name = fnn.__module__ + "." + fnn.__name__

        def decorated(
            *inputs: T.args, **kwargs: T.kwargs
        ) -> _IterableGenericDataStructure:
            num_outputs_in = None
            if output_types is not None:
                # WARNING this could fail if output_types() checks the type of *inputs
                num_outputs_in = len(output_types(*inputs, **kwargs))
                warnings.warn(
                    "output_types is deprecated use annotations on function return instead.",
                    DeprecationWarning,
                )
            if (
                isinstance(num_outputs, GenericAlias)
                and num_outputs.__origin__ == tuple  # noqa: E721
            ):
                num_outputs_in = len(get_args(num_outputs))
            if num_outputs_in is None:
                raise ValueError(
                    "@modulify: "
                    + mod_name
                    + " missing return annotation of decorated function "
                    "or annotation not instance of tuple."
                )

            input_pipes = [
                input.pipeline for input in inputs if input.pipeline is not None
            ]
            new_pipeline = Pipeline.merge_pipelines(*input_pipes)
            output_ids = generate_data_structure_ids(mod_name, num_outputs_in)
            input_ids = [d.id if d.id is not None else d.sym_id for d in inputs]
            for i in input_ids:
                assert isinstance(i, str)
            transformation = generate_transformation(
                input_ids=cast(list[str], input_ids),
                output_ids=output_ids,
                fn_name=mod_name,
                args=kwargs,
            )
            new_pipeline = new_pipeline.add_transformation(transformation)
            outputs = [
                DataStructure(sym_id=sym_id, pipeline=new_pipeline)
                for sym_id in output_ids
            ]
            return outputs

        return decorated

    if _func is None:
        return modulify_decorator
    return modulify_decorator(_func)
