import functools
from collections.abc import Callable
from typing import Protocol, TypeVar

__all__ = [
    "identity",
    "composable",
    "singleton",
    "memorized",
    "lazy",
    "unique_returns",
]

T = TypeVar("T")
U = TypeVar("U")
RT = TypeVar("RT")


def identity(instance: T) -> T:
    """
    Returns the input ``instance`` unchanged. This is a utility function often used as a default or placeholder.

    :param instance: The value to return.
    :return: The same value as provided in ``instance``.
    """
    return instance


class Composable(Protocol[T, RT]):
    """
    Protocol for composable callables, supporting composition and chaining with other callables.

    :param x: The input value for the callable.
    :return: The result of the callable.
    """

    def __call__(self, x: T) -> RT: ...

    def compose(self, func: "Callable[[U], T] | Composable[U, T]") -> "Composable[U, RT]": ...

    def and_then(self, func: "Callable[[RT], U] | Composable[RT, U]") -> "Composable[T, U]": ...


def composable(func: Callable[[T], RT]) -> Composable[T, RT]:
    """
    Wraps a function to make it composable, allowing chaining with compose and and_then methods.

    :param func: The function to wrap as composable.
    :return: A composable version of the function.
    """

    def compose(another_func: Callable[[U], T] | Composable[U, T]) -> Composable[U, RT]:
        def chained(x: U) -> RT:
            return func(another_func(x))

        return composable(chained)

    def and_then(another_func: Callable[[RT], U] | Composable[RT, U]) -> Composable[T, U]:
        def chained(x: T) -> U:
            return another_func(func(x))

        return composable(chained)

    func.compose = compose
    func.and_then = and_then
    return func


def singleton(tar: Callable[..., RT] = None):
    """
    Decorator to ensure a function or class is only instantiated once. Subsequent calls return the same instance.

    :param tar: The target callable to decorate.
    :return: The singleton instance of the callable.
    """

    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        instance = {}

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            if target not in instance:
                instance[target] = target(*args, **kwargs)
            return instance[target]

        return wrapper

    return decorator if tar is None else decorator(tar)


def memorized(tar: Callable[..., RT] = None, *, ordered: bool = False, typed: bool = False):
    """
    Decorator to cache the results of a function based on its arguments. Supports options for argument order and type.

    :param tar: The target callable to decorate.
    :param ordered: If ``True``, keyword argument order is significant in the cache key.
    :param typed: If ``True``, argument types are included in the cache key.
    :return: The decorated function with memoization.
    """

    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        memory = {}

        def make_key(*args, **kwargs):
            if typed:
                arg_hashes = list(hash(arg) for arg in args)
            else:
                arg_hashes = list(hash((arg, type(arg))) for arg in args)
            if ordered and typed:
                kwarg_hashes = list(hash((k, v, type(v))) for k, v in kwargs.items())
            elif ordered:
                kwarg_hashes = list(hash((k, v)) for k, v in kwargs.items())
            elif typed:
                kwarg_hashes = list(hash((k, v, type(v))) for k, v in sorted(kwargs.items()))
            else:
                kwarg_hashes = list(hash((k, v)) for k, v in sorted(kwargs.items()))
            return hash(tuple(arg_hashes + kwarg_hashes))

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            hash_key = make_key(*args, **kwargs)
            if hash_key not in memory:
                memory[hash_key] = target(*args, **kwargs)
            return memory[hash_key]

        return wrapper

    return decorator if tar is None else decorator(tar)


def lazy(tar: Callable[..., RT] = None):
    """
    Decorator to defer the execution of a function until its result is explicitly requested.

    :param tar: The target callable to decorate.
    :return: A function that returns a callable to execute the original function.
    """

    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            return lambda: target(*args, **kwargs)

        return wrapper

    return decorator if tar is None else decorator(tar)


def unique_returns(tar: Callable[..., RT] = None, *, max_trials: int | None = None):
    """
    Decorator to ensure a function produces unique return values. If no unique value is found within max_trials,
    raises an error.

    :param tar: The target callable to decorate.
    :param max_trials: The maximum number of attempts to find a unique return value. If ``None``,
    attempts are unlimited.
    :return: The decorated function that ensures unique return values.
    """

    def decorator(target):
        if not callable(target):
            raise TypeError("expected a callable")

        seen = set()

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            trials = 0
            while max_trials is None or trials < max_trials:
                result = target(*args, **kwargs)
                if result not in seen:
                    seen.add(result)
                    return result
                trials += 1

            raise ValueError("no unique return value found")

        return wrapper

    return decorator if tar is None else decorator(tar)
