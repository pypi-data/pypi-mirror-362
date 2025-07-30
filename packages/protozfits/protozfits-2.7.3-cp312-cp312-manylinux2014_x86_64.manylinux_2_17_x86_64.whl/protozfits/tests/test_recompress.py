from importlib.resources import files
from pathlib import Path

import pytest

from protozfits import File, recompress_zfits

test_data_dir = Path(files("protozfits") / "tests/resources")
test_file = str(test_data_dir / "example_LST_R1_10_evts.fits.fz")


def test_recompress_help():
    with pytest.raises(SystemExit) as e:
        recompress_zfits.main(["--help"])
    assert e.value.code == 0


def test_recompress(tmp_path):
    output_path = tmp_path / "recompressed.fits.fz"
    recompress_zfits.main([test_file, str(output_path), "--default-compression=zstd9"])
    with File(output_path) as f:
        assert len(f.Events) == 10


def test_recompress_n_events(tmp_path):
    output_path = tmp_path / "recompressed.fits.fz"
    recompress_zfits.main(
        [test_file, str(output_path), "-n", "5", "--default-compression=zstd9"]
    )

    with File(output_path) as f:
        assert len(f.Events) == 5
