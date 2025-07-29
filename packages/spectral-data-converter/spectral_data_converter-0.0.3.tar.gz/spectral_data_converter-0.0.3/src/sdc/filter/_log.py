import argparse
import numpy as np
from typing import List

from wai.logging import LOGGING_WARNING
from wai.ma.transformation import Log as WaiLog

from sdc.api import flatten_list, make_list, Filter, Spectrum2D, safe_deepcopy, spectrum_to_matrix, matrix_to_spectrum


class Log(Filter):
    """
    Log-transforms the spectra.
    """

    def __init__(self, base: float = None, offset: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param base: the base to use for the logarithm
        :type base: float
        :param offset: the offset to use for the spectra
        :type offset: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.base = base
        self.offset = offset

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "log"

    def description(self) -> str:
        """
        Returns a description of the filter.

        :return: the description
        :rtype: str
        """
        return "Log-transforms the spectra."

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
        parser.add_argument("-b", "--base", type=float, help="The base for the logarithm.", default=np.e, required=False)
        parser.add_argument("-o", "--offset", type=float, help="The offset for the spectra.", default=1.0, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.base = ns.base
        self.offset = ns.offset

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.base is None:
            self.base = np.e
        if self.offset is None:
            self.offset = 1.0

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []

        trans = WaiLog()
        trans.base = self.base
        trans.offset = self.offset

        for item_old in make_list(data):
            sp_old = item_old.spectrum
            mat_old = spectrum_to_matrix(sp_old, add_waveno=False)
            mat_new = trans.transform(mat_old)
            sp_new = matrix_to_spectrum(mat_new, sample_id=sp_old.id, waveno=safe_deepcopy(sp_old.waves), sample_data=safe_deepcopy(sp_old.sample_data))
            item_new = Spectrum2D(spectrum_name=item_old.spectrum_name, spectrum=sp_new)
            result.append(item_new)

        return flatten_list(result)
