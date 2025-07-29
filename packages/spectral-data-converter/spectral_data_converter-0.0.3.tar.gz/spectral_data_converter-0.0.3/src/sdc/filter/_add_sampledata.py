import argparse
from typing import List

from seppl import init_initializable, Initializable
from wai.logging import LOGGING_WARNING

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, parse_reader, SAMPLE_ID


class AddSampleData(Filter):
    """
    Loads sample data with the specified sample data reader and adds it to the spectra passing through based on matching sample ID.
    """

    def __init__(self, reader: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param reader: the sample data reader command-line for loading the sample data
        :type reader: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.reader = reader
        self._reader = None
        self._sampledata = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "add-sampledata"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Loads sample data with the specified sample data reader and adds it to the spectra passing through based on matching sample ID."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum2D]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [Spectrum2D]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-r", "--reader", type=str, help="The sample data reader command-line.", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.reader = ns.reader

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.reader is not None:
            self._reader = parse_reader(self.reader)
            self._reader.session = self.session
            if isinstance(self._reader, Initializable) and not init_initializable(self._reader, "reader"):
                self.logger().error("Failed to initialize sample data reader: %s" % self.reader)
            else:
                self._sampledata = dict()
                while not self._reader.has_finished():
                    for sd in self._reader.read():
                        if SAMPLE_ID in sd.sampledata:
                            self._sampledata[sd.sampledata[SAMPLE_ID]] = sd
                        else:
                            self.logger().warning("No '%s' field in sample data, skipping: %s" % (SAMPLE_ID, str(sd.sampledata)))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        if self._sampledata is None:
            return data

        result = []
        for item_old in make_list(data):
            sid = item_old.spectrum.id
            if sid not in self._sampledata:
                self.logger().warning("No sample data for sample ID: %s" % sid)
                result.append(item_old)
            else:
                self.logger().info("Updating spectrum with sample ID: %s" % sid)
                item_new = safe_deepcopy(item_old)
                item_new.spectrum.sample_data.update(self._sampledata[sid].sampledata)
                result.append(item_new)

        return flatten_list(result)
