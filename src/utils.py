import shlex

def parse_input(user_input):
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

# Декоратор для обробки помилок
def input_error(func):
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

