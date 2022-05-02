from mediate import utils


def test_identity() -> None:
    assert utils.identity(123) == 123
