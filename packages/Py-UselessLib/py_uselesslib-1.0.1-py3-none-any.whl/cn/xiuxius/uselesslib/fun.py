import random
from typing import Callable, Any, Optional


def execute_fun(fn: Callable):
    """
    Executes the given function with no arguments.
    :param fn: A callable (function) with no required parameters.
    :return: The result of calling fn().
    """
    if not callable(fn):
        raise TypeError("execute_fun expects a callable.")
    return fn()


def execute_fun_with_args(fn: Callable, *args: Any):
    """
    Executes the given function with the provided arguments.
    :param fn: A callable (function) with required parameters.
    :param args: The arguments to pass to fn().
    :return: The result of calling fn(*args).
    """
    if not callable(fn):
        raise TypeError("execute_fun_with_args expects a callable.")
    return fn(*args)


def execute_fun_with_kwargs(fn: Callable, **kwargs: Any):
    """
    Executes the given function with the provided keyword arguments.
    :param fn: A callable (function) with required parameters.
    :param kwargs: The keyword arguments to pass to fn().
    :return: The result of calling fn(**kwargs).
    """
    if not callable(fn):
        raise TypeError("execute_fun_with_kwargs expects a callable.")
    return fn(**kwargs)


def execute_fun_with_args_and_kwargs(fn: Callable, *args: Any, **kwargs: Any):
    """
    Executes the given function with the provided arguments and keyword arguments.
    :param fn: A callable (function) with required parameters.
    :param args: The arguments to pass to fn().
    :param kwargs: The keyword arguments to pass to fn().
    :return: The result of calling fn(*args, **kwargs).
    """
    if not callable(fn):
        raise TypeError("execute_fun_with_args_and_kwargs expects a callable.")
    return fn(*args, **kwargs)


def execute_fun_with_random_exception(
    fn: Callable,
    probability: float = 1.0,
    exception: Optional[Exception] = None,
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    Executes the given function with provided arguments and keyword arguments,
    but with a chance of raising an exception instead of executing.

    :param fn: The callable function to execute.
    :param probability: A float between 0 and 1 representing the chance to raise an exception.
    :param exception: Optional Exception instance to raise if the exception is triggered.
                      If None, a random default exception will be raised.
    :param args: Positional arguments to pass to fn.
    :param kwargs: Keyword arguments to pass to fn.
    :return: The result of fn(*args, **kwargs) if no exception is raised.
    :raises: The specified or random exception based on the probability.
    """
    if not callable(fn):
        raise TypeError("fn must be a callable")
    if not (0 <= probability <= 1):
        raise ValueError("probability must be between 0 and 1")
    if random.random() < probability:
        if exception is not None:
            raise exception
        else:
            default_exceptions = [
                ValueError("Randomly raised ValueError"),
                RuntimeError("Randomly raised RuntimeError"),
                KeyError("Randomly raised KeyError"),
                Exception("Randomly raised generic Exception"),
                TypeError("Randomly raised TypeError"),
                IndexError("Randomly raised IndexError"),
                AttributeError("Randomly raised AttributeError"),
                MemoryError("Randomly raised MemoryError"),
                ZeroDivisionError("Randomly raised ZeroDivisionError"),
                OverflowError("Randomly raised OverflowError"),
                FloatingPointError("Randomly raised FloatingPointError"),
                ArithmeticError("Randomly raised ArithmeticError"),
                AssertionError("Randomly raised AssertionError"),
                ImportError("Randomly raised ImportError"),
                ModuleNotFoundError("Randomly raised ModuleNotFoundError"),
                NameError("Randomly raised NameError"),
                UnboundLocalError("Randomly raised UnboundLocalError"),
                SyntaxError("Randomly raised SyntaxError"),
                IndentationError("Randomly raised IndentationError"),
                TabError("Randomly raised TabError"),
                SystemError("Randomly raised SystemError"),
                ReferenceError("Randomly raised ReferenceError"),
                StopIteration("Randomly raised StopIteration"),
                StopAsyncIteration("Randomly raised StopAsyncIteration"),
                EOFError("Randomly raised EOFError"),
                KeyboardInterrupt("Randomly raised KeyboardInterrupt"),
                GeneratorExit("Randomly raised GeneratorExit"),
                SystemExit("Randomly raised SystemExit"),
                BlockingIOError("Randomly raised BlockingIOError"),
                BrokenPipeError("Randomly raised BrokenPipeError"),
                ChildProcessError("Randomly raised ChildProcessError"),
                ConnectionError("Randomly raised ConnectionError"),
                ConnectionAbortedError("Randomly raised ConnectionAbortedError"),
                ConnectionRefusedError("Randomly raised ConnectionRefusedError"),
                ConnectionResetError("Randomly raised ConnectionResetError"),
                FileExistsError("Randomly raised FileExistsError"),
                FileNotFoundError("Randomly raised FileNotFoundError"),
                InterruptedError("Randomly raised InterruptedError"),
                IsADirectoryError("Randomly raised IsADirectoryError"),
                NotADirectoryError("Randomly raised NotADirectoryError"),
                PermissionError("Randomly raised PermissionError"),
                ProcessLookupError("Randomly raised ProcessLookupError"),
                TimeoutError("Randomly raised TimeoutError"),
                RecursionError("Randomly raised RecursionError"),
                UnicodeError("Randomly raised UnicodeError"),
                UnicodeEncodeError("Randomly raised UnicodeEncodeError"),
                UnicodeDecodeError("Randomly raised UnicodeDecodeError"),
                UnicodeTranslateError("Randomly raised UnicodeTranslateError"),
            ]
            raise random.choice(default_exceptions)
    else:
        return fn(*args, **kwargs)
