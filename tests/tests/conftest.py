from pathlib import Path

import pooch
import pytest

from brainglobe_utils.image_io import load_any


@pytest.fixture
def data_path():
    """Directory storing all test data"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def test_data_registry():
    """
    Create a test data registry for BrainGlobe.

    Returns:
        pooch.Pooch: The test data registry object.

    """
    registry = pooch.create(
        path=pooch.os_cache("brainglobe_test_data"),
        base_url="https://gin.g-node.org/BrainGlobe/test-data/raw/master/",
        registry={
            "cellfinder/cells-z-1000-1050.xml": None,
            "cellfinder/other-cells-z-1000-1050.xml": None,
            "cellfinder/bright_brain.zip": None,
            "cellfinder/edge_cells_brain.zip": None,
        },
        env="BRAINGLOBE_TEST_DATA_DIR",
    )
    return registry


@pytest.fixture
def bright_brain_path(test_data_registry):
    """Fetches and unzips the contents of 'cellfinder/bright_brain.zip'
    from GIN test data and returns the path to unzipped local folder."""
    bright_brain_relative_path = "cellfinder/bright_brain"
    _ = test_data_registry.fetch(
        f"{bright_brain_relative_path}.zip",
        processor=pooch.Unzip(extract_dir="./"),
        progressbar=True,
    )
    bright_brain_absolute_path = (
        Path(test_data_registry.path) / bright_brain_relative_path
    )
    assert bright_brain_absolute_path.exists()
    return bright_brain_absolute_path


@pytest.fixture
def edge_cells_brain_path(test_data_registry):
    """Fetches and unzips the contents of 'cellfinder/edge_cells_brain.zip'
    from GIN test data and returns the path to unzipped local folder."""
    edge_cells_brain_relative_path = "cellfinder/edge_cells_brain"
    _ = test_data_registry.fetch(
        f"{edge_cells_brain_relative_path}.zip",
        processor=pooch.Unzip(extract_dir="./"),
        progressbar=True,
    )
    edge_cells_brain_absolute_path = (
        Path(test_data_registry.path) / edge_cells_brain_relative_path
    )
    assert edge_cells_brain_absolute_path.exists()
    return edge_cells_brain_absolute_path


# FIXME: putting the two tests below as proof of concept
# and smoke tests for newly added image data on GIN.
# Please refactor into sensible tests in other files..
@pytest.mark.xfail
def test_bright_brain(bright_brain_path):
    bright_brain_signal = load_any(bright_brain_path / "signal/")
    assert not bright_brain_signal.shape


@pytest.mark.xfail
def test_edge_cells_brain(edge_cells_brain_path):
    edge_cells_brain_signal = load_any(edge_cells_brain_path / "signal/")
    assert not edge_cells_brain_signal
