def clean_keyboard_interruption(func):
    """Clean the KeyboardInterrupt exception"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            exit(0)

    return wrapper
