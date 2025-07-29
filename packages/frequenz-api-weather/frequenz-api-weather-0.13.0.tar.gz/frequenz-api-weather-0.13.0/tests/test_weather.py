# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Tests for the frequenz.api.weather package."""


def test_package_import() -> None:
    """Test that the package can be imported."""
    # pylint: disable=import-outside-toplevel
    from frequenz.api.weather import v1

    assert v1 is not None


def test_module_import_components() -> None:
    """Test that the modules can be imported."""
    # pylint: disable=import-outside-toplevel
    from frequenz.api.weather.v1 import weather_pb2

    assert weather_pb2 is not None

    # pylint: disable=import-outside-toplevel
    from frequenz.api.weather.v1 import weather_pb2_grpc

    assert weather_pb2_grpc is not None
