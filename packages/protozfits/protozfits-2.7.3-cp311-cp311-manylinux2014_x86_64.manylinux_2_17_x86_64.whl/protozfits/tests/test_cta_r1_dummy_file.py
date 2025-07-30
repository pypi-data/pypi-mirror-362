from importlib.resources import files

import numpy as np

from protozfits import File

test_data_dir = files("protozfits") / "tests/resources"
sample_file_path = str(test_data_dir / "10_CTA_R1_dummy_evts.fits.fz")

base_value = 10
arrays_size = 1000


def test_can_read_r1v1_format():
    with File(sample_file_path) as f:
        cam_config = next(f.CameraConfiguration)
        assert cam_config.tel_id == base_value + 0
        assert cam_config.local_run_id == base_value + 1
        assert cam_config.config_time_s == base_value + 2
        assert cam_config.camera_config_id == base_value + 4

        assert (
            cam_config.pixel_id_map
            == np.arange(start=base_value, stop=base_value + arrays_size)
        ).all()
        assert (
            cam_config.module_id_map
            == np.arange(start=base_value + 1, stop=base_value + 1 + arrays_size)
        ).all()

        assert cam_config.num_modules == base_value + 5
        assert cam_config.num_pixels == base_value + 6
        assert cam_config.num_channels == base_value + 7
        assert cam_config.data_model_version == "TEST_VERSION"
        assert cam_config.calibration_service_id == base_value + 9
        assert cam_config.calibration_algorithm_id == base_value + 10
        assert cam_config.num_samples_nominal == base_value + 11
        assert cam_config.num_samples_long == base_value + 12

        for i, event in enumerate(f.Events):
            assert event.event_id == base_value + 0
            assert event.tel_id == base_value + 1
            assert event.local_run_id == base_value + 2
            assert event.event_type == base_value + 3
            assert event.event_time_s == base_value + 4
            assert event.event_time_qns == base_value + 5
            assert event.num_channels == base_value + 6
            assert event.num_samples == base_value + 7
            assert event.num_pixels == base_value + 8
            assert event.num_modules == base_value + 9

            assert (
                event.waveform
                == np.arange(start=base_value, stop=base_value + arrays_size)
            ).all()
            assert (
                event.pixel_status
                == np.arange(start=base_value + 1, stop=base_value + 1 + arrays_size)
            ).all()
            assert (
                event.first_cell_id
                == np.arange(start=base_value + 2, stop=base_value + 2 + arrays_size)
            ).all()
            assert (
                event.module_hires_local_clock_counter
                == np.arange(start=base_value + 3, stop=base_value + 3 + arrays_size)
            ).all()
            assert (
                event.pedestal_intensity
                == np.arange(start=base_value + 4, stop=base_value + 4 + arrays_size)
            ).all()

            assert event.calibration_monitoring_id == base_value + 10
