"""Tests for the application factory."""

from flask import Flask

from zecmf import create_app


def test_create_app_basic() -> None:
    """Test that the basic app creation works."""
    app = create_app(
        config_name="testing",
        api_namespaces=[],
        app_config_module="zecmf.config",
    )

    assert isinstance(app, Flask)
    assert "api" in app.blueprints

    assert app.config["TESTING"] is True
    assert app.config["DEBUG"] is False

    assert "flask-jwt-extended" in app.extensions

    routes = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/api/v1/swagger.json" in routes
