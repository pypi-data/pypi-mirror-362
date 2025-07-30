import numpy as np
import pytest
from astropy.io import fits
from astropy.table import Table


@pytest.fixture
def simple_bintable(tmp_path):
    n_rows = 50
    table = Table({"idx": np.arange(n_rows), "value": np.linspace(0, 1, n_rows)})

    hdu = fits.BinTableHDU(table, name="TEST")
    hdu.header["MYBOOL1"] = True, "This value is true"
    hdu.header["MYBOOL2"] = False, "This value is false"
    hdu.header["MYINT1"] = -251, "This value is negative"
    hdu.header["MYINT2"] = 5001, "This value is positive"
    hdu.header["PI"] = np.pi, "Take the cake"
    hdu.header["DOUBLE1"] = 2.1e-10, "Some number smaller than 1"
    hdu.header["DOUBLE2"] = 1.2345678e4, "Some number larger than 1"
    hdu.header["STRING1"] = "Hello World", "A nice greeting"
    hdul = fits.HDUList([fits.PrimaryHDU(), hdu])

    path = tmp_path / "test_simple.fits"
    hdul.writeto(path)
    return path


@pytest.fixture
def two_tables(tmp_path):
    n_rows = 50
    table = Table({"idx": np.arange(n_rows), "value": np.linspace(0, 1, n_rows)})

    hdu1 = fits.BinTableHDU(table, name="TEST-1")
    hdu2 = fits.BinTableHDU(table, name="TEST-2")
    hdul = fits.HDUList([fits.PrimaryHDU(), hdu1, hdu2])

    path = tmp_path / "test_two_tables.fits"
    hdul.writeto(path)
    return path


def test_header(simple_bintable):
    """Test parsing header values"""
    from protozfits.rawzfits import IFits

    with IFits(str(simple_bintable)) as ifits:
        header = ifits.header

    assert header["MYBOOL1"].value is True
    assert header["MYBOOL2"].value is False
    assert header["MYINT1"].value == -251
    assert header["MYINT2"].value == 5001
    assert header["PI"].value == np.pi
    assert header["DOUBLE1"].value == 2.1e-10
    assert header["DOUBLE2"].value == 1.2345678e4
    assert header["STRING1"].value == "Hello World"


def test_seen_tables(two_tables, simple_bintable):
    from protozfits.rawzfits import IFits

    with IFits(str(simple_bintable)) as ifits1, IFits(str(two_tables)) as ifits2:
        while ifits1.has_next_table():
            ifits1.open_next_table()

        while ifits2.has_next_table():
            ifits2.open_next_table()

    assert ifits1.seen_tables == ["TEST"]
    assert ifits2.seen_tables == ["TEST-1", "TEST-2"]
