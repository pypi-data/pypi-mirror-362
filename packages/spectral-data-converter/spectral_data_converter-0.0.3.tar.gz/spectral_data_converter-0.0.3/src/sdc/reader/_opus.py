import argparse
from typing import List, Iterable, Union

from seppl.io import locate_files, DirectReader
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from wai.logging import LOGGING_WARNING
from wai.spectralio.opus import Reader as SReader

from sdc.api import SpectralIOReader, Spectrum2D


class OPUSReader(SpectralIOReader, DirectReader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 resume_from: str = None, instrument: str = None, format: str = None, keep_format: bool = None,
                 sample_id: str = None, start: int = None, max: int = None, add_trace_to_report: bool = None,
                 direct_read: bool = False, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param instrument: the instrument name to use
        :type instrument: str
        :param format: the spectral format
        :type format: str
        :param keep_format: whether to keep the format determined by the reader
        :type keep_format: bool
        :param sample_id: the field with the sample ID
        :type sample_id: str
        :param start: the spectrum number to start loading from
        :type start: int
        :param max: the maximum number of spectra to load, None or -1 for unlimited
        :type max: int
        :param add_trace_to_report: if enabled the trace of identified blocks etc gets added to the report, using prefix 'Trace.'
        :type add_trace_to_report: bool
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
        self.start = start
        self.max = max
        self.add_trace_to_report = add_trace_to_report
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
        return "from-opus"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the spectra in Bruker OPUS format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the OPUS file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the OPUS files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.0'", required=False)
        parser.add_argument("--sample_id", type=str, help="ID|Field1|Field2|Field3|[prefix]", required=False, default="SNM")
        parser.add_argument("-s", "--start", type=int, help="The spectrum number to start loading from", required=False, default=1)
        parser.add_argument("-m", "--max", type=int, help="The maximum number of spectra to load, -1 for all", required=False, default=-1)
        parser.add_argument("--add_trace_to_report", action="store_true", help="If enabled the trace of identified blocks etc gets added to the report, using prefix 'Trace.'")
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
        self.start = ns.start
        self.max = ns.max
        self.add_trace_to_report = ns.add_trace_to_report

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
        if self.sample_id is None:
            self.sample_id = "SNM"
        if self.start is None:
            self.start = 1
        if self.max is None:
            self.max = -1
        if self.add_trace_to_report is None:
            self.add_trace_to_report = False
        self._reader = self._init_reader()
        if self.direct_read:
            self._inputs = []
        else:
            self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.0", resume_from=self.resume_from)

    def _init_reader(self):
        """
        Initializes the reader.

        :return: the reader
        """
        reader = SReader(options=self._compile_options())
        return reader

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying reader.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        result.extend(["--sample-id", self.sample_id])
        result.append("--start=%s" % str(self.start))
        result.append("--max=%s" % str(self.max))
        if self.add_trace_to_report:
            result.append("--add-trace-to-report")
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

        for sp in self._reader.read(self.session.current_input):
            yield Spectrum2D(source=self.session.current_input, spectrum=sp, spectrum_name=sp.id)

    def read_fp(self, fp) -> Iterable:
        """
        Reads the data from the file-like object and returns the items one by one.

        :param fp: the file-like object to read from
        :return: the data
        :rtype: Iterable
        """
        for sp in self._reader.read_fp(fp):
            yield Spectrum2D(spectrum_name=sp.id, spectrum=sp)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
