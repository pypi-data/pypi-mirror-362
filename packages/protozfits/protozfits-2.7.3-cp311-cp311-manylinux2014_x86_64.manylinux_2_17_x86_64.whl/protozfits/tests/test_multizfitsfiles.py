from importlib.resources import files
from pathlib import Path

from protozfits import File, MultiZFitsFiles

test_data_dir = Path(files("protozfits") / "tests/resources")
test_paths = sorted(str(p) for p in test_data_dir.glob("*.fits.fz"))

EVENTS_IN_EXAMPLE_FILE = 10
EXPECTED_NUMBER_OF_PIXELS = 1296
EXPECTED_NUMBER_OF_SAMPLES = 50
FIRST_EVENT_NUMBER = 97750287


def test_len():
    """
    'example_100evts.fits.fz': Table(100xDataModel.CameraEvent),
    'example_LST_R1_10_evts.fits.fz': Table(10xR1.CameraEvent),
    'example_10evts.fits.fz': Table(10xDataModel.CameraEvent),
    'example_9evts_NectarCAM.fits.fz': Table(9xDataModel.CameraEvent),
    'example_SST1M_20180822.fits.fz': Table(32xDataModel.CameraEvent),

    expected number of events: 100 + 10 + 10 + 9 + 32 = 161
    """
    expected_number_of_events = 0
    for path in test_paths:
        with File(path) as f:
            expected_number_of_events += len(f.Events)

    with MultiZFitsFiles(test_paths) as f:
        assert len(f) == expected_number_of_events


def test_can_iterate():
    with MultiZFitsFiles(test_paths) as f:
        assert sum(1 for e in f) == len(f)


def test_is_iteration_order_correct():
    """I have no idea how to test this."""
    with MultiZFitsFiles(test_paths) as f:
        for e in f:
            # the tests files are very heterogeneous, some have `eventNumber`
            # all have `event_id` but for those which have `eventNumber`,
            # the `event_id` is always zero.
            try:
                print(e.eventNumber)
            except AttributeError:
                print(e.event_id)


def test_headers():
    with MultiZFitsFiles(test_paths) as mf:
        for key in ("ZNAXIS2", "PBFHEAD"):
            for path, value in mf.headers[key].items():
                with File(path) as f:
                    assert f.Events.header[key] == value
