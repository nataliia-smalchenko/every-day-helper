from textwrap import wrap
import shlex
import re

from prompt_toolkit import print_formatted_text, HTML
from prettytable import HRuleStyle, PrettyTable



def parse_input(user_input):
    """
    Parse user input string into command and arguments.
    
    :param user_input: The input string from the user.
    :return: Tuple containing the command and a list of arguments.
    """
    try:
        parts = shlex.split(user_input.strip())
    except ValueError as e:
        print_formatted_text(HTML(f"<ansired>Error parsing input: {e}</ansired>"))
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
            e_text = str(e).replace("<", "&lt;")
            e_text = e_text.replace(">", "&gt;")
            return f"<ansired>Error: {e_text}</ansired>"
        except IndexError:
            return "<ansired>Error: Missing arguments.</ansired>"
        except KeyError:
            return "<ansired>Error: Record not found.</ansired>"
    return wrapper


def is_valid_date(date):
    """
    Validate a date string against the format DD.MM.YYYY.
    
    :param date: The date string to validate.
    :return: True if valid, False otherwise.
    """
    date_pattern = r'^([0-2]?[0-9]|3[0-1])\.(0[1-9]|1[0-2])\.\d{4}$'
    return bool(re.match(date_pattern, date))

def draw_table(headers, data, maxcolwidths=None, allhlines=False):
    """
    Generate a formatted table using PrettyTable.

    :param headers (list): Column headers.
    :param data (list of lists): Table rows.
    :param maxcolwidths (list, optional): Max width for each column.
    :param allhlines (bool, optional): Draw horizontal lines for all rows. Default is False.

    :return: PrettyTable: A formatted table.
    """
    hrules = HRuleStyle.ALL if allhlines else HRuleStyle.FRAME

    table = PrettyTable(
        vertical_char="│",
        horizontal_char="─",
        junction_char="┼",
        top_junction_char="┬",
        bottom_junction_char="┴",
        right_junction_char="┤",
        left_junction_char="├",
        top_right_junction_char="╮",
        top_left_junction_char="╭",
        bottom_right_junction_char="╯",
        bottom_left_junction_char="╰",
        hrules=hrules,
        align="l",
    )

    table.field_names = headers

    if maxcolwidths and data:
        cleared_data = []
        for line in data:
            cleared_data.append(
                ["\n".join(wrap(item, width=maxcolwidths[i])) for i, item in enumerate(line)]
            )
        table.add_rows(cleared_data)
    else:
        table.add_rows(data)

    return table