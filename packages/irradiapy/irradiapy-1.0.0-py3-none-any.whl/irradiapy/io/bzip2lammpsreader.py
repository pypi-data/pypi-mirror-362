"""This module contains the `BZIP2LAMMPSReader` class."""

import bz2
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Generator, Type

import numpy as np


@dataclass
class BZIP2LAMMPSReader:
    """A class to read data from a bzip2-compressed LAMMPS dump file.

    Note
    ----
    Assumed orthogonal simulation box.

    Note
    ----
    If you only need to decompress a file, use `irradiapy.io.io_utils.decompress_file_bz2` instead.


    Attributes
    ----------
    file_path : Path
        The path to the bzip2-compressed LAMMPS dump file.
    encoding : str, optional (default="utf-8")
        The file encoding.
    """

    file_path: Path
    encoding: str = "utf-8"
    file: BinaryIO = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.file = bz2.open(self.file_path, mode="rt", encoding=self.encoding)

    def __del__(self) -> None:
        if self.file is not None:
            self.file.close()

    def __iter__(
        self,
    ) -> Generator[
        dict,
        None,
        None,
    ]:
        """Read the bzip2 file as an iterator, timestep by timestep.

        Yields
        ------
        dict
            A dictionary containing the timestep data with keys:
            'time' (optional), 'timestep', 'natoms', 'boundary', 'xlo', 'xhi',
            'ylo', 'yhi', 'zlo', 'zhi', and 'atoms' (as a numpy structured array).
        """
        with bz2.open(self.file_path, mode="rt", encoding="utf-8") as file:
            while True:
                data = defaultdict(None)
                line = file.readline()
                if not line:
                    break
                if line == "ITEM: TIME\n":
                    data["time"] = float(file.readline())
                    file.readline()
                data["timestep"] = int(file.readline())
                file.readline()
                data["natoms"] = int(file.readline())
                data["boundary"] = file.readline().split()[-3:]
                data["xlo"], data["xhi"] = map(float, file.readline().split())
                data["ylo"], data["yhi"] = map(float, file.readline().split())
                data["zlo"], data["zhi"] = map(float, file.readline().split())

                line = file.readline()
                items, types, dtype = self.__get_dtype(line)
                data["atoms"] = np.empty(data["natoms"], dtype=dtype)
                for i in range(data["natoms"]):
                    line = file.readline().split()
                    for j, item in enumerate(items):
                        data["atoms"][i][item] = types[j](line[j])
                yield data

    def __get_dtype(
        self, line: str
    ) -> tuple[list[str], list[Type[int | float]], np.dtype]:
        items = line.split()[2:]
        types = [
            int if item in ("id", "type", "element", "size") else float
            for item in items
        ]
        dtype = np.dtype([(item, type) for item, type in zip(items, types)])
        return items, types, dtype

    def close(self) -> None:
        """Close the file associated with this reader."""
        self.file.close()
