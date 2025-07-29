import argparse
from typing import List

from seppl.placeholders import InputBasedPlaceholderSupporter
from seppl.io import DirectBatchWriter
from wai.logging import LOGGING_WARNING
from wai.spectralio.nir import Writer as SWriter

from sdc.api import Spectrum2D, SplittableBatchWriter, SpectralIOWriter, DefaultExtensionWriter, make_list


class NIRWriter(SplittableBatchWriter, SpectralIOWriter, DirectBatchWriter, DefaultExtensionWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_file: str = None, instrument_name: str = None,
                 product_code: str = None, product_code_from_field: bool = None, client: str = None,
                 file_id: str = None, sample_id_1: str = None, sample_id_2: str = None,
                 sample_id_3: str = None, serial_no: str = None, master: str = None,
                 operator: str = None, segment_widths: List[int] = None, start_points: List[float] = None,
                 increments: List[float] = None, end_points: List[float] = None, EOC: int = None, timestamp: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the output file to save the spectra to
        :type output_file: str
        :param instrument_name: the instrument name used in the header
        :type instrument_name: str
        :param product_code: either the attribute name with the product code in it, or the actual product code to be used
        :type product_code: str
        :param product_code_from_field: whether to use the product code option as the attribute name containing the actual product code
        :type product_code_from_field: bool
        :param client: the client name used in the header
        :type client: str
        :param file_id: the file ID to use
        :type file_id: str
        :param sample_id_1: the sample ID 1
        :type sample_id_1: str
        :param sample_id_2: the sample ID 2
        :type sample_id_2: str
        :param sample_id_3: the sample ID 3
        :type sample_id_3: str
        :param serial_no: serial number of instrument
        :type serial_no: str
        :param master: serial number of master instrument
        :type master: str
        :param operator: instrument operator
        :type operator: str
        :param segment_widths: width of segments
        :type segment_widths: list of int
        :param start_points: start points of segments
        :type start_points: list of float
        :param increments: wave increments
        :type increments: list of float
        :param end_points: end points of segments
        :type end_points: list of float
        :param EOC: number of EOCs per rev
        :type EOC: int
        :param timestamp: the timestamp to use in the file
        :type timestamp: str
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param split_group: the regular expression with a single group used for keeping items in the same split, e.g., for identifying the base name of a file or the sample ID
        :type split_group: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, split_group=split_group, logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.instrument_name = instrument_name
        self.product_code = product_code
        self.product_code_from_field = product_code_from_field
        self.client = client
        self.file_id = file_id
        self.sample_id_1 = sample_id_1
        self.sample_id_2 = sample_id_2
        self.sample_id_3 = sample_id_3
        self.serial_no = serial_no
        self.master = master
        self.operator = operator
        self.segment_widths = segment_widths
        self.start_points = start_points
        self.increments = increments
        self.end_points = end_points
        self.EOC = EOC
        self.timestamp = timestamp
        self._writer = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-nir"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the spectra in FOSS NIR format."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".nir"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The NIR file to store the spectra in.", required=False)
        parser.add_argument("--instrument_name", type=str, help="The instrument name to use in the header", required=False, default="<not implemented>")
        parser.add_argument("--product_code", type=str, help="Either the attribute name with the product code in it, or the actual product code to be used", required=False, default="01")
        parser.add_argument("--product_code_from_field", action="store_true", help="Whether to use the product code option as the attribute name containing the actual product code")
        parser.add_argument("--client", type=str, help="The client name to use in the header", required=False, default="client")
        parser.add_argument("--file_id", type=str, help="The file ID to use", required=False, default="generated by spectral-data-converter")
        parser.add_argument("--sample_id_1", type=str, help="The sample ID 1 to use", required=False, default="")
        parser.add_argument("--sample_id_2", type=str, help="The sample ID 2 to use", required=False, default="")
        parser.add_argument("--sample_id_3", type=str, help="The sample ID 3 to use", required=False, default="")
        parser.add_argument("--serial_no", type=str, help="The serial number of instrument", required=False, default="0000-0000-0000")
        parser.add_argument("--master", type=str, help="The serial number of the master instrument", required=False, default="0000-0000-0000")
        parser.add_argument("--operator", type=str, help="The instrument operator", required=False, default="spectral-data-converter")
        parser.add_argument("--segment_widths", type=int, help="The width of segments", required=False, default=[1050], nargs="+")
        parser.add_argument("--start_points", type=float, help="The start points of segments", required=False, default=[400.0], nargs="+")
        parser.add_argument("--increments", type=float, help="The wave increments", required=False, default=[2.0], nargs="+")
        parser.add_argument("--end_points", type=float, help="The end points of segments", required=False, default=[1098.0], nargs="+")
        parser.add_argument("--EOC", type=int, help="The number of EOCs per rev", required=False, default=0)
        parser.add_argument("--timestamp", type=str, help="The timestamp to use in the file", required=False, default=None)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output
        self.instrument_name = ns.instrument_name
        self.product_code = ns.product_code
        self.product_code_from_field = ns.product_code_from_field
        self.client = ns.client
        self.file_id = ns.file_id
        self.sample_id_1 = ns.sample_id_1
        self.sample_id_2 = ns.sample_id_2
        self.sample_id_3 = ns.sample_id_3
        self.serial_no = ns.serial_no
        self.master = ns.master
        self.operator = ns.operator
        self.segment_widths = ns.segment_widths
        self.start_points = ns.start_points
        self.increments = ns.increments
        self.end_points = ns.end_points
        self.EOC = ns.EOC
        self.timestamp = ns.timestamp

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum2D]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.instrument_name is None:
            self.instrument_name = "<not implemented>"
        if self.product_code is None:
            self.product_code = "01"
        if self.product_code_from_field is None:
            self.product_code_from_field = False
        if self.client is None:
            self.client = "client"
        if self.file_id is None:
            self.file_id = "generated by spectral-data-converter"
        if self.sample_id_1 is None:
            self.sample_id_1 = ""
        if self.sample_id_2 is None:
            self.sample_id_2 = ""
        if self.sample_id_3 is None:
            self.sample_id_3 = ""
        if self.serial_no is None:
            self.serial_no = "0000-0000-0000"
        if self.master is None:
            self.master = "0000-0000-0000"
        if self.operator is None:
            self.operator = "spectral-data-converter"
        if self.segment_widths is None:
            self.segment_widths = [1050]
        if self.start_points is None:
            self.start_points = [400.0]
        if self.increments is None:
            self.increments = [2.0]
        if self.end_points is None:
            self.end_points = [1098.0]
        if self.EOC is None:
            self.EOC = 0
        self._writer = self._init_writer()

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying writer.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        result.extend(["--instrument-name=%s" % self.instrument_name])
        result.extend(["--product-code=%s" % self.product_code])
        if self.product_code_from_field:
            result.append("--product-code-from-field")
        result.extend(["--client=%s" % self.client])
        result.extend(["--file-id=%s" % self.file_id])
        if len(self.sample_id_1) > 0:
            result.extend(["--sample-id-1=%s" % self.sample_id_1])
        if len(self.sample_id_2) > 0:
            result.extend(["--sample-id-2=%s" % self.sample_id_2])
        if len(self.sample_id_3) > 0:
            result.extend(["--sample-id-3=%s" % self.sample_id_3])
        result.extend(["--serial-no=%s" % self.serial_no])
        result.extend(["--master=%s" % self.master])
        result.extend(["--operator=%s" % self.operator])
        result.append("--segment-widths")
        result.extend([str(x) for x in self.segment_widths])
        result.append("--start-points")
        result.extend([str(x) for x in self.start_points])
        result.append("--increments")
        result.extend([str(x) for x in self.increments])
        result.append("--end-points")
        result.extend([str(x) for x in self.end_points])
        result.append("--EOC=%s" % self.EOC)
        if self.timestamp is not None:
            result.extend("--timestamp=%s" % self.timestamp)
        return result

    def _init_writer(self):
        """
        Initializes the writer.

        :return: the writer
        """
        writer = SWriter()
        writer.options = self._compile_options()
        return writer

    def write_batch(self, data):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        if self.output_file is None:
            raise Exception("No output file specified!")

        output_file = self.session.expand_placeholders(self.output_file)
        self.logger().info("Writing spectra to: %s" % output_file)
        self._writer.write([x.spectrum for x in data], output_file)

    def write_batch_fp(self, data, fp, as_bytes: bool):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        :param fp: the file-like object to write to
        :param as_bytes: whether to write as str or bytes
        :type as_bytes: bool
        """
        data = make_list(data)
        self._writer.write_fp([x.spectrum for x in data], fp, as_bytes)
