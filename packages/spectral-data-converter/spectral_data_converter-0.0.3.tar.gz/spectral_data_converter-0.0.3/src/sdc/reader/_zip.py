import argparse
import fnmatch
import os
from io import BytesIO
from typing import List, Iterable, Union
from zipfile import ZipFile

from seppl import init_initializable, Initializable
from seppl.io import locate_files, DirectReader
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from wai.logging import LOGGING_WARNING

from sdc.api import Reader, SampleData, Spectrum2D, parse_reader


class ZipReader(Reader, DirectReader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 resume_from: str = None, pattern: str = None, reader: str = None, direct_read: bool = False,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param pattern: the glob pattern that files must match in order to be extracted, None for all
        :type pattern: str
        :param reader: the command-line of the base reader to use
        :type reader: str
        :param direct_read: whether to use direct read mode
        :type direct_read: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.resume_from = resume_from
        self.pattner = pattern
        self.reader = reader
        self._direct_read = direct_read
        self._inputs = None
        self._current_input = None
        self._reader = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-zip"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads spectra or sample data matching the pattern from the zip file(s) using the specified reader."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the zip file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the zip files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.zip'", required=False)
        parser.add_argument("-p", "--pattern", type=str, help="Glob expression matching the files to extract, e.g., '*.spec'", required=False)
        parser.add_argument("-r", "--reader", type=str, help="The command-line of the direct reader to use for reading the spectra or sample data from the zip archive.", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.resume_from = ns.resume_from
        self.pattern = ns.pattern
        self.reader = ns.reader

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self._reader is None:
            return [Spectrum2D, SampleData]
        else:
            return self._reader.generates()

    @property
    def direct_read(self) -> bool:
        """
        Returns whether the reader is in direct read mode.

        :return: True if in direct read mode
        :rtype: bool
        """
        return self._direct_read

    @direct_read.setter
    def direct_read(self, direct: bool):
        """
        Sets whether the reader is to be used in direct mode or not.

        :param direct: True if to use in direct read mode
        :type direct: bool
        """
        self._direct_read = direct

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        self._reader = parse_reader(self.reader)
        if not isinstance(self._reader, DirectReader):
            raise Exception("Base reader is not a direct reader: %s" % str(type(self._reader)))
        self._reader.direct_read = True
        self._reader.session = self.session
        if isinstance(self._reader, Initializable) and not init_initializable(self._reader, "reader"):
            self.logger().error("Failed to initialize reader: %s" % self.reader)

        if self.direct_read:
            self._inputs = []
        else:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.zip", resume_from=self.resume_from)

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        with open(self.session.current_input, "rb") as fp:
            yield self.read_fp(fp)

    def read_fp(self, fp) -> Iterable:
        """
        Reads the data from the file-like object and returns the items one by one.

        :param fp: the file-like object to read from
        :return: the data
        :rtype: Iterable
        """
        zipfile = ZipFile(fp)
        names = zipfile.namelist()
        self.logger().info("# files in zip file: %d" % len(names))
        if self.pattern is not None:
            names = fnmatch.filter(names, self.pattern)
            self.logger().info("# matching files: %d" % len(names))
        for name in names:
            self.logger().info("Extracting: %s" % name)
            data = zipfile.read(name)
            buffer = BytesIO(data)
            self.logger().info("Reading data from: %s" % name)
            for item in self._reader.read_fp(buffer):
                if isinstance(item, Spectrum2D):
                    item.spectrum_name = os.path.basename(name)
                if isinstance(item, SampleData):
                    item.sampledata_name = os.path.basename(name)
                yield item

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
