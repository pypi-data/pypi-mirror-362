import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.spectralio.cal import Writer as SWriter

from ._nir import NIRWriter
from ..api import make_list


class CALWriter(NIRWriter):

    def __init__(self, output_file: str = None, instrument_name: str = None,
                 product_code: str = None, product_code_from_field: bool = None, client: str = None,
                 file_id: str = None, sample_id_1: str = None, sample_id_2: str = None,
                 sample_id_3: str = None, serial_no: str = None, master: str = None,
                 operator: str = None, segment_widths: List[int] = None, start_points: List[float] = None,
                 increments: List[float] = None, end_points: List[float] = None, EOC: int = None, timestamp: str = None,
                 constituents: List[str] = None,
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
        :param constituents: the constituents (names of modeling targets to store in CAL file)
        :type constituents: list of str
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
        super().__init__(output_file=output_file, instrument_name=instrument_name, product_code=product_code,
                         product_code_from_field=product_code_from_field, client=client, file_id=file_id,
                         sample_id_1=sample_id_1, sample_id_2=sample_id_2, sample_id_3=sample_id_3,
                         serial_no=serial_no, master=master, operator=operator, segment_widths=segment_widths,
                         start_points=start_points, increments=increments, end_points=end_points,
                         EOC=EOC, timestamp=timestamp,
                         split_names=split_names, split_ratios=split_ratios, split_group=split_group,
                         logger_name=logger_name, logging_level=logging_level)
        self.constituents = constituents

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-cal"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the spectra in FOSS CAL format."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".cal"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("--constituents", type=str, help="The constituents (names of modeling targets to store in CAL file)", required=False, default=[], nargs="+")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.constituents = ns.constituents

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        if self.constituents is None:
            self.constituents = []
        super().initialize()

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying writer.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        if len(self.constituents) > 0:
            result.append("--constituents")
            result.extend([str(x) for x in self.constituents])
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
