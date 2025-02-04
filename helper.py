def make_ordinal(n):
    """Convert an integer into its ordinal representation."""
    try:
        n = int(n)
    except ValueError:
        raise ValueError("Please input a valid integer.")

    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
