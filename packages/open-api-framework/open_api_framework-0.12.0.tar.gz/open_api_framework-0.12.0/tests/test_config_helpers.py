from open_api_framework.conf.utils import config


def test_empty_list_as_default():
    value = config("SOME_TEST_ENVVAR", split=True, default=[], add_to_docs=False)

    assert value == []


def test_non_empty_list_as_default():
    value = config("SOME_TEST_ENVVAR", split=True, default=["foo"], add_to_docs=False)

    assert value == ["foo"]
