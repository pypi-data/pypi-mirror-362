import argparse
from typing import List

from wai.logging import LOGGING_WARNING
from wai.ma.filter import Downsample

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, spectrum_to_matrix, matrix_to_spectrum


class DownSample(Filter):
    """
    Picks every n-th wave number.
    """

    def __init__(self, start_index: int = None, step: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param start_index: the index to start sampling from
        :type start_index: int
        :param step: the step-size between samples
        :type step: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.start_index = start_index
        self.step = step

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "downsample"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Picks every n-th wave number."

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
        parser.add_argument("-s", "--start_index", type=int, help="The index to start sampling from.", default=0, required=False)
        parser.add_argument("-n", "--step", type=int, help="The step-size between samples.", default=1, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.start_index = ns.start_index
        self.step = ns.step

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.start_index is None:
            self.start_index = 0
        if self.start_index < 0:
            raise Exception("Start index has to be >=0, provided: %s" % str(self.start_index))
        if self.step is None:
            self.step = 1
        if self.step < 1:
            raise Exception("Step has to be >=1, provided: %s" % str(self.step))

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        flt = Downsample()
        flt.start_index = self.start_index
        flt.step = self.step

        for item in make_list(data):
            sp = item.spectrum
            mat = spectrum_to_matrix(sp, add_waveno=True)
            mat_new = flt.transform(mat)
            sp_new = matrix_to_spectrum(mat_new, sample_id=sp.id, sample_data=safe_deepcopy(sp.sample_data))
            item_new = Spectrum2D(spectrum_name=item.spectrum_name, spectrum=sp_new)
            result.append(item_new)

        return flatten_list(result)
