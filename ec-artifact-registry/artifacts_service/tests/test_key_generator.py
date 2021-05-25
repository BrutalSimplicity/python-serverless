import pytest
from swacorp.ec.artifact_registry.aws.dynamodb.models import (
    FailOnConsecutiveMissingKeysError,
    KeyGenerator,
    TooManyArgumentsError,
)

PREFIX = "__test__"
PREFIXTWO = "__two__"
PREFIXTHREE = "__three__"
PREFIXFOUR = "__four__"


@pytest.fixture
def a_prefix():
    return KeyGenerator(PREFIX)


@pytest.fixture
def two_prefixes():
    return KeyGenerator(PREFIX, PREFIXTWO)


@pytest.fixture
def quadruple_prefixes():
    return KeyGenerator(PREFIX, PREFIXTWO, PREFIXTHREE, PREFIXFOUR)


class TestSinglePrefix:
    def test_no_keys(self, a_prefix: KeyGenerator):
        result = a_prefix.generate(None)
        assert result == PREFIX

    def test_a_key(self, a_prefix: KeyGenerator):
        result = a_prefix.generate("one")
        assert result == f"{PREFIX}#one"

    def test_two_keys(self, a_prefix: KeyGenerator):
        with pytest.raises(TooManyArgumentsError):
            result = a_prefix.generate("one", "two")


class TestDoublePrefix:
    def test_two_keys(self, two_prefixes: KeyGenerator):
        result = two_prefixes.generate("one", "two")
        assert result == f"{PREFIX}#one#{PREFIXTWO}#two"


class TestQuadruplePrefix:
    def test_two_consecutive_missing_keys(self, quadruple_prefixes: KeyGenerator):
        with pytest.raises(FailOnConsecutiveMissingKeysError):
            quadruple_prefixes.generate("one", None, None, "four")
