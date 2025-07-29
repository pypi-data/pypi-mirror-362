import argparse
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING

from sdc.api import flatten_list, make_list, Spectrum, load_function


class PythonFunctionFilter(Filter):
    """
    Applies a Python function to the data.
    """

    def __init__(self, function: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param function: the function to use (module_name:function_name)
        :type function: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.function = function
        self._function = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "pyfunc-filter"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "The declared Python function processes spectrum containers. The function must handle a single spectrum container or an iterable of spectrum containers and return a single spectrum container or an iterable of spectrum containers."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum]

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

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._function = load_function(self.function)

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        for item in make_list(data):
            if issubclass(type(item), Spectrum):
                new_items = self._function(item)
                if new_items is None:
                    continue
                new_items = make_list(new_items)
                for new_item in new_items:
                    if new_item is None:
                        continue
                    if issubclass(type(item), Spectrum):
                        result.append(new_item)
                    else:
                        self.logger().error("Function '%s' did not return an object of type '%s' but of type '%s'!" % (self.function, str(Spectrum), str(type(item))))
            else:
                self.logger().error("Did not receive an object of type '%s' but of type '%s'!" % (str(Spectrum), str(type(item))))

        return flatten_list(result)
