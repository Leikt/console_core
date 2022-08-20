def clean_keyboard_interruption(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            exit(0)

    return wrapper
