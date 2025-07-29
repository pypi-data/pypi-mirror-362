import argparse
from typing import List

from seppl import AnyData
from wai.logging import LOGGING_WARNING

from sdc.api import BatchFilter, parse_cleaner


class ApplyCleaner(BatchFilter):
    """
    Applies the cleaner to the data.
    """

    def __init__(self, cleaner: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param cleaner: the cleaner command-line
        :type cleaner: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.cleaner = cleaner
        self._cleaner = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "apply-cleaner"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Applies the specified cleaner to the batches of data it receives."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        if self._cleaner is None:
            return [AnyData]
        else:
            return self._cleaner.accepts()

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        if self._cleaner is None:
            return [AnyData]
        else:
            return self._cleaner.generates()

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-c", "--cleaner", type=str, default=None, help="The command-line defining the cleaner.")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.cleaner = ns.cleaner

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        if self.cleaner is None:
            self._cleaner = None
        else:
            self._cleaner = parse_cleaner(self.cleaner)

    def _process_batch(self, batch):
        """
        Processes the batch.

        :param batch: the batch to process
        :return: the potentially updated batch
        """
        if self._cleaner is None:
            self.logger().warning("No cleaner defined, just passing through the data!")
            return batch

        return self._cleaner.clean(batch)
