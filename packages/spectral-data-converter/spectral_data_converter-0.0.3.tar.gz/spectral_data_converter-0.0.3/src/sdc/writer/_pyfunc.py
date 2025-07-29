import argparse
from typing import List

from wai.logging import LOGGING_WARNING

from sdc.api import Spectrum, SplittableStreamWriter, make_list, load_function


class PythonFunctionWriter(SplittableStreamWriter):

    def __init__(self, function: str = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param function: the function to use (module_name:function_name)
        :type function: str
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
        self.function = function
        self._function = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-pyfunc"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Processes the spectra via the declared Python function. The function must take an Spectrum2D container as input and an optional 'split' string parameter."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-f", "--function", type=str, default=None, help="The Python function to use, format: module_name:function_name", required=True)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.function = ns.function

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._function = load_function(self.function)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            if issubclass(type(item), Spectrum):
                split = None
                if self.splitter is not None:
                    split = self.splitter.next(item=item.spectrum_name)
                self.logger().info("Processing spectrum '%s' (split: %s)" % (item.spectrum_name, str(split)))
                self._function(item, split)
            else:
                self.logger().error("Did not receive an object of type '%s' but of type '%s'!" % (str(Spectrum), str(type(item))))
