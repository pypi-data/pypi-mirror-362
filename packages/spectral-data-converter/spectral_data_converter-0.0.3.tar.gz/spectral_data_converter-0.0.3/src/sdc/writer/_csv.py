import argparse
import csv
from io import StringIO
from typing import List

from seppl.placeholders import InputBasedPlaceholderSupporter
from seppl.io import DirectBatchWriter
from wai.logging import LOGGING_WARNING
from wai.spectralio.csv import Writer as SWriter, PLACEHOLDERS, PH_WAVE_NUMBER

from sdc.api import Spectrum2D, SplittableBatchWriter, SplittableSampleDataBatchWriter, SampleData, SAMPLE_ID, \
    SpectralIOWriter, make_list, DefaultExtensionWriter


class CSVWriter(SplittableBatchWriter, SpectralIOWriter, DirectBatchWriter, DefaultExtensionWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_file: str = None, sample_id: str = None, sample_data: List[str] = None,
                 sample_data_prefix: str = None, wave_numbers_format: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the output file to save the spectra to
        :type output_file: str
        :param sample_id: the attribute name to use for the sample ID
        :type sample_id: str
        :param sample_data: the sample data fields to store in the CSV file
        :type sample_data: list of str
        :param sample_data_prefix: the prefix to use for the sample data attributes
        :typer sample_data_prefix: str
        :param wave_numbers_format: the format to use for constructing the wave number attribute names
        :type wave_numbers_format: str
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
        self.sample_id = sample_id
        self.sample_data = sample_data
        self.sample_data_prefix = sample_data_prefix
        self.wave_numbers_format = wave_numbers_format
        self._writer = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-csv"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the spectra in CSV format (row-wise)."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".csv"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The CSV file to store the spectra in.", required=False)
        parser.add_argument("--sample_id", type=str, help="The name to use for the sample ID column.", required=False, default="sample_id")
        parser.add_argument("--sample_data", type=str, help="The sample data names to store in CSV file.", required=False, default=[], nargs="*")
        parser.add_argument("--sample_data_prefix", type=str, help="The prefix to use for the sample data columns.", required=False, default="")
        parser.add_argument("--wave_numbers_format", type=str, help="The format to use for the spectral data columns, the following placeholders are available: " + "|".join(PLACEHOLDERS), default=PH_WAVE_NUMBER)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output
        self.sample_id = ns.sample_id
        self.sample_data = ns.sample_data
        self.sample_data_prefix = ns.sample_data_prefix
        self.wave_numbers_format = ns.wave_numbers_format

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
        if self.sample_data is None:
            self.sample_data = []
        self._writer = self._init_writer()

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying writer.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        if self.sample_id is not None:
            result.extend(["--sample-id", self.sample_id])
        if len(self.sample_data) > 0:
            result.append("--sample-data")
            result.extend([str(x) for x in self.sample_data])
            if self.sample_data_prefix is not None:
                result.extend(["--sample-data-prefix", self.sample_data_prefix])
        if self.wave_numbers_format is not None:
            result.extend(["--wave-numbers-format", self.wave_numbers_format])
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


class CSVSampleDataWriter(SplittableSampleDataBatchWriter, DirectBatchWriter, DefaultExtensionWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_file: str = None, sample_id: str = None, sample_data: List[str] = None,
                 sample_data_prefix: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the output file to save the spectra to
        :type output_file: str
        :param sample_id: the attribute name to use for the sample ID
        :type sample_id: str
        :param sample_data: the sample data fields to store in the CSV file
        :type sample_data: list of str
        :param sample_data_prefix: the prefix to use for the sample data attributes
        :typer sample_data_prefix: str
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
        self.sample_id = sample_id
        self.sample_data = sample_data
        self.sample_data_prefix = sample_data_prefix

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-csv-sd"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the sample data in CSV format (row-wise)."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".csv"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The CSV file to store the sample data in.", required=False)
        parser.add_argument("--sample_id", type=str, help="The name to use for the sample ID column.", required=False, default="sample_id")
        parser.add_argument("--sample_data", type=str, help="The sample data names to store in CSV file.", required=False, default=[], nargs="*")
        parser.add_argument("--sample_data_prefix", type=str, help="The prefix to use for the sample data columns.", required=False, default="")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output
        self.sample_id = ns.sample_id
        self.sample_data = ns.sample_data
        self.sample_data_prefix = ns.sample_data_prefix

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [SampleData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.sample_id is None:
            self.sample_id = "sample_id"
        if self.sample_data is None:
            self.sample_data = []
        if self.sample_data_prefix is None:
            self.sample_data_prefix = ""

    def write_batch(self, data):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        if self.output_file is None:
            raise Exception("No output file specified!")

        output_file = self.session.expand_placeholders(self.output_file)
        self.logger().info("Writing sample data to: %s" % output_file)

        with open(output_file, "w") as fp:
            self.write_batch_fp(data, fp, False)

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
        if as_bytes:
            buffer = StringIO()
            writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)
        else:
            buffer = None
            writer = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)

        # header
        row = [self.sample_id]
        if len(self.sample_data) == 0:
            names = []
            for name in sorted(data[0].sampledata.keys()):
                if name == SAMPLE_ID:
                    continue
                names.append(name)
            self.logger().info(
                "No sample data fields specified, using all available from first spectrum: %s" % ",".join(names))
        else:
            names = self.sample_data
        for name in names:
            row.append(self.sample_data_prefix + name)
        writer.writerow(row)

        # data
        for sd in data:
            row = ["NA" if (SAMPLE_ID not in sd.sampledata) else sd.sampledata[SAMPLE_ID]]
            for name in names:
                if name in sd.sampledata:
                    row.append(sd.sampledata[name])
                else:
                    row.append("")
            writer.writerow(row)

        if as_bytes:
            fp.write(buffer.getvalue().encode())
