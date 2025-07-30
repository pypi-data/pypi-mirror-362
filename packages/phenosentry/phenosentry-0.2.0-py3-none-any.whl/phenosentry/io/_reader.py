import logging
import typing
import zipfile

from pathlib import Path
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket
from phenopackets.schema.v2.phenopackets_pb2 import Cohort
from google.protobuf.json_format import Parse

def read_phenopacket(
    path: Path | zipfile.Path,
    logger: logging.Logger
) -> Phenopacket:
    """
     Reads a single phenopacket from a specified directory.

     Args:
         directory (Path): The path to the directory containing the phenopacket file.
         logger (logging.Logger): Logger instance for logging messages.

     Returns:
         PhenopacketInfo: An object containing information about the phenopacket.

     Raises:
         ParseError: If the phenopacket file cannot be parsed due to invalid format.
     """
    logger.info("Reading phenopacket at `%s`", path)
    return Parse(path.read_text(), Phenopacket())

def read_phenopackets(directory: Path | zipfile.Path, logger: logging.Logger) -> typing.Union[
    typing.List[Phenopacket], typing.Iterator[Phenopacket]]:
    """
    Reads all phenopackets from a specified directory or zip folder.

    Args:
        directory (Path): The path to the directory containing phenopacket files.
        logger (logging.Logger): Logger instance for logging messages.
    Returns:
        typing.List[PhenopacketInfo]: A list of objects containing information about each phenopacket.
    """
    logger.info("Reading phenopackets at `%s`", directory)
    return [
        read_phenopacket(path, logger)
        for path in find_json_files(directory)
        if path.name.endswith(".json")
    ]

def read_cohort(
    directory: Path | zipfile.Path,
    logger: logging.Logger
) -> Cohort:
    """
      Reads a cohort of phenopackets from a specified directory.

      Args:
          :param directory (Path): The path to the directory containing the cohort of phenopackets.
          :param logger (logging.Logger): Logger instance for logging messages.
          :param lazy (boolean): The strategy to use for loading phenopackets.

      Returns:
          CohortInfo: An object containing information about the cohort, including its name, path, and phenopackets.
      """
    logger.info("Reading cohort at `%s`", directory)
    name = ""
    if isinstance(directory, zipfile.Path) and directory.name.endswith(".zip"):
        name = directory.name[:-4]
    else:
        name = directory.stem
    phenopackets = read_phenopackets(directory, logger)
    return Cohort(id=name, members=phenopackets)

def find_json_files(directory):
    for entry in directory.iterdir():
        if entry.is_dir():
            yield from find_json_files(entry)
        elif entry.name.endswith(".json"):
            yield entry