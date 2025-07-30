"""This module contains the `BZIP2LAMMPSWriter` class."""

import bz2
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO

from irradiapy import config


@dataclass
class BZIP2LAMMPSWriter:
    """A class to write data like a LAMMPS dump file, but compressed with bzip2.

    Note
    ----
    If you only need to compress a file, use `irradiapy.io.io_utils.compress_file_bz2` instead.

    Attributes
    ----------
    file_path : Path
        The path to the bzip2-compressed LAMMPS dump file.
    mode : str, optional (default="wt")
        The file open mode.
    excluded_items : list[str], optional (default=irradiapy.config.EXCLUDED_ITEMS)
        Atom fields to exclude from output.
    encoding : str, optional (default=irradiapy.config.ENCODING)
        The file encoding.
    int_format : str, optional (default=irradiapy.config.INT_FORMAT)
        The format for integers.
    float_format : str, optional (default=irradiapy.config.FLOAT_FORMAT)
        The format for floats.
    compresslevel : int, optional (default=9)
        The bzip2 compression level.
    """

    file_path: Path
    mode: str = "wt"
    excluded_items: list[str] = field(default_factory=lambda: config.EXCLUDED_ITEMS)
    encoding: str = field(default_factory=lambda: config.ENCODING)
    int_format: str = field(default_factory=lambda: config.INT_FORMAT)
    float_format: str = field(default_factory=lambda: config.FLOAT_FORMAT)
    compresslevel: int = 9
    file: BinaryIO = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.file = bz2.open(
            self.file_path,
            self.mode,
            encoding=self.encoding,
            compresslevel=self.compresslevel,
        )

    def __enter__(self) -> "BZIP2LAMMPSWriter":
        return self

    def __del__(self) -> None:
        if self.file is not None:
            self.file.close()

    def __exit__(self, exc_type=None, exc_value=None, exc_traceback=None) -> bool:
        if self.file is not None:
            self.file.close()
        return False

    def close(self) -> None:
        """Closes the file associated with this writer."""
        if self.file is not None:
            self.file.close()

    def write(self, data: dict) -> None:
        """Writes the data (from LAMMPSReader/BZIP2LAMMPSReader) to the file.

        Parameters
        ----------
        data : dict
            The dictionary containing the data.
        """
        if data.get("time") is not None:
            self.file.write(f"ITEM: TIME\n{data['time']}\n")
        self.file.write(f"ITEM: TIMESTEP\n{data['timestep']}\n")
        self.file.write(f"ITEM: NUMBER OF ATOMS\n{data['natoms']}\n")
        self.file.write(f"ITEM: BOX BOUNDS {' '.join(data['boundary'])}\n")
        self.file.write(
            f"{self.float_format % data['xlo']} {self.float_format % data['xhi']}\n"
        )
        self.file.write(
            f"{self.float_format % data['ylo']} {self.float_format % data['yhi']}\n"
        )
        self.file.write(
            f"{self.float_format % data['zlo']} {self.float_format % data['zhi']}\n"
        )

        atoms = data["atoms"]
        field_names = [f for f in atoms.dtype.names if f not in self.excluded_items]
        self.file.write(f"ITEM: ATOMS {' '.join(field_names)}\n")

        formatters = []
        for field_name in field_names:
            dtype = atoms.dtype[field_name]
            if dtype.kind == "i":
                formatters.append(self.int_format)
            elif dtype.kind == "f":
                formatters.append(self.float_format)
            else:
                formatters.append("%s")

        for row in atoms:
            self.file.write(
                " ".join(
                    fmt % row[field_name]
                    for fmt, field_name in zip(formatters, field_names)
                )
                + "\n"
            )
