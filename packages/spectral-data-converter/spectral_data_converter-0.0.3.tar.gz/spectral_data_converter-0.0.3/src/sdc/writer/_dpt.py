import argparse
import os
from typing import List

from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter
from seppl.io import DirectStreamWriter
from wai.logging import LOGGING_WARNING
from wai.spectralio.dpt import Writer as SWriter

from sdc.api import Spectrum2D, SplittableStreamWriter, make_list, add_locale_option, SpectralIOWriter, DefaultExtensionWriter


class DPTWriter(SplittableStreamWriter, SpectralIOWriter, DirectStreamWriter, DefaultExtensionWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, descending: bool = None, locale: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the .spec files in
        :type output_dir: str
        :param descending: whether to output the wave numbers in descending order
        :type descending: bool
        :param locale: the locale to use for writing the numbers
        :type locale: str
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
        self.descending = descending
        self.locale = locale
        self._writer = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-dpt"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the spectrum in DPT format."

    @property
    def default_extension(self) -> str:
        """
        Returns the default extension (incl dot) for this file type.

        :return: the default extension
        :rtype: str
        """
        return ".dpt"

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the .asc files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=False)
        parser.add_argument("--descending", action="store_true", help="Outputs the wave numbers in descending order")
        add_locale_option(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.descending = ns.descending
        self.locale = ns.locale

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
        if self.descending is None:
            self.descending = False
        if self.locale is None:
            self.locale = "en_US"
        self._writer = self._init_writer()

    def _compile_options(self) -> List[str]:
        """
        Compiles the options for initializing the underlying writer.

        :return: the list of options to use
        :rtype: list
        """
        result = super()._compile_options()
        if self.descending:
            result.append("--descending")
        result.extend(["--locale", self.locale])
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
