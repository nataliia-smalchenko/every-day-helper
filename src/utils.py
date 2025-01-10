import shlex
import re


def parse_input(user_input):
    """
    Parse user input string into command and arguments.
    
    :param user_input: The input string from the user.
    :return: Tuple containing the command and a list of arguments.
    """
    try:
        parts = shlex.split(user_input.strip())
    except ValueError as e:
        print(f"Error parsing input: {e}")
        return None, []
    if not parts:
        return None, []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


def input_error(func):
    """
    Decorator for error handling in functions.

    :param func: The function to wrap.
    :return: Wrapped function with error handling.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Missing arguments."
        except KeyError:
            return "Error: Record not found."
    return wrapper


def is_valid_date(date):
    """
    Validate a date string against the format DD.MM.YYYY.
    
    :param date: The date string to validate.
    :return: True if valid, False otherwise.
    """
    date_pattern = r'^([0-2]?[0-9]|3[0-1])\.(0[1-9]|1[0-2])\.\d{4}$'
    return bool(re.match(date_pattern, date))
