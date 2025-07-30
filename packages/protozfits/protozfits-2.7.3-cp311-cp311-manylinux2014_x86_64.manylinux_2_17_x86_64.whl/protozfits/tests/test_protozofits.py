import numpy as np

from protozfits.anyarray import numpy_to_any_array


def test_write_r1(tmp_path):
    from protozfits import File, ProtobufZOFits
    from protozfits.R1v1_debug_pb2 import DebugCameraConfiguration, DebugEvent
    from protozfits.R1v1_pb2 import CameraConfiguration, Event

    path = tmp_path / "foo.fits.fz"

    with ProtobufZOFits() as f:
        f.open(str(path))
        f.move_to_new_table("CameraConfiguration")
        f.write_message(
            CameraConfiguration(
                local_run_id=1, debug=DebugCameraConfiguration(evb_version="1.0.0")
            )
        )
        f.move_to_new_table("Events")

        for i in range(1, 11):
            e = Event(event_id=i, debug=DebugEvent(extdevices_presence=0b11))
            f.write_message(e)

    assert path.is_file()

    with File(str(path)) as f:
        camera_config = f.CameraConfiguration[0]
        assert camera_config.local_run_id == 1
        assert camera_config.debug.evb_version == "1.0.0"

        i = 0
        for e in f.Events:
            i += 1
            assert e.event_id == i
            assert e.debug.extdevices_presence == 0b11

        assert i == 10


def test_write_dl0(tmp_path):
    from protozfits import File, ProtobufZOFits
    from protozfits.DL0v1_Telescope_pb2 import (
        CameraConfiguration,
    )
    from protozfits.DL0v1_Telescope_pb2 import (
        DataStream as TelescopeDataStream,
    )
    from protozfits.DL0v1_Telescope_pb2 import (
        Event as TelescopeEvent,
    )

    path = tmp_path / "foo.fits.fz"

    with ProtobufZOFits() as f:
        f.open(str(path))
        f.move_to_new_table("CameraConfiguration")
        f.write_message(CameraConfiguration(tel_id=3))
        f.move_to_new_table("DataStream")
        f.write_message(TelescopeDataStream(sb_id=1, obs_id=2, tel_id=3))
        f.move_to_new_table("Events")

        for i in range(1, 11):
            e = TelescopeEvent(event_id=i, tel_id=3)
            f.write_message(e)

    assert path.is_file()

    with File(str(path)) as f:
        camera_config = f.CameraConfiguration[0]
        assert camera_config.tel_id == 3

        data_stream = f.DataStream[0]
        assert data_stream.sb_id == 1
        assert data_stream.obs_id == 2
        assert data_stream.tel_id == 3

        i = 0
        for e in f.Events:
            i += 1
            assert e.event_id == i
            assert e.tel_id == 3

        assert i == 10


def test_write_proto_r1(tmp_path):
    from protozfits import File, ProtobufZOFits
    from protozfits.ProtoR1_pb2 import CameraConfiguration, CameraEvent

    path = tmp_path / "foo.fits.fz"

    with ProtobufZOFits() as f:
        f.open(str(path))
        f.move_to_new_table("CameraConfiguration")
        f.write_message(CameraConfiguration(configuration_id=1))
        f.move_to_new_table("Events")

        for i in range(1, 11):
            e = CameraEvent(event_id=i)
            f.write_message(e)

    assert path.is_file()

    with File(str(path)) as f:
        camera_config = f.CameraConfiguration[0]
        assert camera_config.configuration_id == 1

        i = 0
        for e in f.Events:
            i += 1
            assert e.event_id == i

        assert i == 10


def test_compression(tmp_path):
    from protozfits import ProtobufZOFits
    from protozfits.R1v1_pb2 import Event

    default_path = tmp_path / "default_comp.fits.fz"
    custom_path = tmp_path / "custom_comp.fits.fz"
    rng = np.random.default_rng(0)

    def random_waveform():
        time = rng.uniform(10, 30, (1855, 1))
        amplitude = rng.uniform(0, 500, (1855, 1))

        t = np.arange(40)
        waveform = amplitude * np.exp(-0.25 * (t[np.newaxis, :] - time) ** 2)
        waveform = rng.normal(waveform, 0.1)
        waveform = np.clip(10 * waveform + 400, 0, 4096)
        return waveform.astype(np.uint16)

    # write with to different compression schemes and compare size
    kwargs = dict(compression_block_size_kb=100 * 1024)
    with (
        ProtobufZOFits(**kwargs) as default_writer,
        ProtobufZOFits(**kwargs) as custom_writer,
    ):
        default_writer.open(str(default_path))

        custom_writer.open(str(custom_path))
        custom_writer.set_default_compression("zstd5")
        custom_writer.request_explicit_compression("waveform", "fact")

        pixel_status = np.full(1855, 0b0000_1101, dtype=np.uint8)

        for f in (default_writer, custom_writer):
            f.move_to_new_table("Events")

        for event_id in range(1, 101):
            waveform = random_waveform()
            e = Event(
                event_id=event_id,
                tel_id=1,
                local_run_id=1337,
                event_type=32,
                waveform=numpy_to_any_array(waveform),
                num_channels=1,
                num_pixels=1855,
                num_samples=40,
                pixel_status=numpy_to_any_array(pixel_status),
            )

            for f in (default_writer, custom_writer):
                f.write_message(e)

    # compression should be *much* better
    # currently it's 5.5 vs 15 MB
    assert custom_path.stat().st_size < 0.5 * default_path.stat().st_size


def test_write_dl0_trigger(tmp_path):
    from protozfits import File, ProtobufZOFits
    from protozfits.DL0v1_Trigger_pb2 import (
        DataStream,
        Trigger,
    )

    path = tmp_path / "foo.fits.fz"

    tel_ids = np.arange(1, 19).astype(np.uint16)
    data_stream = DataStream(sb_id=1, obs_id=2, tel_ids=numpy_to_any_array(tel_ids))
    with ProtobufZOFits() as f:
        f.open(str(path))
        f.move_to_new_table("DataStream")
        f.write_message(data_stream)
        f.move_to_new_table("Triggers")

        for i in range(1, 11):
            e = Trigger(trigger_id=i // 5, tel_id=i)
            f.write_message(e)

    assert path.is_file()

    with File(str(path)) as f:
        data_stream = f.DataStream[0]
        assert data_stream.sb_id == 1
        assert data_stream.obs_id == 2
        np.testing.assert_equal(data_stream.tel_ids, tel_ids)

        i = 0
        for e in f.Triggers:
            i += 1
            assert e.trigger_id == i // 5
            assert e.tel_id == i

        assert i == 10


def test_write_header(tmp_path):
    from astropy.io import fits

    from protozfits import ProtobufZOFits
    from protozfits.DL0v1_Telescope_pb2 import Event

    path = tmp_path / "header.fits.fz"

    with ProtobufZOFits() as f:
        f.open(str(path))
        f.move_to_new_table("Events")

        f.set_string("FOO", "bar", "a string value")
        f.set_int("INTVAL", -1, "an int value")
        f.set_bool("BOOLVAL", True, "a bool value")
        f.set_float("FLOATVAL", 1.23456789, "a float value")

        f.write_message(Event(event_id=1))

    assert path.is_file()
    header = fits.getheader(path, "Events")

    assert header["FOO"] == "bar"
    assert header["INTVAL"] == -1
    assert header["BOOLVAL"]
    assert header["FLOATVAL"] == 1.23456789
