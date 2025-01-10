from prompt_toolkit import print_formatted_text, HTML
import shlex
import re

def parse_input(user_input):
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

# Декоратор для обробки помилок
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print_formatted_text(HTML(f"<ansired>Error: {e}</ansired>"))
        except IndexError:
            print_formatted_text(HTML("<ansired>Error: Missing arguments.</ansired>"))
        except KeyError:
            print_formatted_text(HTML("<ansired>Error: Record not found.</ansired>"))
    return wrapper

def is_valid_date(date):
    
    date_pattern = r'^([0-2]?[0-9]|3[0-1])\.(0[1-9]|1[0-2])\.\d{4}$'
    return bool(re.match(date_pattern, date))