def get_valid_input(value, min_val, max_val, default):
    try:
        val = int(value)
        if min_val <= val <= max_val:
            return val
        return default
    except (ValueError, TypeError):
        return default

category_mapping = {
    "animals": 27,
    "history": 23,
    "sports": 21,
    "movies": 11,
}
