def parse_switch_opt(text):
    if text is None:
        return
    elif str(text).lower() in ("true", "1", "on"):
        return True
    elif str(text).lower() in ("false", "0", "off"):
        return False
    raise ValueError("Can't parse argument. Expected None, True or False")