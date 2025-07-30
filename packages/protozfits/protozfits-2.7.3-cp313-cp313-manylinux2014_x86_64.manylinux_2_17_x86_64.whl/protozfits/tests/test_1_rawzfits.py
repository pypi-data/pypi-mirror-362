import importlib
import os
from importlib.resources import files
from pathlib import Path

import numpy as np
import pytest

test_data_dir = Path(files("protozfits") / "tests/resources")
example_file_path = str(test_data_dir / "example_10evts.fits.fz")


EVENTS_IN_EXAMPLE_FILE = 10
EXPECTED_NUMBER_OF_PIXELS = 1296
EXPECTED_NUMBER_OF_SAMPLES = 50
FIRST_EVENT_NUMBER = 97750287


def to_numpy(a):
    any_array_type_to_npdtype = {
        1: "i1",
        2: "u1",
        3: "i2",
        4: "u2",
        5: "i4",
        6: "u4",
        7: "i8",
        8: "u8",
        9: "f4",
        10: "f8",
    }

    any_array_type_cannot_convert_exception_text = {
        0: "This any array has no defined type",
        11: """I have no idea if the boolean representation
            of the anyarray is the same as the numpy one""",
    }
    if a.type in any_array_type_to_npdtype:
        return np.frombuffer(a.data, any_array_type_to_npdtype[a.type])
    else:
        raise ValueError(
            "Conversion to NumpyArray failed with error:\n%s",
            any_array_type_cannot_convert_exception_text[a.type],
        )


def test_import_only():
    importlib.import_module("protozfits.rawzfits")


def test_import_and_open():
    from protozfits import rawzfits

    path = os.path.relpath(example_file_path)
    with rawzfits.ProtobufIFits(file_path=path, table_name="Events"):
        pass


def test_import_open_and_read():
    from protozfits import rawzfits

    path = os.path.relpath(example_file_path)

    with rawzfits.ProtobufIFits(file_path=path, table_name="Events") as ifits:
        ifits.read_serialized_message(1)


def test_import_open_read_and_parse():
    from protozfits import ProtoDataModel_pb2, rawzfits

    path = os.path.relpath(example_file_path)

    with rawzfits.ProtobufIFits(file_path=path, table_name="Events") as ifits:
        raw = ifits.read_serialized_message(1)

    event = ProtoDataModel_pb2.CameraEvent()
    event.ParseFromString(raw)


def test_rawreader_can_work_with_relative_path():
    from protozfits import ProtoDataModel_pb2, rawzfits

    path = os.path.relpath(example_file_path)
    with rawzfits.ProtobufIFits(file_path=path, table_name="Events") as ifits:
        assert len(ifits) == EVENTS_IN_EXAMPLE_FILE

        raw = ifits.read_serialized_message(1)

    event = ProtoDataModel_pb2.CameraEvent()
    event.ParseFromString(raw)


def test_examplefile_has_no_runheader():
    from protozfits import rawzfits

    with pytest.raises(RuntimeError, match="Table RunHeader could not be found"):
        with rawzfits.ProtobufIFits(example_file_path, table_name="RunHeader"):
            pass


def test_rawreader_can_work_with_absolute_path():
    from protozfits import ProtoDataModel_pb2, rawzfits

    with rawzfits.ProtobufIFits(example_file_path, table_name="Events") as ifits:
        assert len(ifits) == EVENTS_IN_EXAMPLE_FILE

        raw = ifits.read_serialized_message(1)

    event = ProtoDataModel_pb2.CameraEvent()
    event.ParseFromString(raw)


def test_rawreader_can_iterate():
    from protozfits import ProtoDataModel_pb2, rawzfits

    with rawzfits.ProtobufIFits(example_file_path, table_name="Events") as ifits:
        for i in range(len(ifits)):
            event = ProtoDataModel_pb2.CameraEvent()
            event.ParseFromString(ifits.read_serialized_message(i + 1))


def test_protobufifits_read_a_given_event():
    from protozfits import ProtoDataModel_pb2, rawzfits

    with rawzfits.ProtobufIFits(example_file_path, table_name="Events") as ifits:
        for random_id in [7, 1, 10, 2]:
            event = ProtoDataModel_pb2.CameraEvent()
            event.ParseFromString(ifits.read_serialized_message(random_id))
            assert event.eventNumber == FIRST_EVENT_NUMBER + random_id - 1


#  We know the iteration part works so we do not want to
# repeat that in every test ... that's boring for you to read


def iterate():
    from protozfits import ProtoDataModel_pb2, rawzfits

    with rawzfits.ProtobufIFits(example_file_path, "Events") as ifits:
        for i in range(len(ifits)):
            event = ProtoDataModel_pb2.CameraEvent.FromString(
                ifits.read_serialized_message(i + 1)
            )
            yield i, event


def test_event_has_certain_fields():
    """
    The ProtoDataModel_pb2.CameraEvent has many fields, and sub fields.
    However many of them seem to be not used at the moment in SST1M
    So I check if these fields are non empty, since I have seen them used
    in code
    """
    for _, e in iterate():
        assert e.eventNumber is not None
        assert e.telescopeID is not None
        assert e.head.numGainChannels is not None

        assert e.local_time_sec is not None
        assert e.local_time_nanosec is not None

        assert e.trig.timeSec is not None
        assert e.trig.timeNanoSec is not None

        assert e.event_type is not None
        assert e.eventType is not None

        assert e.hiGain.waveforms.samples is not None
        assert e.hiGain.waveforms.baselines is not None
        assert e.pixels_flags is not None

        assert e.trigger_input_traces is not None
        assert e.trigger_output_patch7 is not None
        assert e.trigger_output_patch19 is not None


#  from this point on, we test not the interface, but that the values
#  are roughly what we expect them to be


def test_event_number():
    first_event_in_example_file = 97750287
    for i, e in iterate():
        assert e.eventNumber == i + first_event_in_example_file


def test_telescope_id():
    telescope_id_in_example_file = 1
    for i, e in iterate():
        assert e.telescopeID == telescope_id_in_example_file


def test_num_channels():
    for i, e in iterate():
        assert e.head.numGainChannels == -1


def test_local_time():
    expected_local_time = [
        1509415494406789700,
        1509415494408104064,
        1509415494408683944,
        1509415494415717036,
        1509415494418082848,
        1509415494421871916,
        1509415494424555140,
        1509415494426785248,
        1509415494438982004,
        1509415494445290168,
    ]

    for i, e in iterate():
        local_time = e.local_time_sec * int(1e9) + e.local_time_nanosec
        assert local_time == expected_local_time[i]


def test_trigger_time():
    for _, e in iterate():
        local_time = e.trig.timeSec * 1e9 + e.trig.timeNanoSec
        assert local_time == 0


def test_event_type():
    expected = [1, 1, 1, 1, 1, 8, 1, 1, 1, 1]
    for i, e in iterate():
        assert e.event_type == expected[i]
        assert e.eventType == 0


def test_samples():
    for _, e in iterate():
        samples = to_numpy(e.hiGain.waveforms.samples)
        n = EXPECTED_NUMBER_OF_PIXELS * EXPECTED_NUMBER_OF_SAMPLES
        assert samples.shape == (n,)
        assert samples.dtype == np.int16
        assert samples.min() >= 0
        assert samples.max() <= (2**12) - 1


def test_baselines():
    for i, e in iterate():
        baselines = to_numpy(e.hiGain.waveforms.baselines)
        assert baselines.shape == (EXPECTED_NUMBER_OF_PIXELS,)
        assert baselines.dtype == np.int16
        assert baselines.min() >= 0
        assert baselines.max() <= (2**12) - 1


def test_pixel_flags():
    for i, e in iterate():
        pixel_flags = to_numpy(e.pixels_flags)
        assert pixel_flags.shape == (EXPECTED_NUMBER_OF_PIXELS,)
        assert pixel_flags.dtype == np.uint16


def test_trigger_input_traces():
    for i, e in iterate():
        trigger_input_traces = to_numpy(e.trigger_input_traces)
        assert trigger_input_traces.shape == (28800,)
        assert trigger_input_traces.dtype == np.uint8


def test_trigger_output_patch7():
    for i, e in iterate():
        trigger_output_patch7 = to_numpy(e.trigger_output_patch7)
        assert trigger_output_patch7.shape == (2700,)
        assert trigger_output_patch7.dtype == np.uint8


def test_trigger_output_patch19():
    for i, e in iterate():
        trigger_output_patch19 = to_numpy(e.trigger_output_patch19)
        assert trigger_output_patch19.shape == (2700,)
        assert trigger_output_patch19.dtype == np.uint8


def test_no_crash_when_iterating_too_far():
    from protozfits import ProtobufIFits, ProtoDataModel_pb2

    with ProtobufIFits(example_file_path, table_name="Events") as ifits:
        for i in range(len(ifits)):
            event = ProtoDataModel_pb2.CameraEvent()
            event.ParseFromString(ifits.read_serialized_message(i + 1))

        # At this point we iterated through the entire file.
        # In version 0.43 we got a crash (seg fault or so) when iterating too
        # far. This test should ensure this behaviour is fixed in 0.44

        with pytest.raises(IndexError):
            ifits.read_serialized_message(i + 2)
