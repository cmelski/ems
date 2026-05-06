def valid_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if len(password) > 12:
        return False
    return True
