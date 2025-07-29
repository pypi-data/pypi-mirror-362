import argparse
import csv
import os
from typing import List, Iterable, Union

from seppl.io import locate_files, DirectReader
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from simple_range import Index, Range
from wai.logging import LOGGING_WARNING
from wai.spectralio.csv import Reader as SReader

from sdc.api import SpectralIOReader, SampleDataReader, Spectrum2D, SampleData, SAMPLE_ID


class CSVReader(SpectralIOReader, DirectReader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None, resume_from: str = None,
                 sample_id: str = None, spectral_data: str = None, sample_data: str = None, sample_data_prefix: str = None,
                 wave_numbers_in_header: bool = None, wave_numbers_regexp: str = None,
                 instrument: str = None, format: str = None, keep_format: bool = None,
                 direct_read: bool = False, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param sample_id: the 1-based index of the sample ID column
        :type sample_id: str
        :param spectral_data: the range of amplitude columns (1-based)
        :type spectral_data: str
        :param sample_data: the range of reference data columns (1-based)
        :type sample_data: str
        :param sample_data_prefix: the prefix to use for the sample data columns
        :typer sample_data_prefix: str
        :param wave_numbers_in_header: whether the wave numbers are encoded in the column names
        :type wave_numbers_in_header: bool
        :param wave_numbers_regexp: the regular expression to identify the wave number in the column name (uses 1st group)
        :type wave_numbers_regexp: str
        :param instrument: the instrument name to use
        :type instrument: str
        :param format: the spectral format
        :type format: str
        :param keep_format: whether to keep the format determined by the reader
        :type keep_format: bool
        :param direct_read: whether to use direct read mode
        :type direct_read: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(instrument=instrument, format=format, keep_format=keep_format,
                         logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.resume_from = resume_from
        self.sample_id = sample_id
        self.spectral_data = spectral_data
        self.sample_data = sample_data
        self.sample_data_prefix = sample_data_prefix
        self.wave_numbers_in_header = wave_numbers_in_header
        self.wave_numbers_regexp = wave_numbers_regexp
        self._direct_read = direct_read
        self._reader = None
        self._inputs = None
        self._current_input = None
        self._reader = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-csv"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the spectra in CSV format (row-wise)."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the CSV file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the CSV files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.csv'", required=False)
        parser.add_argument("--sample_id", type=str, help="The 1-based index of the sample ID column.", required=False, default="1")
        parser.add_argument("--spectral_data", type=str, help="The range of columns containing the spectral data (1-based).", required=False, default="2-last")
        parser.add_argument("--sample_data", type=str, help="The range of columns containing the reference values (1-based).", required=False, default=None)
        parser.add_argument("--sample_data_prefix", type=str, help="The prefix used by the sample data columns.", required=False, default=None)
        parser.add_argument("--wave_numbers_in_header", action="store_true", help="Whether the wave numbers are encoded in the column name.")
        parser.add_argument("--wave_numbers_regexp", type=str, help="The regular expression for extracting the wave numbers from the column names (1st group is used).", required=False, default="(.*)")
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
        self.sample_id = ns.sample_id
        self.spectral_data = ns.spectral_data
        self.sample_data = ns.sample_data
        self.sample_data_prefix = ns.sample_data_prefix
        self.wave_numbers_in_header = ns.wave_numbers_in_header
        self.wave_numbers_regexp = ns.wave_numbers_regexp

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum2D]

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
        if self.wave_numbers_in_header is None:
            self.wave_numbers_in_header = False
        self._reader = self._init_reader()
        if self.direct_read:
            self._inputs = []
        else:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.csv", resume_from=self.resume_from)

    def _init_reader(self):
        """
        Initializes the reader.

        :return: the reader
        """
        reader = SReader()
        reader.options = self._compile_options()
        return reader

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying writer.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        if self.sample_id is not None:
            result.extend(["--sample-id", self.sample_id])
        if self.spectral_data is not None:
            result.extend(["--spectral-data", self.spectral_data])
        if self.sample_data is not None:
            result.extend(["--sample-data", self.sample_data])
            if self.sample_data_prefix is not None:
                result.extend(["--sample-data-prefix", self.sample_data_prefix])
        if self.wave_numbers_in_header:
            result.append("--wave-numbers-in-header")
            if self.wave_numbers_regexp is not None:
                result.extend(["--wave-numbers-regexp", self.wave_numbers_regexp])
        return result

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        i = 0
        for sp in self._reader.read(self.session.current_input):
            i += 1
            spectrum_name = os.path.basename(self.session.current_input)
            spectrum_name = os.path.splitext(spectrum_name)[0] + "-" + str(i)
            yield Spectrum2D(spectrum_name=spectrum_name, spectrum=sp)

    def read_fp(self, fp) -> Iterable:
        """
        Reads the data from the file-like object and returns the items one by one.

        :param fp: the file-like object to read from
        :return: the data
        :rtype: Iterable
        """
        i = 0
        for sp in self._reader.read_fp(fp):
            i += 1
            yield Spectrum2D(spectrum_name=sp.id, spectrum=sp)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0


class CSVSampleDataReader(SampleDataReader, DirectReader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None, resume_from: str = None,
                 sample_id: str = None, sample_data: str = None, sample_data_prefix: str = None, direct_read: bool = False,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param sample_id: the 1-based index of the sample ID column
        :type sample_id: str
        :param sample_data: the range of reference data columns (1-based)
        :type sample_data: str
        :param sample_data_prefix: the prefix to use for the sample data columns
        :typer sample_data_prefix: str
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
        self.sample_id = sample_id
        self.sample_data = sample_data
        self.sample_data_prefix = sample_data_prefix
        self._direct_read = direct_read
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-csv-sd"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the sample data in CSV format (row-wise)."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the CSV file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the CSV files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.csv'", required=False)
        parser.add_argument("--sample_id", type=str, help="The 1-based index of the sample ID column.", required=False, default="1")
        parser.add_argument("--sample_data", type=str, help="The range of columns containing the reference values (1-based).", required=False, default="2-last")
        parser.add_argument("--sample_data_prefix", type=str, help="The prefix used by the sample data columns.", required=False, default=None)
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
        self.sample_id = ns.sample_id
        self.sample_data = ns.sample_data
        self.sample_data_prefix = ns.sample_data_prefix

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [SampleData]

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
        if self.sample_id is None:
            raise Exception("No sample ID index specified!")
        if self.sample_data is None:
            self.sample_data = "2-last"
        if self.sample_data_prefix is None:
            self.sample_data_prefix = ""
        if self.direct_read:
            self._inputs = []
        else:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.csv", resume_from=self.resume_from)

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        with open(self.session.current_input, "r") as fp:
            yield self.read_fp(fp)

    def read_fp(self, fp) -> Iterable:
        """
        Reads the data from the file-like object and returns the items one by one.

        :param fp: the file-like object to read from
        :return: the data
        :rtype: Iterable
        """
        sample_id_index = None
        sample_data_range = None
        names = None
        reader = csv.reader(fp)
        first = True
        row_idx = 0
        for row in reader:
            if first:
                if len(self.sample_id) > 0:
                    sample_id = Index(self.sample_id, maximum=len(row))
                    sample_id_index = sample_id.value()
                if (self.sample_data is not None) and (len(self.sample_data) > 0):
                    sample_data = Range(self.sample_data, maximum=len(row))
                    sample_data_range = sample_data.indices()
                else:
                    sample_data_range = []
                names = []
                for idx in sample_data_range:
                    name = row[idx]
                    if (len(self.sample_data_prefix) > 0) and name.startswith(self.sample_data_prefix):
                        name = name[len(self.sample_data_prefix):]
                    names.append(name)
                first = False
            else:
                row_idx += 1
                sd = dict()
                if sample_id_index is not None:
                    sd[SAMPLE_ID] = row[sample_id_index]
                for i, idx in enumerate(sample_data_range):
                    sd[names[i]] = row[idx]
                if self.session.current_input is None:
                    name = str(row_idx)
                else:
                    name = os.path.splitext(os.path.basename(self.session.current_input))[0] + str(row_idx)
                yield SampleData(sampledata_name=name, sampledata=sd)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
