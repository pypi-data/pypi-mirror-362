import math
import sys
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

import yaml
from astropy.extern.configobj.validate import pprint
from astropy.io import fits
from tqdm import tqdm

from . import get_class_from_PBFHEAD
from .rawzfits import ProtobufIFits, ProtobufZOFits
from .version import __version__


def existing_file(path):
    path = Path(path)
    if not path.exists():
        raise ArgumentTypeError(f"Path '{path}' does not exist")

    if not path.is_file():
        raise ArgumentTypeError(f"Path '{path}' is not a f file")

    return path


parser = ArgumentParser()
parser.add_argument("inputfile", type=existing_file)
parser.add_argument("outputfile", type=Path)
parser.add_argument(
    "-n", "--n-events", type=int, default=None, help="If given, stop after n events"
)
parser.add_argument(
    "--rows-per-tile",
    type=int,
    help="Number of events per tile, if not given, same as inputfile will be used",
)
parser.add_argument(
    "--block-size", type=int, default=100, help="Compression block size in MB"
)
parser.add_argument(
    "--overwrite", action="store_true", help="Overwrite output file without asking"
)

parser.add_argument(
    "--config",
    type=Path,
    help="Path to yaml config file setting up compression options",
)
parser.add_argument(
    "--default-compression",
    type=str,
    help="Default compression to be used, see adh-apis for supported compressions",
)
parser.add_argument(
    "-c",
    "--column-compression",
    action="append",
    nargs=2,
    type=str,
    help="Compression to be used for a specific column",
)
parser.add_argument("--version", action="version", version=__version__)


def load_config(args):
    """Load compression configuration from yaml"""

    if args.config is not None:
        compression_config = yaml.safe_load(args.config.read_text())
    else:
        compression_config = {}

    if "column_compression" not in compression_config:
        compression_config["column_compression"] = {}

    if args.default_compression:
        compression_config["default_compression"] = args.default_compression

    if args.column_compression is not None:
        for field, compression in args.column_compression:
            compression_config["column_compression"][field] = compression

    return compression_config


def get_headers(inputfile):
    """Get a mapping of extname to headers from the input file."""
    # currently there is no way to get the table names and headers using
    # protozfits python bindings, so use astropy
    headers = {}
    with fits.open(inputfile) as hdul:
        for hdu in hdul:
            if isinstance(hdu, fits.BinTableHDU):
                headers[hdu.name] = hdu.header

    return headers


def main(args=None):
    args = parser.parse_args(args=args)

    if args.outputfile.exists() and not args.overwrite:
        print(f"outputfile {args.outputfile} already exists", file=sys.stderr)
        sys.exit(2)

    headers = get_headers(args.inputfile)
    print(f"Inputfile contains tables: {list(headers)}")

    compression_config = load_config(args)
    args.outputfile.parent.mkdir(parents=True, exist_ok=True)

    if args.rows_per_tile is None:
        args.rows_per_tile = headers["Events"]["ZTILELEN"]

    n_events_in_input = headers["Events"]["ZNAXIS2"]
    if args.n_events is None:
        args.n_events = n_events_in_input
    else:
        args.n_events = min(n_events_in_input, args.n_events)

    if args.n_events < args.rows_per_tile:
        args.rows_per_tile = args.n_events
        n_tiles = 1
    else:
        n_tiles = int(math.ceil(args.n_events / args.rows_per_tile))

    kwargs = dict(
        compression_block_size_kb=args.block_size * 1024,
        n_tiles=n_tiles,
        rows_per_tile=args.rows_per_tile,
    )

    print("Using the following compression configuration")
    pprint(compression_config)

    with ProtobufZOFits(**kwargs) as outfile:
        outfile.open(str(args.outputfile))

        if default_compression := compression_config.get("default_compression"):
            outfile.set_default_compression(default_compression)

        for field, compression in compression_config["column_compression"].items():
            outfile.request_explicit_compression(field, compression)

        for table, header in headers.items():
            print("Writing table", table)
            outfile.move_to_new_table(table)
            infile = ProtobufIFits(str(args.inputfile), table)
            proto_cls = get_class_from_PBFHEAD(header["PBFHEAD"])

            if table == "Events":
                n = args.n_events
            else:
                n = len(infile)

            for i in tqdm(range(n)):
                msg = proto_cls.FromString(infile.read_serialized_message(i + 1))
                outfile.write_message(msg)


if __name__ == "__main__":
    main()
