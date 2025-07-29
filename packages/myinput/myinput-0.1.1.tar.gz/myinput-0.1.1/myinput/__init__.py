# myinput/__init__.py

def my_input(prompt="", end=""):
    """
    Custom function to mimic Python's built-in input().
    Prints a prompt and returns user input.
    """
    if not isinstance(end, str):
        end = ""  # Default to empty string if incorrect type passed
    print(prompt, end=end)
    return input()
