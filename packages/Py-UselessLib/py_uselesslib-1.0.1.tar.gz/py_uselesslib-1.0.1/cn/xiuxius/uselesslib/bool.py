import random


def is_true(n: bool) -> bool:
    """
    Determines if a number is true.
    :param n: The bool to check.
    :return: True if the bool is true, False otherwise.
    """
    return n == True


def is_false(n: bool) -> bool:
    """
    Determines if a number is false.
    :param n: The bool to check.
    :return: True if the bool is false, False otherwise.
    """
    return n == False


def is_not_true(n: bool) -> bool:
    """
    Determines if a number is not true.
    :param n: The bool to check.
    :return: True if the bool is not true, False otherwise.
    """
    return n != True


def is_not_false(n: bool) -> bool:
    """
    Determines if a number is not false.
    :param n: The bool to check.
    :return: True if the bool is not false, False otherwise.
    """
    return n != False


def is_true_or_false(n: bool) -> bool:
    """
    Determines if a number is true or false.
    :param n: The bool to check.
    :return: True if the bool is true or false, False otherwise.
    """
    return n == True or n == False


def is_true_and_false(n: bool) -> bool:
    """
    Determines if a number is true and false.
    :param n: The bool to check.
    :return: True if the bool is true and false, False otherwise.
    """
    return n == True and n == False


def random_bool() -> bool:
    """
    Generates a random bool.
    :return: A random bool.
    """
    return random.choice([True, False])


def get_true() -> bool:
    """
    Gets the true bool.
    :return: The true bool.
    """
    return True


def get_false() -> bool:
    """
    Gets the false bool.
    :return: The false bool.
    """
    return False
