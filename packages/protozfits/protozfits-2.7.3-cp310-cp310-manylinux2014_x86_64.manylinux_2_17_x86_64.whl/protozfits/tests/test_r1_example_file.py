from importlib.resources import files
from pathlib import Path

import numpy as np

from protozfits import File

test_data_dir = Path(files("protozfits") / "tests/resources")
example_file_path = str(test_data_dir / "example_LST_R1_10_evts.fits.fz")
all_test_resources = sorted(str(p) for p in test_data_dir.glob("*.fits.fz"))


def test_can_iterate_over_events_and_run_header():
    with File(example_file_path) as f:
        camera_config = next(f.CameraConfig)
        assert (camera_config.expected_pixels_id == np.arange(14)).all()

        for i, event in enumerate(f.Events):
            assert event.event_id == i + 1
            assert event.waveform.shape == (1120,)
            assert event.pixel_status.shape == (14,)
            assert event.lstcam.first_capacitor_id.shape == (16,)
            assert event.lstcam.counters.shape == (44,)


def test_can_open_and_get_an_event_from_all_test_resources():
    print()
    for path in all_test_resources:
        with File(path) as f:
            event = next(f.Events)
        print(path, len(str(event)))
