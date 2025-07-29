import argparse
import os
from typing import List, Dict, Any

from javaproperties import Properties, dump, dumps
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter
from seppl.io import DirectStreamWriter
from wai.logging import LOGGING_WARNING
from wai.spectralio.adams import DATATYPE_SUFFIX
from wai.spectralio.adams import Writer as SWriter

from sdc.api import Spectrum2D, SplittableStreamWriter, SplittableSampleDataStreamWriter, make_list, SpectralIOWriter, DefaultExtensionWriter


class AdamsWriter(SplittableStreamWriter, SpectralIOWriter, DirectStreamWriter, DefaultExtensionWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, output_sampledata: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the .spec files in
        :type output_dir: str
        :param output_sampledata: whether to output the sample data as well
        :type output_sampledata: bool
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
        self.output_dir = output_dir
        self.output_sampledata = output_sampledata
        self._writer = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-adams"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the spectrum in ADAMS .spec format."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".spec"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the .spec files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=False)
        parser.add_argument("--output_sampledata", action="store_true", help="Outputs the sampledata as well")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.output_sampledata = ns.output_sampledata

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
        if self.output_sampledata is None:
            self.output_sampledata = False
        self._writer = self._init_writer()

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying writer.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        if self.output_sampledata:
            result.append("--output-sampledata")
        return result

    def _init_writer(self):
        """
        Initializes the writer.

        :return: the writer
        """
        writer = SWriter()
        writer.options = self._compile_options()
        return writer

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        if self.output_dir is None:
            raise Exception("No output directory specified!")

        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next(item=item.spectrum_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            path = os.path.join(sub_dir, item.spectrum_name)
            path = os.path.splitext(path)[0] + self.default_extension
            self.logger().info("Writing spectrum to: %s" % path)
            self._writer.write([item.spectrum], path)

    def write_stream_fp(self, data, fp, as_bytes: bool):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        :param fp: the file-like object to write to
        :param as_bytes: whether to write as str or bytes
        :type as_bytes: bool
        """
        self._writer.write_fp([x.spectrum for x in make_list(data)], fp, as_bytes)


class ReportSampleDataWriter(SplittableSampleDataStreamWriter, DirectStreamWriter, DefaultExtensionWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the .spec files in
        :type output_dir: str
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
        self.output_dir = output_dir

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-report-sd"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the sample data in ADAMS .report format."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".report"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the .report files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output

    def _to_props(self, sd: Dict[str, Any]) -> Properties:
        """
        Turns the sample data into java props.

        :param sd: the sample data to convert
        :type sd: dict
        :return: th generated properties object
        :rtype: Properties
        """
        props = Properties()
        for k in sd:
            value = sd[k]
            if isinstance(value, bool):
                props[k] = str(sd[k])
                props[k + DATATYPE_SUFFIX] = "B"
            elif isinstance(value, (int, float)):
                props[k] = str(sd[k])
                props[k + DATATYPE_SUFFIX] = "N"
            elif isinstance(value, str):
                props[k] = str(sd[k])
                props[k + DATATYPE_SUFFIX] = "S"
            else:
                props[k] = str(sd[k])
                props[k + DATATYPE_SUFFIX] = "U"
        return props

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        if self.output_dir is None:
            raise Exception("No output directory specified!")

        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next(item=item.sampledata_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            path = os.path.join(sub_dir, item.sampledata_name)
            path = os.path.splitext(path)[0] + ".report"
            self.logger().info("Writing sample data to: %s" % path)
            with open(path, "w") as fp:
                dump(self._to_props(item.sampledata), fp)

    def write_stream_fp(self, data, fp, as_bytes: bool):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        :param fp: the file-like object to write to
        :param as_bytes: whether to write as str or bytes
        :type as_bytes: bool
        """
        data = make_list(data)
        if len(data) != 1:
            raise Exception("Can only save single sample data at a time!")
        if as_bytes:
            fp.write(dumps(self._to_props(data[0].sampledata)).encode())
        else:
            dump(self._to_props(data[0].sampledata), fp)
