from src.tools.platform_tools import explain_platform_engineering


def test_platform_engineering_returns_definition():
    result = explain_platform_engineering()
    assert "platform engineering" in result.lower()
    assert "internal developer platform" in result.lower()


def test_platform_engineering_returns_non_empty_string():
    result = explain_platform_engineering()
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_platform_engineering_mentions_key_capabilities():
    result = explain_platform_engineering()
    assert "self-service" in result.lower() or "golden path" in result.lower()
    assert "developer experience" in result.lower() or "developer portal" in result.lower()
