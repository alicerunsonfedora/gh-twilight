from gh_twilight import __version__, create_dataset, GHRepositoryWeeksum
import numpy

def test_version():
    """Test that the version string matches."""
    assert __version__ == '0.1.0'

def test_dataset_create():
    """Test that the dataset created is a proper numpy array."""
    example_repo = GHRepositoryWeeksum("example/example",
                                       "John Smith",
                                       500,
                                       512,
                                       [12, 12, 31, 100, 200, 15, 120])
    data = create_dataset([example_repo])
    assert isinstance(data["data"][0], numpy.ndarray) \
        and isinstance(data["data"][1], numpy.ndarray)
