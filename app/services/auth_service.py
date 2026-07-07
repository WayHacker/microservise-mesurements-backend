import secrets

temp_codes = {}


def generate_code(phone: str) -> str:
    code = "".join(secrets.choice("0123456789") for _ in range(4))
    temp_codes[phone] = code
    print(temp_codes)
    return code


def verify_code(phone: str, code: str) -> bool:
    if temp_codes(phone) == code:
        del temp_codes[phone]
        return True
    return False
