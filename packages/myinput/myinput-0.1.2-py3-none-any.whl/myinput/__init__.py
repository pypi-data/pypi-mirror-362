def my_input(prompt="", end=""):
    """
    Custom input function to mimic Python's built-in input().
    """
    print(prompt, end=end)
    return input()  # ✅ This works in all environments
