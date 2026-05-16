from dev.utilities.generic_utils import valid_password


def test_valid_password():
    assert valid_password('123456789999') is True


def test_password_too_short():
    assert valid_password('1234567') is False


def test_valid_password_too_long():
    assert valid_password('1234567899999') is False
